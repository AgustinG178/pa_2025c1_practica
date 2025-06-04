from flask_login import UserMixin, login_user, logout_user, login_required, current_user
from flask import abort
from functools import wraps
from modules.gestor_usuario import GestorDeUsuarios
from modules.BaseDeDatos import BaseDatos

class FlaskLoginUser(UserMixin):
    def __init__(self, dicc_usuario):
        self.id = dicc_usuario["id"]
        self.nombre = dicc_usuario["nombre"]
        self.email = dicc_usuario["email"]
        self.__password = dicc_usuario["password"]

    def verificar_password(self, password):
        return self.__password == password  # Mejora: usar hash seguro en producción

class GestorLogin:
    def __init__(self, gestor_usuarios: GestorDeUsuarios, login_manager, admin_list):
        self.__gestor_usuarios = gestor_usuarios
        login_manager.user_loader(self.__cargar_usuario_actual)
        self.__admin_list = admin_list

    @property
    def nombre_usuario_actual(self):
        return current_user.nombre

    @property
    def id_usuario_actual(self):
        return current_user.id

    @property
    def usuario_autenticado(self):
        return current_user.is_authenticated

    def __cargar_usuario_actual(self, id_usuario):
        dicc_usuario = self.__gestor_usuarios.cargar_usuario(id_usuario)
        if dicc_usuario:
            return FlaskLoginUser(dicc_usuario)
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

    def es_admin(self):
        return current_user.is_authenticated and current_user.id in self.__admin_list
    
if __name__ == "__main__":
    # Ejemplo de uso
    session = BaseDatos("sqlite:///data/base_datos.db")
    session.conectar()
    repo = session.session 
    
    
    gestor = GestorLogin(
        gestor_usuarios=GestorDeUsuarios(), 
        repo = repo,
        login_manager=None,   
        admin_list=[1, 2, 3]
          )
    
    gestor.login_usuario("tupapacitoXD_123", "1234")