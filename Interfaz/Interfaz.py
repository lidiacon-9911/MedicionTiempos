from tkinter import *
from botocore import client
from matplotlib import figure
import numpy as np
import requests
import boto3
import pandas as lid
import matplotlib.pyplot as mat
from pandas import ExcelFile
from pandas import ExcelWriter
from openpyxl import Workbook
import json

ACCESS_KEY="ASIAZFIOXVCPFCD4PYHB"
SECRET_KEY="f0mTXTm6JNtkuc5RiJiCfzu3ysTBt76OUkDdhnWI"
bucket_name="tiempoconsulta"

from botocore import UNSIGNED
from botocore.client import Config
from botocore.exceptions import ClientError

#conexion boto3
client = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='')
client._request_signer.sign = (lambda *args, **kwargs:None)
ventana =Tk()
ventana.title("Grafico de Excels velocidad")
ventana.geometry('1200x600')
marco1 = Frame(ventana, bg="white", width = 600 , height = 160)
marco1.place(relx=0.27, rely=0.64)  

def servic_web():    
    servicio1 = requests.get("http://localhost:4000/paises/tiempo")
    content1 = json.loads(servicio1.text)
    servicio2 = requests.get("http://127.0.0.1:8000/tiempos_calculos")
    content2 = json.loads(servicio2.text)
    content1.update(content2)
    return content1

def img_file():
    df = lid.DataFrame(servic_web())
    write = ExcelWriter('Tiempos.xlsx')
    df.to_excel(write, 'Sheet1', index=False)
    write.save()
    valores = df[["flask_consultasPaises","tiemposcalculo_flask"]]
    ax2 = valores.plot.bar(x="flask_consultasPaises",y="tiemposcalculo_flask", rot = 0)
    mat.savefig('saved_figura.png')
    valores1 = df[["fastapi_consulta","fastapi_tiempos"]]
    ax1 = valores1.plot.bar(x="fastapi_consulta",y="fastapi_tiempos", rot = 0)
    mat.savefig('saved_figura1.png')
    mat.show()
    archivo1s3()
    archivo2s3()

def unionGraficos():
    pdf = lid.read_excel('C:/Users/Lenovo/Documents/lIDIA/Tendecnias Actuales/VisualCode/MedicionTiempos/flask/TiemposFlask.xlsx','Sheet' )
    print(pdf)
    mat.bar(pdf["flask_consultas"],pdf["flask_tiempos"], color='red',label='Tiempo Flask')
    mat.bar(pdf["fast_consultas"],pdf["fast_tiempos"], color='blue', label='Tiempo Fast')
    mat.title("Consulta de tiempos")
    mat.legend()
    mat.show()
    
def guardar():
  ruta = 'Grafica.pdf'
  client.upload_file(ruta, bucket_name, "Grafica.pdf",
  ExtraArgs={'ACL': 'public-read'})
  generaLink()

def archivo1s3():
    ruta = '/saved_figura.png'
    client.upload_file(ruta, bucket_name, "imagen1.png",
    ExtraArgs={'ACL': 'public-read'})

def archivo2s3():
    ruta = '/saved_figura1.png'
    client.upload_file(ruta, bucket_name, "imagen2.png",
    ExtraArgs={'ACL': 'public-read'})

#botones
boton1 = Button(ventana, text="Generar grafica", bg="white", height=10, width=85, command=unionGraficos)
boton1.place(relx=0.27, rely=0.21,)


def generaLink():
    label3 = Label(ventana,text="https://tiempoconsulta.s3.amazonaws.com/Grafica.pdf",height=3, width=70).place(relx=0.4, rely=0.69)
    #label3 = Label(ventana,text="https://tiempoconsulta.s3.amazonaws.com/imagen2.png",height=3, width=40).place(relx=0.4, rely=0.74)

botonGuardar = Button(ventana, text="Guardar Archivo" , command=guardar).place(x=45,y= 67)
ventana.mainloop()
