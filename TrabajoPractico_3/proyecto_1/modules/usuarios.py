from modules.BaseDeDatos import BaseDatos
from modules.modelos import Usuario as UsuarioBD
class Usuario():
    def __init__(self, nombre, apellido, email, nombre_de_usuario, contraseña, claustro,rol, **kwargs):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__email = email
        self.__nombre_de_usuario = nombre_de_usuario
        self.__contraseña = contraseña
        self.__claustro = claustro
        self.__rol = 0
        self.__kwargs = kwargs

    @property
    def nombre(self):
        return self.__nombre

    @property
    def apellido(self):
        return self.__apellido

    @property
    def email(self):
        return self.__email

    @property
    def nombre_de_usuario(self):
        return self.__nombre_de_usuario

    @property
    def contraseña(self):
        return self.__contraseña

    def registrar(self, base_datos: BaseDatos):
        pass

    def iniciar_sesion(self, base_datos: BaseDatos):
        pass
    
    def ver_reclamos(self, base_datos: BaseDatos):
        pass

    def adherirse_a_reclamo(self, base_datos: BaseDatos, reclamo_id):
        pass
  
    def map_to_modelo_bd(self):
        return UsuarioBD(
            nombre=self.nombre,
            apellido=self.apellido,
            email=self.email,
            nombre_de_usuario=self.nombre_de_usuario,
            contraseña=self.contraseña,
            claustro=self.__claustro,
            rol=self.__rol,
            **self.__kwargs
        )
    
    def __dict__(self):
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "nombre_de_usuario": self.nombre_de_usuario,
            "contraseña": self.contraseña,
            "claustro": self.__claustro,
            **self.__kwargs
        }

    def __str__(self):
        return f"Usuario(nombre={self.nombre}, apellido={self.apellido}, email={self.email}, nombre_de_usuario={self.nombre_de_usuario}, claustro={self.__claustro}, rol={self.__rol})"
    



