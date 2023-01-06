
import sys, os
from datetime import timedelta

from flask import Flask, session
from flask_cors import CORS
from flask_caching import Cache
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, send
# from flask_session import Session


from flaskapp.config_ import Config_

app = Flask(__name__)


if sys.platform == 'win32':
    config_redis = {
        'CACHE_TYPE': 'simple',
    }
else:
    print("Configuring redis...")
    config_redis = {
        'CACHE_TYPE': 'redis',
        'CACHE_KEY_PREFIX': 'server1',
        'CACHE_REDIS_HOST': 'localhost',
        'CACHE_REDIS_PORT': '6379',
        'CACHE_REDIS_URL': 'redis://localhost:6379',
    }
cache = Cache(app, config=config_redis)
cache.clear()


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

# app.secret_key = "5791628bb0b13ce0c676dfde280ba245"
# app.config['SECRET_KEY'] = 'top-secret!'
# app.config['SESSION_TYPE'] = 'simple'
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)

CORS(app)
# socketio = SocketIO(app)
socketio = SocketIO(app, manage_session=False)

def create_app(config_class=Config_):

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(Config_)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskapp.main.routes import main
    from flaskapp.users.routes import users
    from flaskapp.posts.routes import posts
    from flaskapp.example1.routes import example1
    from flaskapp.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(example1)
    app.register_blueprint(errors)


    return app