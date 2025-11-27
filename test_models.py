import unittest
from models import User

class UserModelTestCase(unittest.TestCase):
    def test_password_hashing(self):
        """Prueba que la contraseña se hashea correctamente."""
        u = User(id=1, username='testuser', password_hash=None)
        u.set_password('cat')
        
        self.assertFalse(u.verify_password('dog'))
        self.assertTrue(u.verify_password('cat'))
        self.assertNotEqual(u.password_hash, 'cat') # El hash no debe ser texto plano

if __name__ == '__main__':
    unittest.main()