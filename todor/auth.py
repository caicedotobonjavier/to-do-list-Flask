from flask import Blueprint
#
from flask import render_template, request, url_for, redirect, flash, session, g
#
from werkzeug.security import generate_password_hash, check_password_hash
#
from .models import User
#
from todor import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario = User(
            username=username,
            password=generate_password_hash(password)   
        )

        error = None

        user_name = User.query.filter_by(username=username).first()
        if user_name:
            error = f'El usuario {username} ya existe'
            flash(error)
            return redirect(url_for('auth.register'))
        else:
            db.session.add(usuario)
            db.session.commit()
            flash(f'Usuario {username} registrado correctamente')

            return redirect (url_for('auth.login'))

    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        usuario = User.query.filter_by(username=username).first()
        if usuario:
            if check_password_hash(usuario.password, password):
                session.clear()
                session['user_id'] = usuario.id         
                
                return redirect(url_for('todo.index'))
            
            elif not check_password_hash(usuario.password, password):
                flash('Usuario o contraseña incorrectos')

                return redirect(url_for('auth.login'))
            
        elif not usuario:
            flash('Usuario o contraseña incorrectos')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')


#mantener el inicio de sesion
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


#vista que requiere sesion
import functools
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view