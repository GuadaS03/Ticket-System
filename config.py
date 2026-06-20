import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave_super_secreta_123'
    
    uri = os.environ.get('DATABASE_URL')
    
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
        

    SQLALCHEMY_DATABASE_URI = uri or 'sqlite:///site.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False