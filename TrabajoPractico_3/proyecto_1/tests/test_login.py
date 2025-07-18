import unittest
from unittest.mock import MagicMock, patch
from modules.login import FlaskLoginUser, GestorLogin
from modules.usuarios import Usuario
from modules.repositorio import RepositorioUsuariosSQLAlchemy
from modules.config import crear_engine

class DummyCurrentUser:
    def __init__(self, nombre="Juan", id=1, is_authenticated=True):
        self.nombre = nombre
        self.id = id
        self.is_authenticated = is_authenticated

class DummyRepo:
    def buscar_usuario(self, **kwargs):
        if kwargs.get("nombre_de_usuario") == "existe":
            usuario = MagicMock()
            usuario.id = 1
            usuario.nombre = "Juan"
            usuario.apellido = "Perez"
            usuario.email = "juan@x.com"
            usuario.nombre_de_usuario = "existe"
            usuario.contraseña = "1234"
            usuario.rol = 2
            usuario.claustro = "estudiante"
            return usuario
        return None

class TestFlaskLoginUser(unittest.TestCase):
    """Tests para la clase FlaskLoginUser."""

    def setUp(self):
        # Arrange
        usuario = MagicMock()
        usuario.id = 1
        usuario.nombre = "Juan"
        usuario.apellido = "Perez"
        usuario.email = "juan@x.com"
        usuario.nombre_de_usuario = "existe"
        usuario.contraseña = "1234"
        usuario.rol = 2
        usuario.claustro = "estudiante"
        self.user = FlaskLoginUser(usuario)

    def test_get_id(self):
        # Act & Assert
        self.assertEqual(self.user.get_id(), "1")

    def test_str(self):
        # Act
        s = str(self.user)
        # Assert
        self.assertIn("Juan", s)
        self.assertIn("Perez", s)

    def test_is_authenticated(self):
        # Assert
        self.assertTrue(self.user.is_authenticated)

    def test_is_active(self):
        # Assert
        self.assertTrue(self.user.is_active)

    def test_is_anonymous(self):
        # Assert
        self.assertFalse(self.user.is_anonymous)

    def test_contraseña(self):
        # Assert
        self.assertEqual(self.user.contraseña, "1234")

    def test_usuario_orm(self):
        # Assert
        self.assertIsNotNone(self.user.usuario_orm)

    def test_rol_to_dpto(self):
        # Arrange & Assert
        self.assertEqual(self.user.rol_to_dpto(), "soporte informático")
        self.user.rol = 3
        self.assertEqual(self.user.rol_to_dpto(), "secretaría técnica")
        self.user.rol = 4
        self.assertEqual(self.user.rol_to_dpto(), "maestranza")
        # Assert excepciones
        with self.assertRaises(KeyError):
            self.user.rol = 99
            self.user.rol_to_dpto()

class TestGestorLogin(unittest.TestCase):
    """Tests para la clase GestorLogin."""

    def setUp(self):
        # Arrange
        self.repo = DummyRepo()
        self.gestor = GestorLogin(self.repo)

    @patch("modules.login.current_user", new_callable=lambda: DummyCurrentUser("Juan", 42, True))
    def test_nombre_usuario_actual(self, mock_user):
        # Act & Assert
        self.assertEqual(self.gestor.nombre_usuario_actual, "Juan")

    @patch("modules.login.current_user", new_callable=lambda: DummyCurrentUser("Juan", 42, True))
    def test_id_usuario_actual(self, mock_user):
        # Act & Assert
        self.assertEqual(self.gestor.id_usuario_actual, 42)

    @patch("modules.login.current_user", new_callable=lambda: DummyCurrentUser("Juan", 42, True))
    def test_usuario_autenticado(self, mock_user):
        # Assert
        self.assertTrue(self.gestor.usuario_autenticado)

    def test_autenticar_ok(self):
        # Act
        usuario = self.gestor.autenticar("existe", "1234")
        # Assert
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nombre, "Juan")

    def test_autenticar_fail(self):
        # Act & Assert
        usuario = self.gestor.autenticar("noexiste", "1234")
        self.assertIsNone(usuario)
        usuario = self.gestor.autenticar("existe", "malpass")
        self.assertIsNone(usuario)

    @patch("modules.login.login_user")
    @patch("modules.login.current_user", new_callable=lambda: DummyCurrentUser("Juan", 1, True))
    def test_login_usuario(self, mock_user, mock_login_user):
        # Este test quedó como ejemplo, no implementado (Act & Assert si fuese implementado)
        pass

    @patch("modules.login.logout_user")
    @patch("modules.login.current_user", new_callable=lambda: DummyCurrentUser("Juan", 1, True))
    def test_logout_usuario(self, mock_user, mock_logout_user):
        # Act
        self.gestor.logout_usuario()
        # Assert
        mock_logout_user.assert_called_once()

    def test_admin_only(self):
        # Arrange
        self.gestor._GestorLogin__admin_list = [1]
        @self.gestor.admin_only
        def f():
            return "ok"
        # Act & Assert usuario admin
        with patch("modules.login.current_user", new_callable=lambda: DummyCurrentUser("Juan", 1, True)):
            self.assertEqual(f(), "ok")
        # Act & Assert usuario no admin
        with patch("modules.login.current_user", new_callable=lambda: DummyCurrentUser("Juan", 2, True)):
            with self.assertRaises(Exception):
                f()

    def test_se_requiere_login(self):
        # Arrange
        def dummy_func(): return "ok"
        # Act
        decorated = self.gestor.se_requiere_login(dummy_func)
        # Assert
        self.assertTrue(callable(decorated))

class TestLogin(unittest.TestCase):
    """Tests adicionales para autenticación."""

    def test_flask_login_user_get_id(self):
        # Arrange
        usuario = Usuario(nombre="A", apellido="B", email="a@b.com", nombre_de_usuario="ab", contraseña="123", rol=0, claustro=0, id=42)
        flask_user = FlaskLoginUser(usuario)
        # Act & Assert
        self.assertEqual(flask_user.get_id(), "42")

    def test_autenticar_falla(self):
        # Arrange
        engine, Session = crear_engine()
        session = Session()
        repo = RepositorioUsuariosSQLAlchemy(session)
        gestor = GestorLogin(repo)
        # Act & Assert
        self.assertIsNone(gestor.autenticar("noexiste", "malpass"))

if __name__ == "__main__":
    unittest.main()
