
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flaskapp.config_ import Config_


db = SQLAlchemy()

def create_app(config_class=Config_):
    app = Flask(__name__)
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(Config_)
    db.init_app(app)

    from flaskapp.main.routes import main
    from flaskapp.users.routes import users
    from flaskapp.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(errors)


    return app