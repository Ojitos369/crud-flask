from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import unittest

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'SUPER SECRET'

todos = ['Task 1', 'Task 2', 'Task 3']

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


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


@app.route('/hello', methods=['GET', 'POST'])
def hello_world():
    login = LoginForm()
    user_ip = session.get('user_ip')
    username = session.get('username')
    context = {
        'todos': todos,
        'user_ip': user_ip,
        'login': login,
        'username': username
    }
    
    if login.validate_on_submit():
        username = login.username.data
        password = login.password.data
        session['username'] = username
        flash('Login Successful')
        return redirect(url_for('hello_world'))
    return render_template('hello.html', **context)

# Run the app
# export FLASK_APP=main.py
# export FLASK_DEBUG=1
# export FLASK_ENV=development
# flask run