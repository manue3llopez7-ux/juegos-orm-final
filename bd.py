import pymysql

def obtener_conexion():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Root', # Asegúrate de que no tenga errores
        database='juegos_db',
        port=3307 # <--- ESTO ES VITAL: Le dice que use el puerto 3307
    )