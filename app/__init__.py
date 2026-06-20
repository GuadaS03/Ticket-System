from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config 

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'main.login' 

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app) 

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        from app import models
        from app.models import User
        
        db.create_all() 
        
        if not User.query.filter_by(username='admin').first():
            print("Creando usuario admin...")
            u = User(username='admin', email='admin@helpdesk.com', role='admin')
            u.set_password('123456')
            db.session.add(u)
            db.session.commit()
            print("Usuario admin creado.")
        else:
            print("El usuario admin ya existe.")

    return app