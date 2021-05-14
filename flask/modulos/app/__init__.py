from flask import Flask
import json
from flask_pymongo import PyMongo
import datetime
from flask_cors import CORS
from bson.objectid import ObjectId


class JSONEncoder(json.JSONEncoder):

    def default(self,o):
        if isinstance(o,ObjectId):
            return str(o)
        if isinstance(o,datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self,o)

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['MONGO_URI']= "mongodb+srv://flask:flask123@cluster0.67ou4.mongodb.net/paises?retryWrites=true&w=majority"


app.json_encoder = JSONEncoder
mongo = PyMongo(app)



from modulos.app.controladores import paises