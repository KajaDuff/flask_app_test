import os
from flask import Flask
from flask_cors import CORS
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from werkzeug.utils import secure_filename


db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = u'Přihlašte se prosím.'
mail = Mail()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)

    with app.app_context():
         
        from app import models

        # blueprint registration
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)
        from .home import home as home_blueprint
        app.register_blueprint(home_blueprint)
        from .user import user as user_blueprint
        app.register_blueprint(user_blueprint)

        from .errors import error as error_blueprint
        app.register_blueprint(error_blueprint)


        return app










