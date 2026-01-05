import os

# ... resto del código ...

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu_clave_secreta'
    
    # ESTA ES LA LÍNEA MÁGICA:
    # Busca la variable 'DATABASE_URL' (la de Render). 
    # Si no la encuentra, usa 'sqlite:///site.db' (tu PC).
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Parche para Render (a veces la URL empieza con postgres:// y debe ser postgresql://)
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)