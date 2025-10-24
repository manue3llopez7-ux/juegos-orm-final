# auth/__init__.py

from flask import Blueprint
auth = Blueprint('auth', __name__, template_folder='templates', url_prefix='/auth')

from . import routes # Importa las rutas del Blueprint