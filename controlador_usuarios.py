# controlador_usuarios.py

from bd import obtener_conexion # Función que devuelve la conexión PyMySQL
from werkzeug.security import generate_password_hash # Necesario para el registro

# Importamos la clase User de forma diferida en las funciones

def obtener_usuario_por_id(user_id):
    """Busca un usuario por ID (usado por Flask-Login)."""
    # ✅ Importación diferida
    from models import User 
    
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        # Nota: Debes asegurar que tu tabla se llame 'users' y tenga los campos 'id', 'username', 'password_hash'
        cursor.execute("SELECT id, username, password_hash FROM users WHERE id = %s", (user_id,))
        datos = cursor.fetchone()
    conexion.close()
    
    if datos:
        # Creamos una instancia del objeto User con los datos de la tupla
        return User(id=datos[0], username=datos[1], password_hash=datos[2])
    return None

def obtener_usuario_por_username(username):
    """Busca un usuario por nombre de usuario (usado para el Login)."""
    # ✅ Importación diferida
    from models import User
    
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, username, password_hash FROM users WHERE username = %s", (username,))
        datos = cursor.fetchone()
    conexion.close()
    
    if datos:
        return User(id=datos[0], username=datos[1], password_hash=datos[2])
    return None

def insertar_usuario(username, password):
    """Inserta un nuevo usuario en la base de datos después de hashear la contraseña."""
    
    # Hasheamos la contraseña antes de guardar (el modelo User lo haría, pero aquí lo hacemos antes de la inserción)
    password_hash = generate_password_hash(password)
    
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                       (username, password_hash))
    conexion.commit()
    conexion.close()

# 🚨 NOTA: Las rutas de tu Blueprint (auth/routes.py) y app.py deben ahora llamar
# a los métodos estáticos User.get_by_id() y User.get_by_username() en lugar de llamar directamente
# a las funciones del controlador. Por ejemplo, en el login:
# user = User.get_by_username(form.username.data)