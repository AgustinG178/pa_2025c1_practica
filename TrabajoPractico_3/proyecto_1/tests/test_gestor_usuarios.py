import unittest
from unittest.mock import MagicMock
from modules.gestor_usuario import GestorUsuarios
from modules.repositorio import RepositorioUsuariosSQLAlchemy
from modules.modelos import ModeloUsuario


class TestGestorUsuarios(unittest.TestCase):
    def setUp(self):
        """Configura el entorno para cada prueba."""
        # Arrange
        self.session = MagicMock()
        self.repo = RepositorioUsuariosSQLAlchemy(self.session)
        self.gestor = GestorUsuarios(self.repo)

        # Limpia la base de datos simulada
        self.session.query(ModeloUsuario).delete()

    def test_crear_usuario(self):
        # Arrange
        usuario = ModeloUsuario(
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            nombre_de_usuario="juanperez",
            contraseña="1234",
            rol=0,
            claustro="estudiante",
        )
        # Act
        self.repo.guardar_registro(usuario)
        # Assert
        self.session.commit.assert_called_once()

    def test_actualizar_usuario(self):
        # Arrange
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
        # Act
        self.repo.modificar_registro(usuario)
        # Assert
        self.session.commit.assert_called()

    def test_eliminar_usuario(self):
        # Arrange
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
        # Act
        self.repo.eliminar_registro_por_id(usuario.id)
        # Assert
        self.session.commit.assert_called()

    def test_buscar_usuario(self):
        # Arrange
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
        # Act
        resultado = self.repo.obtener_modelo_por_id(usuario.id)
        # Assert
        self.assertEqual(resultado, usuario)

    def test_autenticar_usuario(self):
        # Arrange
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
        # Act
        resultado = self.gestor.autenticar_usuario("juanperez", "1234")
        # Assert
        self.assertEqual(resultado.nombre_de_usuario, "juanperez")
        self.assertEqual(resultado.nombre, "Juan")

    def test_autenticar_usuario_contraseña_incorrecta(self):
        # Arrange
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
        self.session.query().filter_by().first.return_value = usuario
        # Act & Assert
        with self.assertRaises(ValueError):
            self.gestor.autenticar_usuario("juanperez", "incorrecta")

    def test_autenticar_usuario_inexistente(self):
        # Arrange
        self.session.query().filter_by().first.return_value = None
        # Act & Assert
        with self.assertRaises(ValueError):
            self.gestor.autenticar_usuario("usuario_inexistente", "1234")


if __name__ == "__main__":
    unittest.main()
