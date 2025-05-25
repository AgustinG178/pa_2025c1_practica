from modules.usuarios import Usuario, UsuarioFinal, JefeDepartamento, SecretarioTecnico
from modules.repositorio import RepositorioAbstracto
from werkzeug.security import generate_password_hash, check_password_hash


class GestorDeUsuarios:
    def __init__(self, repo: RepositorioAbstracto):
        self.__repo = repo  

    """
    Intermediario entre el usuario y la base de datos, consiste de métodos para registrar, auntenticar y cargar usuarios.
    """

    def registrar_nuevo_usuario(self, nombre, apellido, email, nombre_de_usuario, password, rol):
        if self.__repo.obtener_registro_por_filtro("email", email):
            raise ValueError("El usuario ya está registrado, por favor inicie sesión")
        pass_encriptada = generate_password_hash(password= password, method= 'pbkdf2:sha256', salt_length=8)
        if rol == "UsuarioFinal":
            usuario = UsuarioFinal(nombre, apellido, email, nombre_de_usuario, pass_encriptada, rol)
        elif rol == "JefeDepartamento":
            usuario = JefeDepartamento(nombre, apellido, email, nombre_de_usuario, pass_encriptada, rol)
        elif rol == "SecretarioTecnico":
            usuario = SecretarioTecnico(nombre, apellido, email, nombre_de_usuario, pass_encriptada, rol)
        self.__repo.guardar_registro(usuario)

    def autenticar_usuario(self, email, password):
        usuario = self.__repo.obtener_registro_por_filtro("email", email)
        if not usuario:
            raise ValueError("El usuario no está registrado")
        if not check_password_hash(usuario.contraseña, password):
            raise ValueError("Contraseña incorrecta")
        return usuario.__dict__  # o usuario.to_dict() si tienes ese método
        
    def cargar_usuario(self, id_usuario):
        return self.__repo.obtener_registro_por_filtro("id", id_usuario).to_dict()
