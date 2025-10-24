from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Importaciones de Módulos (Deben ir al inicio)
from models import User 
from auth.routes import auth as auth_bp
import controlador_juegos 

# --- 1. Inicialización de la Aplicación y Configuración ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'CLAVE_SECRETA_SOLIDA_AQUI_12345'

# --- Configuración de Flask-Login ---
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'

@login_manager.user_loader
def load_user(user_id):
    # Llama al método estático de la clase User para obtener el usuario
    return User.get_by_id(int(user_id)) 

# --- Registro de Blueprints (Debe hacerse UNA SOLA VEZ) ---
app.register_blueprint(auth_bp, url_prefix='/auth')

# --- 2. Rutas de la Aplicación (Juegos) ---

@app.route("/")
@app.route("/juegos")
def juegos():
    juegos = controlador_juegos.obtener_juegos()
    return render_template("juegos.html", juegos=juegos)

@app.route("/agregar_juego")
@login_required # Protege esta ruta
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
@login_required # Protege esta ruta
def guardar_juego():
    titulo = request.form["titulo"]
    genero = request.form["genero"]
    plataforma = request.form["plataforma"]
    precio = request.form["precio"]
    
    controlador_juegos.insertar_juego(titulo, genero, plataforma, precio)
    flash("Juego agregado correctamente.", "success")
    return redirect(url_for('juegos'))

@app.route("/eliminar_juego", methods=["POST"])
@login_required # Protege esta ruta
def eliminar_juego():
    id_juego = request.form["id"]
    controlador_juegos.eliminar_juego(id_juego)
    flash("Juego eliminado correctamente.", "danger")
    return redirect(url_for('juegos'))

@app.route("/formulario_editar_juego/<int:id>")
@login_required # Protege esta ruta
def formulario_editar_juego(id):
    juego = controlador_juegos.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)

@app.route("/actualizar_juego", methods=["POST"])
@login_required # Protege esta ruta
def actualizar_juego():
    id_juego = request.form["id"]
    titulo = request.form["titulo"]
    genero = request.form["genero"]
    plataforma = request.form["plataforma"]
    precio = request.form["precio"]
    
    controlador_juegos.actualizar_juego(titulo, genero, plataforma, precio, id_juego)
    flash("Juego actualizado correctamente.", "success")
    return redirect(url_for('juegos'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)