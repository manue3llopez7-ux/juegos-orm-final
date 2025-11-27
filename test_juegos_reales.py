import unittest
import json
# Importamos TU aplicación real, no la calculadora del video
from app import create_app, db
from models import Juego

class TestJuegosAPI(unittest.TestCase):

    # setUp: Se ejecuta ANTES de cada prueba (Igual que en el video)
    # Aquí configuramos una base de datos vacía y temporal para no borrar tus datos reales
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Base de datos en memoria (RAM) para pruebas rápidas
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()

    # tearDown: Se ejecuta DESPUÉS de cada prueba (Igual que en el video)
    # Aquí borramos todo para que la siguiente prueba empiece limpia
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # Prueba 1: Verificar que la lista de juegos empieza vacía
    def test_get_juegos_vacio(self):
        response = self.client.get('/api/juegos')
        self.assertEqual(response.status_code, 200) # Usamos assertEqual como en el video
        self.assertEqual(response.json, [])

    # Prueba 2: Verificar que podemos crear un juego
    def test_crear_juego(self):
        nuevo_juego = {
            "titulo": "Super Mario Test",
            "genero": "Plataforma",
            "plataforma": "Switch",
            "precio": 59.99
        }
        
        # Enviamos una petición POST (similar a usar Postman o Curl)
        response = self.client.post('/api/juegos', 
                                    data=json.dumps(nuevo_juego),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['titulo'], "Super Mario Test")

if __name__ == "__main__":
    unittest.main()