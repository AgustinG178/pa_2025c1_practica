import unittest
from modules.gestor_base_datos import GestorBaseDatos

class TestGestorBaseDatos(unittest.TestCase):
    def setUp(self):
        self.gestor = GestorBaseDatos('sqlite:///docs/base_datos.db')

    def test_conectar_base_datos(self):
        """Verifica que se puede conectar a la base de datos."""
        resultado = self.gestor.conectar()
        self.assertTrue(resultado)

    def test_desconectar_base_datos(self):
        """Verifica que se puede desconectar de la base de datos."""
        self.gestor.conectar()
        resultado = self.gestor.desconectar()
        self.assertTrue(resultado)

if __name__ == "__main__":
    unittest.main()