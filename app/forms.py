from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms import TextAreaField, SelectField

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