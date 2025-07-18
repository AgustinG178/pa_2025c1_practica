import unittest
from modules.gestor_base_datos import GestorBaseDatos

class TestGestorBaseDatos(unittest.TestCase):
    def setUp(self):
        # Arrange: Configuración inicial para los tests
        self.gestor = GestorBaseDatos('sqlite:///docs/base_datos.db')

    def test_conectar_base_datos(self):
        """Verifica que se puede conectar a la base de datos."""
        # Arrange: No se requiere configuración adicional, ya está en setUp

        # Act: Llamar al método que se desea probar
        resultado = self.gestor.conectar()

        # Assert: Verificar que el resultado sea el esperado
        self.assertTrue(resultado)

    def test_desconectar_base_datos(self):
        """Verifica que se puede desconectar de la base de datos."""
        # Arrange: Conectar a la base de datos antes de desconectar
        self.gestor.conectar()

        # Act: Llamar al método que se desea probar
        resultado = self.gestor.desconectar()

        # Assert: Verificar que el resultado sea el esperado
        self.assertTrue(resultado)

if __name__ == "__main__":
    unittest.main()