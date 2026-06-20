import os
from app import create_app, db
from app.models import User

# 1. Creamos la app
app = create_app()

# 2. Leemos la URL desde las variables de entorno de Render
db_url = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

# 3. Entramos al contexto de la app
with app.app_context():
    print("--- CONECTANDO A LA NUBE ---")
    
    # Crear las tablas
    print("1. Creando tablas...")
    db.create_all()
    print("Tablas listas.")

    # Crear el usuario
    print("2. Verificando usuario Admin...")
    if not User.query.filter_by(username='admin').first():
        u = User(username='admin', email='admin@helpdesk.com', role='admin')
        u.set_password('123456')
        db.session.add(u)
        db.session.commit()
        print("¡USUARIO ADMIN CREADO EN LA NUBE!")
    else:
        print("ℹ El usuario admin ya existía en la nube.")

    print("--- FIN DEL PROCESO ---")