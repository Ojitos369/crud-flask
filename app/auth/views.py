
from flask import render_template, session, flash, redirect, url_for
from . import auth
from app.forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login = LoginForm()
    context = {
        'login_form': login
    }
    
    if login.validate_on_submit():
        username = login.username.data
        password = login.password.data
        session['username'] = username
        flash('Login Successful')
        return redirect(url_for('hello_world'))
    
    return render_template('auth/login.html', **context)