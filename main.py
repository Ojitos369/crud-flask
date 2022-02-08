# Python
import unittest

# User
from app import create_app
from app.firestore_service import *
from app.forms import TodoForm, TodoUpdateForm

# Flask
from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_login import login_required, current_user

app = create_app()

#todos = ['Task 1', 'Task 2', 'Task 3']


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

# error 404
@app.errorhandler(404)
def error(error):
    return render_template('error/404.html', error = error)

# error 500
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error/500.html', error = error)


@app.route('/')
@login_required
def home():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
    return response


@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello_world():
    todos = []
    user_ip = session.get('user_ip')
    username = current_user.id
    form = TodoForm()
    todo_update = TodoUpdateForm()
    #users = get_users()
    if username:
        todos_res = get_todos(user_id = username)
        for todo in todos_res:
            todo_dict = todo.to_dict()
            todo_dict['id'] = todo.id
            todos.append(todo_dict)
    
    context = {
        'todos': todos,
        'user_ip': user_ip,
        'username': username,
        'current_user': current_user,
        'cantidad_lista': len(todos),
        'form': form,
        'todo_update': todo_update
    }
    
    if form.validate_on_submit():
        description = form.description.data
        create_todo(user_id = username, description = description)
        flash('Tarea agregada')
        return redirect(url_for('hello_world'))
    
    
    return render_template('hello.html', **context)

@app.route('/todo/delete/<todo_id>', methods=['GET', 'POST'])
@login_required
def delete(todo_id):
    username = current_user.id
    delete_todo(user_id = username, todo_id = todo_id)
    flash('Tarea eliminada')
    return redirect(url_for('hello_world'))

@app.route('/todo/toggle/<todo_id>', methods=['GET', 'POST'])
@login_required
def toggle(todo_id):
    username = current_user.id
    todo_toggle(user_id = username, todo_id = todo_id)
    flash('Cambio de estado')
    return redirect(url_for('hello_world'))

@app.route('/todo/update/<todo_id>', methods=['GET', 'POST'])
@login_required
def update(todo_id):
    username = current_user.id
    description = request.form['description']
    update_todo(user_id = username, todo_id = todo_id, description = description)
    flash('Tarea actualizada')
    return redirect(url_for('hello_world'))

# Run the app
"""
export FLASK_APP=main.py
export FLASK_DEBUG=1
export FLASK_ENV=development
flask run
"""

# Conect with gcloud
"""
gcloud init
gcloud auth login
gcloud auth application-default login
"""

# Deploy to gcloud
"""
gcloud app deploy app.yaml
"""