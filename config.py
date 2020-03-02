from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)

CORS(app)
auth = HTTPTokenAuth(scheme='Bearer')
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = ''
app.config['CSRF_ENABLED'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = ""         #更改为你自己mysql的用户名和密码，记得新建database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


