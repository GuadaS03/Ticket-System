from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FloatField
from wtforms.validators import DataRequired, Optional

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Ingresar')

class TicketForm(FlaskForm):
    title = StringField('Asunto', validators=[DataRequired()])
    description = TextAreaField('Descripción del problema', validators=[DataRequired()])
    priority = SelectField('Prioridad', choices=[
        ('Baja', 'Baja'), 
        ('Media', 'Media'), 
        ('Alta', 'Alta'), 
        ('Critica', 'Crítica')
    ])
    submit = SubmitField('Crear Ticket')

class CommentForm(FlaskForm):
    body = TextAreaField('Nuevo Comentario', validators=[DataRequired()])
    submit = SubmitField('Comentar')

class EditTicketForm(FlaskForm):
    status = SelectField('Estado', choices=[('Abierto', 'Abierto'), ('En Progreso', 'En Progreso'), ('Cerrado', 'Cerrado')])
    priority = SelectField('Prioridad', choices=[('Baja', 'Baja'), ('Media', 'Media'), ('Alta', 'Alta'), ('Crítica', 'Crítica')])
    assigned_to = SelectField('Asignado a', coerce=int, choices=[]) 
    resolution_notes = TextAreaField('Notas de Resolución')
    cost = FloatField('Costo ($)', validators=[Optional()], default=0.0) 
    submit = SubmitField('Actualizar Ticket')