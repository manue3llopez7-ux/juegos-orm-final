# models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# La clase User debe heredar de UserMixin para Flask-Login
class User(UserMixin):
    # La clase User debe tener estos atributos para ser funcional, aunque no use un ORM
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        
    def get_id(self):
        # Método requerido por Flask-Login para obtener el ID del usuario como string
        return str(self.id)

    def set_password(self, pwd):
        """Hashea la contraseña para guardarla de forma segura."""
        self.password_hash = generate_password_hash(pwd)

    def verify_password(self, pwd):
        """Verifica la contraseña ingresada contra el hash almacenado."""
        return check_password_hash(self.password_hash, pwd)
        
    # -----------------------------------------------------------
    # Métodos estáticos para simular la búsqueda de la base de datos
    # Estos son llamados por Flask-Login y las rutas
    # -----------------------------------------------------------
    @staticmethod
    def get_by_id(user_id):
        """Llama al controlador para obtener un usuario por su ID."""
        # ✅ Importación local para evitar el ciclo
        import controlador_usuarios 
        return controlador_usuarios.obtener_usuario_por_id(user_id)

    @staticmethod
    def get_by_username(username):
        """Llama al controlador para obtener un usuario por nombre de usuario."""
        import controlador_usuarios
        return controlador_usuarios.obtener_usuario_por_username(username)