# imports
from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# instantiation of the imports
app = Flask(__name__)
api = Api()
db = SQLAlchemy()
jwt = JWTManager()
