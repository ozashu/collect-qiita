from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cache import Cache
#from flask_redis import FlaskRedis
from flask_session import Session

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
cache = Cache(app ,config={'CACHE_TYPE': 'redis'})
#SESSION_TYPE = 'redis'
#SESSION_REDIS = "127.0.0.1:6379"
#Session(app)
#redis_store = FlaskRedis(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(userid):
    from .models import User
    return User.query.filter(User.id==userid).first()
