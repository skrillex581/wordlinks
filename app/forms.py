from flask_wtf import Form
from wtforms.fields import TextField, BooleanField
from wtforms.validators import Required

class RegistrationForm(Form):
    txEmail = TextField()
    txEmailConfirm = TextField()

class LoginForm(Form):
    username = TextField() 
    remember_me = BooleanField('remember_me', default=True)

