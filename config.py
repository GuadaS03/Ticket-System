import os

class Config:
    # 1. Clave Secreta (Usa la de Render, o una por defecto si estás en tu PC)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave_super_secreta_123'
    
    # 2. Lógica inteligente para la Base de Datos
    uri = os.environ.get('DATABASE_URL')
    
    # Si existe la variable en Render, arreglamos el prefijo si es necesario
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
        
    # Si 'uri' sigue vacía (estás en tu PC), usamos SQLite. Si tiene algo, usamos eso.
    SQLALCHEMY_DATABASE_URI = uri or 'sqlite:///site.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False