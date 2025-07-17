import unittest
from unittest.mock import MagicMock
from modules.gestor_usuario import GestorUsuarios
from modules.repositorio import RepositorioUsuariosSQLAlchemy
from modules.modelos import ModeloUsuario


class TestGestorUsuarios(unittest.TestCase):
    def setUp(self):
        """Configura el entorno para cada prueba."""
        # Mock de la sesión y el repositorio
        self.session = MagicMock()
        self.repo = RepositorioUsuariosSQLAlchemy(self.session)
        self.gestor = GestorUsuarios(self.repo)

        # Limpia la base de datos simulada
        self.session.query(ModeloUsuario).delete()

    def test_crear_usuario(self):
        """Verifica que se puede crear un usuario y recuperarlo por id."""
        usuario = ModeloUsuario(
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            nombre_de_usuario="juanperez",
            contraseña="1234",
            rol=0,
            claustro="estudiante",
        )
        self.repo.guardar_registro(usuario)
        self.session.commit.assert_called_once()

    def test_actualizar_usuario(self):
        """Verifica que se puede actualizar el nombre de usuario correctamente."""
        usuario = ModeloUsuario(
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            nombre_de_usuario="juanperez",
            contraseña="1234",
            rol=0,
            claustro="estudiante",
        )
        self.repo.guardar_registro(usuario)
        usuario.nombre = "Juan Carlos"
        self.repo.modificar_registro(usuario)
        self.session.commit.assert_called()

    def test_eliminar_usuario(self):
        """Verifica que se puede eliminar un usuario y que ya no existe."""
        usuario = ModeloUsuario(
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            nombre_de_usuario="juanperez",
            contraseña="1234",
            rol=0,
            claustro="estudiante",
        )
        self.repo.guardar_registro(usuario)
        self.repo.eliminar_registro_por_id(usuario.id)
        self.session.commit.assert_called()

    def test_buscar_usuario(self):
        """Verifica que se puede buscar un usuario por id y coincide la representación."""
        usuario = ModeloUsuario(
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            nombre_de_usuario="juanperez",
            contraseña="1234",
            rol=0,
            claustro="estudiante",
        )
        self.repo.guardar_registro(usuario)

        # Configurar el mock para devolver el usuario
        self.session.query().filter_by().first.return_value = usuario

        resultado = self.repo.obtener_modelo_por_id(usuario.id)
        self.assertEqual(resultado, usuario)

    def test_autenticar_usuario(self):
        usuario = ModeloUsuario(
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            nombre_de_usuario="juanperez",
            contraseña="1234",
            rol=0,
            claustro="estudiante",
        )
        self.repo.obtener_registro_por_filtro = MagicMock(return_value=usuario)

        resultado = self.gestor.autenticar_usuario("juanperez", "1234")

        self.assertEqual(resultado.nombre_de_usuario, "juanperez")
        self.assertEqual(resultado.nombre, "Juan")

    def test_autenticar_usuario_contraseña_incorrecta(self):
        """Verifica que no se puede autenticar un usuario con contraseña incorrecta."""
        usuario = ModeloUsuario(
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            nombre_de_usuario="juanperez",
            contraseña="1234",
            rol=0,
            claustro="estudiante",
        )
        self.repo.guardar_registro(usuario)

        # Configurar el mock para devolver el usuario
        self.session.query().filter_by().first.return_value = usuario

        with self.assertRaises(ValueError):
            self.gestor.autenticar_usuario("juanperez", "incorrecta")

    def test_autenticar_usuario_inexistente(self):
        """Verifica que no se puede autenticar un usuario inexistente."""
        # Configurar el mock para devolver None
        self.session.query().filter_by().first.return_value = None

        with self.assertRaises(ValueError):
            self.gestor.autenticar_usuario("usuario_inexistente", "1234")

if __name__ == "__main__":
    unittest.main()