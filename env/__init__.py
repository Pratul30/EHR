from logging import PlaceHolder
import bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import flask_excel as excel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY']='secretkey'
db=SQLAlchemy(app)
bcrypt= Bcrypt(app)
login_manager =LoginManager(app)
excel.init_excel(app)
login_manager.login_view= 'login'
from env import routes