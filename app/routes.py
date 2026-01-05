from flask import Blueprint, render_template, flash, redirect, url_for, abort, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.models import User, Ticket, Comment
from app.forms import LoginForm, TicketForm, CommentForm

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return render_template('index.html', title='Dashboard', tickets=tickets)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o contraseña inválidos')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Ingreso', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/ticket/new', methods=['GET', 'POST'])
@login_required
def create_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            title=form.title.data, 
            description=form.description.data,
            priority=form.priority.data,
            author=current_user
        )
        db.session.add(ticket)
        db.session.commit()
        flash('¡Ticket creado exitosamente!')
        return redirect(url_for('main.index'))
    return render_template('create_ticket.html', title='Nuevo Ticket', form=form)

# --- ESTA ES LA ÚNICA VERSIÓN QUE DEBE EXISTIR DE TICKET_DETAIL ---
@main.route('/ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    form = CommentForm()
    
    if ticket.author != current_user and current_user.role != 'admin':
        abort(403)
    
    if form.validate_on_submit():
        comment = Comment(
            body=form.body.data,
            ticket=ticket,
            author=current_user
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comentario agregado')
        return redirect(url_for('main.ticket_detail', ticket_id=ticket.id))

    if request.method == 'POST' and 'status' in request.form and current_user.role == 'admin':
        new_status = request.form.get('status')
        ticket.status = new_status
        db.session.commit()
        flash(f'Estado actualizado a: {new_status}')
        return redirect(url_for('main.ticket_detail', ticket_id=ticket.id))

    comments = ticket.comments.order_by(Comment.created_at.desc()).all()
    
    return render_template('ticket_detail.html', 
                           title=f'Ticket #{ticket.id}', 
                           ticket=ticket, 
                           form=form, 
                           comments=comments)