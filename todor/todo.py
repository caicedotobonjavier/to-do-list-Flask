from flask import Blueprint, g
#
from flask import render_template, request, redirect, url_for
#
from todor.auth import login_required
#
from .models import Todo, User
#
from flask import session
#
from todor import db

bp = Blueprint('todo', __name__, url_prefix='/todo')


@bp.route('/lista')
@login_required
def index():
    usuario = session.get('user_id')
    print(usuario)
    tareas = Todo.query.filter_by(user=usuario).all()
    return render_template('todo/index.html', tareas=tareas)

@bp.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method=='POST':
        tarea = Todo(
            title=request.form['title'],
            description=request.form['description'],
            user=session.get('user_id')
        )
        db.session.add(tarea)
        db.session.commit()

        return redirect(url_for('todo.index'))

    return render_template('todo/create.html')


def get_tarea(id):
    tarea = Todo.query.get_or_404(id)
    return tarea

@bp.route('/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update(id):
    tarea = get_tarea(id)
    if request.method=='POST':
        tarea.title = request.form['title']
        tarea.description = request.form['description']
        tarea.status = True if request.form.get('status')=='on' else False

        db.session.commit()
        return redirect(url_for('todo.index'))
    
    return render_template('todo/update.html', tarea=tarea)

@bp.route('/delete/<int:id>/')
def delete(id):
    tarea = get_tarea(id)
    db.session.delete(tarea)
    db.session.commit()

    return redirect(url_for('todo.index'))