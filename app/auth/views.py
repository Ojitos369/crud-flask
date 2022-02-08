
from multiprocessing import context
from flask import render_template, session, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth
from app.firestore_service import get_user, create_user
from app.forms import LoginForm, SignupForm
from app.models import UserData, User

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login = LoginForm()
    context = {
        'login_form': login,
        'flash_errors': False
    }
    
    if login.validate_on_submit():
        import os
        os.system('clear')
        username = login.username.data
        password = login.password.data
        
        user_doc = get_user(username)
        print(user_doc.id)
        if user_doc.to_dict() is not None:
            pass_from_db = user_doc.to_dict()['password']
            
            if check_password_hash(pass_from_db, password):
                user_data = UserData(username, password)
                user = User(user_data)
                login_user(user)
                
                flash('Bienvenido de nuevo')
                return redirect(url_for('hello_world'))
            else:
                flash('Los datos no coinciden')
                context['flash_errors'] = True
        else:
            flash('El usuario no existe')
            context['flash_errors'] = True
    
    return render_template('auth/login.html', **context)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada')
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    context = {
        'signup_form': signup_form,
        'flash_errors': True
    }
    
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data
        
        user_doc = get_user(username)
        if user_doc.to_dict() is not None:
            flash('El usuario ya existe')
            context['flash_errors'] = True
        else:
            context['flash_errors'] = False
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            create_user(user_data)
    
    if context['flash_errors']:
        return render_template('auth/signup.html', **context)
    else:
        flash('Usuario creado')
        return redirect(url_for('auth.login'))


