# auth/routes.py

from . import auth
from .forms import LoginForm, RegistrationForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from controlador_usuarios import obtener_usuario_por_username, insertar_usuario # Asumo que ya tienes este controlador

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('juegos'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = obtener_usuario_por_username(form.username.data)
        
        if user and user.verify_password(form.password.data):
            # Inicia la sesión
            login_user(user) 
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('juegos')) 
        else:
            flash('Credenciales inválidas. Por favor, verifica tu usuario y contraseña.', 'danger')
            
    # ✅ Llama a la plantilla usando el prefijo 'auth/'
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('juegos'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        # Lógica de verificación (debes tener implementada la verificación de unicidad en forms.py)
        hashed_password = generate_password_hash(form.password.data)
        insertar_usuario(form.username.data, hashed_password)
        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
        
    # ✅ Llama a la plantilla usando el prefijo 'auth/'
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('juegos'))