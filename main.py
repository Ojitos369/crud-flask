from flask import request, make_response, redirect, render_template, session, url_for, flash
import unittest
from app import create_app
from app.forms import LoginForm

app = create_app()

todos = ['Task 1', 'Task 2', 'Task 3']


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
def home():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
    return response


@app.route('/hello')
def hello_world():
    user_ip = session.get('user_ip')
    username = session.get('username')
    context = {
        'todos': todos,
        'user_ip': user_ip,
        'username': username
    }
    
    
    return render_template('hello.html', **context)

# Run the app
# export FLASK_APP=main.py
# export FLASK_DEBUG=1
# export FLASK_ENV=development
# flask run