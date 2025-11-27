import unittest
from app import app

class APITestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_get_juegos(self):
        """Prueba obtener la lista de juegos."""
        response = self.client.get('/api/juegos')
        self.assertEqual(response.status_code, 200)
        # Verifica que la respuesta sea JSON
        self.assertTrue(response.is_json)

    def test_get_juego_404(self):
        """Prueba obtener un juego que no existe."""
        # Asumimos que el ID 99999 no existe
        response = self.client.get('/api/juegos/99999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()