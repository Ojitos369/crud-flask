# Python
import unittest

# User
from app import create_app
from app.firestore_service import *

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


@app.route('/hello')
@login_required
def hello_world():
    todos = []
    user_ip = session.get('user_ip')
    username = current_user.id
    #users = get_users()
    if username:
        todos_res = get_todos(user_id = username)
        todos = [todo.to_dict()['description'] for todo in todos_res]
    
    
    context = {
        'todos': todos,
        'user_ip': user_ip,
        'username': username,
        'current_user': current_user,
        'cantidad_lista': len(todos)
    }
    
    
    return render_template('hello.html', **context)

# Run the app
# export FLASK_APP=main.py
# export FLASK_DEBUG=1
# export FLASK_ENV=development
# flask run

# Conect with gcloud
# gcloud init
# gcloud auth login
# gcloud auth application-default login