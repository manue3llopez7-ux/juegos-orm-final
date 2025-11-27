import logging
from logging import FileHandler
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException, BadRequest, MethodNotAllowed

# --- 1. Importaciones de Sentry ---
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# --- 2. Importaciones de tu Proyecto ---
from models import User 
from auth.routes import auth as auth_bp
import controlador_juegos 
# controlador_usuarios se usa dentro de models.py, pero importarlo aquí asegura que esté disponible
import controlador_usuarios 
from api.resources import JuegoList, JuegoResource
from flask_restful import Api

# --- 3. Configuración de Sentry ---
sentry_sdk.init(
    dsn="https://c4a49b3e4d0a53d04bd28e83b48106e9@o4510318598356992.ingest.us.sentry.io/4510318638465024",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)

# --- 4. Inicialización de la Aplicación y Configuración ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'CLAVE_SECRETA_SOLIDA_AQUI_12345' 
api = Api(app) 

# --- 5. Configuración del Logger de Archivos ---
file_handler = FileHandler('errors.log')
file_handler.setLevel(logging.ERROR) 
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(file_handler)

# --- 6. Configuración de Flask-Login ---
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id)) 

# --- 7. Registro de Blueprints y API ---
app.register_blueprint(auth_bp, url_prefix='/auth')
api.add_resource(JuegoList, '/api/juegos')
api.add_resource(JuegoResource, '/api/juegos/<int:id>')

# --- 8. Manejadores de Errores (Lógica Centralizada) ---
# 

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """
    Manejador único que decide si devolver JSON (para API) o HTML (para Web).
    """
    
    # 1. Si la ruta empieza con /api/, devolvemos JSON
    if request.path.startswith('/api/'):
        response = e.get_response()
        response.data = jsonify({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }).data
        response.content_type = "application/json"
        return response
    
    # 2. Si no es API, devolvemos las plantillas HTML personalizadas
    if e.code == 400:
        return render_template('400.html'), 400
    if e.code == 404:
        return render_template('404.html'), 404
    if e.code == 405:
        return render_template('405.html'), 405
    if e.code == 500:
        return render_template('500.html'), 500

    # Para cualquier otro error HTTP no específico, devolvemos el error estándar
    return e

# --- 9. Rutas de la Aplicación Web (Juegos) ---

@app.route("/")
@app.route("/juegos")
def juegos():
    juegos = controlador_juegos.obtener_juegos()
    return render_template("juegos.html", juegos=juegos)

@app.route("/agregar_juego")
@login_required 
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
@login_required 
def guardar_juego():
    titulo = request.form["titulo"]
    genero = request.form["genero"]
    plataforma = request.form["plataforma"]
    precio = request.form["precio"]
    
    controlador_juegos.insertar_juego(titulo, genero, plataforma, precio)
    flash("Juego agregado correctamente.", "success")
    return redirect(url_for('juegos'))

@app.route("/eliminar_juego", methods=["POST"])
@login_required 
def eliminar_juego():
    id_juego = request.form["id"]
    controlador_juegos.eliminar_juego(id_juego)
    flash("Juego eliminado correctamente.", "danger")
    return redirect(url_for('juegos'))

@app.route("/formulario_editar_juego/<int:id>")
@login_required 
def formulario_editar_juego(id):
    juego = controlador_juegos.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)

@app.route("/actualizar_juego", methods=["POST"])
@login_required 
def actualizar_juego():
    id_juego = request.form["id"]
    titulo = request.form["titulo"]
    genero = request.form["genero"]
    plataforma = request.form["plataforma"]
    precio = request.form["precio"]
    
    controlador_juegos.actualizar_juego(titulo, genero, plataforma, precio, id_juego)
    flash("Juego actualizado correctamente.", "success")
    return redirect(url_for('juegos'))

# --- 10. Rutas de Prueba para Errores ---

@app.route("/test_400")
def test_400():
    # Fuerza un error 400 Bad Request
    abort(400)

@app.route("/test_500")
def test_500():
    # Fuerza un error 500 (División por cero) para probar Sentry y Logs
    x = 1 / 0
    return "Esto no se verá"

if __name__ == '__main__':
    app.run(debug=True, port=8000)