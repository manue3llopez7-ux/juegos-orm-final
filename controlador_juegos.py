from bd import obtener_conexion # Función que devuelve la conexión PyMySQL

def insertar_juego(titulo, genero, plataforma, precio):
    """Inserta un nuevo juego en la base de datos."""
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        # Los campos SQL deben coincidir con las variables
        cursor.execute("INSERT INTO juegos(titulo, genero, plataforma, precio) VALUES (%s, %s, %s, %s)",
                       (titulo, genero, plataforma, precio))
    conexion.commit()
    conexion.close()

def obtener_juegos():
    """Obtiene todos los juegos registrados."""
    conexion = obtener_conexion()
    juegos = []
    with conexion.cursor() as cursor:
        # Selecciona todos los campos de la tabla para listar
        cursor.execute("SELECT id, titulo, genero, plataforma, precio FROM juegos")
        juegos = cursor.fetchall()
    conexion.close()
    return juegos

def eliminar_juego(id_juego):
    """Elimina un juego por su ID."""
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM juegos WHERE id = %s", (id_juego,))
    conexion.commit()
    conexion.close()

def obtener_juego_por_id(id):
    """Obtiene un juego específico por su ID."""
    conexion = obtener_conexion()
    juego = None
    with conexion.cursor() as cursor:
        # Selecciona todos los campos para la edición
        cursor.execute("SELECT id, titulo, genero, plataforma, precio FROM juegos WHERE id = %s", (id,))
        juego = cursor.fetchone() # Devuelve una sola tupla
    conexion.close()
    return juego

def actualizar_juego(titulo, genero, plataforma, precio, id_juego):
    """Actualiza la información de un juego por su ID."""
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        # La sentencia UPDATE debe cubrir todos los campos
        cursor.execute("UPDATE juegos SET titulo = %s, genero = %s, plataforma = %s, precio = %s WHERE id = %s",
                       (titulo, genero, plataforma, precio, id_juego))
    conexion.commit()
    conexion.close()