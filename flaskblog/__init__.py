"""
This is the constructor. here all the configuration settings are there
Author: Akshaya Revaskar
Date: 12/04/2020
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("Flask_SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("Flask_SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

# settings for mail
app.config['MAIL_SERVER'] = os.getenv("Flask_MAIL_SERVER")
app.config['MAIL_PORT'] = os.getenv("Flask_MAIL_PORT")
app.config['MAIL_USERNAME'] = os.getenv("Flask_MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("Flask_MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


from flaskblog import routes