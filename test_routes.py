import unittest
from app import app

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        """Configura el cliente de pruebas antes de cada test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False # Desactiva CSRF para facilitar pruebas
        self.client = app.test_client()

    def test_index_page(self):
        """Prueba que la página de inicio carga correctamente."""
        response = self.client.get('/')
        # Debería devolver 200 OK o 302 (redirección si hay lógica de auth)
        self.assertTrue(response.status_code in [200, 302])

    def test_login_page_loads(self):
        """Prueba que la página de login carga."""
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Iniciar Sesión'.encode('utf-8'), response.data)
if __name__ == '__main__':
    unittest.main()