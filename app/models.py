from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login # Importamos la instancia que creamos arriba

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    # Rol: 'user' (empleado) o 'admin' (técnico)
    role = db.Column(db.String(20), default='user') 
    
    # Relación: Un usuario puede tener muchos tickets
    # backref permite acceder al usuario desde el ticket (ticket.author)
    # tickets = db.relationship('Ticket', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # Estados: 'Abierto', 'En Progreso', 'Cerrado'
    status = db.Column(db.String(20), default='Abierto')
    priority = db.Column(db.String(20), default='Baja')
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='ticket', lazy='dynamic')
    
    # Clave Foránea: Aquí vinculamos con la tabla User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    resolution_notes = db.Column(db.Text, nullable=True)
    cost = db.Column(db.Float, nullable=True, default=0.0)
    closed_at = db.Column(db.DateTime, nullable=True)
    author = db.relationship('User', foreign_keys=[user_id], backref='tickets', lazy=True)
    assigned_tech = db.relationship('User', foreign_keys=[assigned_to_id], backref='assigned_tickets', lazy=True)


    def __repr__(self):
        return f"Ticket('{self.title}', '{self.status}', '{self.priority}')"
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    # Relaciones
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))
    
    # Para saber quién escribió el comentario fácilmente
    author = db.relationship('User', backref='comments')