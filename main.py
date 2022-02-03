from ensurepip import bootstrap
from flask import Flask, request, make_response, redirect, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

todos = ['Task 1', 'Task 2', 'Task 3']

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
    response.set_cookie('user_ip', user_ip)
    return response


@app.route('/hello')
def hello_world():
    user_ip = request.cookies.get('user_ip')
    context = {
        'todos': todos,
        'user_ip': user_ip
    }
    return render_template('hello.html', **context)

# Run the app
# export FLASK_APP=main.py
# export FLASK_DEBUG=1
# flask run