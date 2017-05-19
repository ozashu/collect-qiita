from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signin"

@login_manager.user_loader
def load_user(userid):
    from .models import User
    return User.query.filter(User.id==userid).first()
