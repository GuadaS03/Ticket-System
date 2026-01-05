from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager # <--- Importamos esto
from config import Config

db = SQLAlchemy()
login = LoginManager() # <--- Inicializamos el objeto
login.login_view = 'main.login' # <--- A dónde te mando si no estás logueado

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app) # <--- Conectamos el portero a la app

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        from app import models
        db.create_all()

    return app