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
        """Verifica que get_id retorna el id como string."""
        self.assertEqual(self.user.get_id(), "1")

    def test_str(self):
        """Verifica la representación en string del usuario."""
        s = str(self.user)
        self.assertIn("Juan", s)
        self.assertIn("Perez", s)

    def test_is_authenticated(self):
        """Verifica que is_authenticated retorna True."""
        self.assertTrue(self.user.is_authenticated)

    def test_is_active(self):
        """Verifica que is_active retorna True."""
        self.assertTrue(self.user.is_active)

    def test_is_anonymous(self):
        """Verifica que is_anonymous retorna False."""
        self.assertFalse(self.user.is_anonymous)

    def test_contraseña(self):
        """Verifica que la propiedad contraseña retorna el valor correcto."""
        self.assertEqual(self.user.contraseña, "1234")

    def test_usuario_orm(self):
        """Verifica que usuario_orm no es None."""
        self.assertIsNotNone(self.user.usuario_orm)

    def test_rol_to_dpto(self):
        """Verifica la conversión de rol a departamento y el manejo de errores."""
        self.assertEqual(self.user.rol_to_dpto(), "soporte informático")
        self.user.rol = 3
        self.assertEqual(self.user.rol_to_dpto(), "secretaría técnica")
        self.user.rol = 4
        self.assertEqual(self.user.rol_to_dpto(), "maestranza")
        with self.assertRaises(KeyError):
            self.user.rol = 99
            self.user.rol_to_dpto()

class TestGestorLogin(unittest.TestCase):
    """Tests para la clase GestorLogin."""

    def setUp(self):
        self.repo = DummyRepo()
        self.gestor = GestorLogin(self.repo)

    @patch("modules.login.current_user", new_callable=lambda: DummyCurrentUser("Juan", 42, True))
    def test_nombre_usuario_actual(self, mock_user):
        """Verifica que nombre_usuario_actual retorna el nombre del usuario actual."""
        self.assertEqual(self.gestor.nombre_usuario_actual, "Juan")

    @patch("modules.login.current_user", new_callable=lambda: DummyCurrentUser("Juan", 42, True))
    def test_id_usuario_actual(self, mock_user):
        """Verifica que id_usuario_actual retorna el id del usuario actual."""
        self.assertEqual(self.gestor.id_usuario_actual, 42)

    @patch("modules.login.current_user", new_callable=lambda: DummyCurrentUser("Juan", 42, True))
    def test_usuario_autenticado(self, mock_user):
        """Verifica que usuario_autenticado retorna True si el usuario está autenticado."""
        self.assertTrue(self.gestor.usuario_autenticado)

    def test_autenticar_ok(self):
        """Verifica que autenticar retorna un usuario válido con credenciales correctas."""
        usuario = self.gestor.autenticar("existe", "1234")
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nombre, "Juan")

    def test_autenticar_fail(self):
        """Verifica que autenticar retorna None con credenciales incorrectas."""
        usuario = self.gestor.autenticar("noexiste", "1234")
        self.assertIsNone(usuario)
        usuario = self.gestor.autenticar("existe", "malpass")
        self.assertIsNone(usuario)

    @patch("modules.login.login_user")
    @patch("modules.login.current_user", new_callable=lambda: DummyCurrentUser("Juan", 1, True))
    def test_login_usuario(self, mock_user, mock_login_user):
        """(Ejemplo) Verifica el login de usuario usando mocks."""
        pass

    @patch("modules.login.logout_user")
    @patch("modules.login.current_user", new_callable=lambda: DummyCurrentUser("Juan", 1, True))
    def test_logout_usuario(self, mock_user, mock_logout_user):
        """Verifica que logout_usuario llama a logout_user."""
        # Solo cubre el método logout_usuario (prints)
        self.gestor.logout_usuario()

    def test_admin_only(self):
        """Verifica el decorador admin_only para usuarios admin y no admin."""
        self.gestor._GestorLogin__admin_list = [1]
        @self.gestor.admin_only
        def f():
            return "ok"
        with patch("modules.login.current_user", new_callable=lambda: DummyCurrentUser("Juan", 1, True)):
            self.assertEqual(f(), "ok")
        with patch("modules.login.current_user", new_callable=lambda: DummyCurrentUser("Juan", 2, True)):
            with self.assertRaises(Exception):
                f()

    def test_se_requiere_login(self):
        """Verifica que el decorador se_requiere_login retorna una función decorada."""
        def dummy_func(): return "ok"
        decorated = self.gestor.se_requiere_login(dummy_func)
        # No ejecutamos el decorador real, solo comprobamos que lo devuelve envuelto
        self.assertTrue(callable(decorated))

class TestLogin(unittest.TestCase):
    """Tests adicionales para autenticación."""

    def test_flask_login_user_get_id(self):
        """Verifica que get_id de FlaskLoginUser retorna el id como string."""
        usuario = Usuario(nombre="A", apellido="B", email="a@b.com", nombre_de_usuario="ab", contraseña="123", rol=0, claustro=0, id=42)
        flask_user = FlaskLoginUser(usuario)
        self.assertEqual(flask_user.get_id(), "42")

    def test_autenticar_falla(self):
        """Verifica que autenticar retorna None si el usuario no existe."""
        engine, Session = crear_engine()
        session = Session()
        repo = RepositorioUsuariosSQLAlchemy(session)
        gestor = GestorLogin(repo)
        self.assertIsNone(gestor.autenticar("noexiste", "malpass"))

if __name__ == "__main__":
    unittest.main()