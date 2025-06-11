from flask_login import login_user, logout_user, login_required, current_user
from flask import abort
from functools import wraps
from modules.gestor_usuario import GestorUsuarios
from modules.gestor_base_datos import BaseDatos
from modules.repositorio import RepositorioUsuariosSQLAlchemy

class FlaskLoginUser:
    def __init__(self, usuario):
        self._usuario = usuario  # Guardo la instancia ORM original
        self.id = usuario.id
        self.nombre = usuario.nombre
        self.apellido = usuario.apellido
        self.email = usuario.email
        self.nombre_de_usuario = usuario.nombre_de_usuario
        self._contraseña = usuario.contraseña
        self.rol = usuario.rol
        self.claustro = usuario.claustro

    def get_id(self):
        return str(self.id)

    def __str__(self):
        return f"FlaskLoginUser(id={self.id}, nombre={self.nombre}, apellido={self.apellido}, email={self.email}, nombre_de_usuario={self.nombre_de_usuario}, rol={self.rol})"

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    @property
    def contraseña(self):
        return self._contraseña
    
    @property
    def usuario_orm(self):
        return self._usuario  # Devuelve la instancia ORM original

class GestorLogin:
    def __init__(self, repositorio_usuario: RepositorioUsuariosSQLAlchemy):
        self.repositorio_usuario = repositorio_usuario

    @property
    def nombre_usuario_actual(self):
        return current_user.nombre

    @property
    def id_usuario_actual(self):
        return current_user.id

    @property
    def usuario_autenticado(self):
        return current_user.is_authenticated

    def autenticar(self, nombre_de_usuario, contraseña):
        usuario = self.repositorio_usuario.buscar_usuario(nombre_de_usuario=nombre_de_usuario)
        if usuario and usuario.contraseña == contraseña:
            return usuario
        return None

    def login_usuario(self, nombre_de_usuario, password):
        dicc_usuario = self.__gestor_usuarios.buscar_usuario_por_nombre(nombre_de_usuario)
        if dicc_usuario and dicc_usuario["password"] == password:  # Mejora: usar hash seguro
            user = FlaskLoginUser(dicc_usuario)
            login_user(user)
            print(f"Usuario {current_user.nombre} ha iniciado sesión")
            return True
        print("Credenciales incorrectas")
        return False

    def logout_usuario(self):
        logout_user()
        print("Usuario ha cerrado sesión")
        print(f"Usuario actual {current_user}")

    def admin_only(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated and current_user.id not in self.__admin_list:
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function

    def se_requiere_login(self, func):
        return login_required(func)

if __name__ == "__main__":
    # Configuración de la base de datos y repositorio
    base_datos = BaseDatos("sqlite:///data/base_datos.db")
    base_datos.conectar()
    sqlalchemy_session = base_datos.session

    repo_usuarios = RepositorioUsuariosSQLAlchemy(sqlalchemy_session)
    gestor_usuarios = GestorUsuarios(repo_usuarios)
    gestor_login = GestorLogin(repo_usuarios)

    # Prueba de autenticación
    nombre_de_usuario = "tupapacitoXD_123"
    password = "1234"
    usuario = gestor_login.autenticar(nombre_de_usuario, password)
    if usuario:
        print(f"Login exitoso para: {usuario.nombre_de_usuario}")
    else:
        print("Login fallido: credenciales incorrectas")