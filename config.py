import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una_clave_muy_secreta_para_desarrollo'
    
    # Obtenemos la URL de la base de datos
    uri = os.environ.get('DATABASE_URL')
    
    # CORRECCIÓN PARA RENDER:
    # Si la URL existe y empieza con postgres://, la cambiamos a postgresql://
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = uri or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False