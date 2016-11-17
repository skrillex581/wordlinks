import flask_user
from models import User


@login_manager.user_loader
def user_loader(email):
    return User.query.filter(email=email).first()


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    password = getsha256(request.form.get('email'))
    u = User.query.filter(email=email, password=password) 
    if u is None:
        return None
    return u