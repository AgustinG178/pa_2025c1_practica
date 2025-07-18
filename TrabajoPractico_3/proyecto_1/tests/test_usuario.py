import unittest
from modules.usuarios import Usuario  

class TestUsuario(unittest.TestCase):
    """Tests para la clase Usuario."""

    def setUp(self):
        """Configura un usuario para los tests."""
        self.usuario = Usuario(
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            nombre_de_usuario="jperez",
            contraseña="secreto123",
            rol="admin",
            claustro="docente",
            id=1
        )

    def test_getters(self):
        """Verifica que los getters retornan los valores correctos."""
        self.assertEqual(self.usuario.nombre, "Juan")
        self.assertEqual(self.usuario.apellido, "Pérez")
        self.assertEqual(self.usuario.email, "juan.perez@example.com")
        self.assertEqual(self.usuario.nombre_de_usuario, "jperez")
        self.assertEqual(self.usuario.contraseña, "secreto123")
        self.assertEqual(self.usuario.rol, "admin")
        self.assertEqual(self.usuario.claustro, "docente")
        self.assertEqual(self.usuario.id, 1)

    def test_setters(self):
        """Verifica que los setters actualizan correctamente los atributos."""
        self.usuario.nombre = "Carlos"
        self.assertEqual(self.usuario.nombre, "Carlos")

        self.usuario.apellido = "Gómez"
        self.assertEqual(self.usuario.apellido, "Gómez")

        self.usuario.email = "carlos.gomez@example.com"
        self.assertEqual(self.usuario.email, "carlos.gomez@example.com")

        self.usuario.nombre_de_usuario = "cgomez"
        self.assertEqual(self.usuario.nombre_de_usuario, "cgomez")

        self.usuario.contraseña = "nuevo123"
        self.assertEqual(self.usuario.contraseña, "nuevo123")

        self.usuario.rol = "usuario"
        self.assertEqual(self.usuario.rol, "usuario")

        self.usuario.claustro = "estudiante"
        self.assertEqual(self.usuario.claustro, "estudiante")

    def test_str(self):
        """Verifica la representación __str__ del usuario."""
        self.assertIn("Juan", str(self.usuario))

    def test_id_lectura(self):
        """Verifica que se puede leer el id pero no modificarlo (solo lectura)."""
        self.assertEqual(self.usuario.id, 1)
        with self.assertRaises(AttributeError):
            self.usuario.id = 2  # Debe lanzar error porque no tiene setter

if __name__ == "__main__": #pragma: no cover
    unittest.main()
