from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)


#@app.before_first_request

from app import views,models
#from models import User, Role
