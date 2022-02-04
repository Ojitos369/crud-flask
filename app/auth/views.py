from . import auth
from flask import render_template
from app.forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    context = {
        'login_form': LoginForm()
    }
    
    return render_template('auth/login.html', **context)