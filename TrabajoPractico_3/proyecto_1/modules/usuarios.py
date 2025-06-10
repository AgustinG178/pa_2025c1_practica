from modules.BaseDeDatos import BaseDatos

class Usuario():
    def __init__(self, nombre, apellido, email, nombre_de_usuario, contraseña, claustro, rol,id, **kwargs):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__email = email
        self.__nombre_de_usuario = nombre_de_usuario
        self.__contraseña = contraseña
        self.__claustro = claustro
        self.__rol = 0
        self.__id = id
        self.__kwargs = kwargs

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self,nuevo_nombre:str):
        if not isinstance(nuevo_nombre, str):
            raise ValueError("El nombre debe ser una cadena de texto")
        self.__nombre = nuevo_nombre
    @property
    def apellido(self):
        return self.__apellido

    @apellido.setter
    def apellido(self,nuevo_apellido:str):
        if not isinstance(nuevo_apellido, str):
            raise ValueError("El apellido debe ser una cadena de texto")
        self.__apellido = nuevo_apellido

    @property
    def email(self):
        return self.__email
    
    @email.setter   
    def email(self, nuevo_email: str):
        if not isinstance(nuevo_email, str):
            raise ValueError("El email debe ser una cadena de texto")
        self.__email = nuevo_email

    @property
    def nombre_de_usuario(self):
        return self.__nombre_de_usuario

    @nombre_de_usuario.setter
    def nombre_de_usuario(self, nuevo_nombre_de_usuario: str):
        if not isinstance(nuevo_nombre_de_usuario, str):
            raise ValueError("El nombre de usuario debe ser una cadena de texto")
        self.__nombre_de_usuario = nuevo_nombre_de_usuario

    
    @property
    def contraseña(self):
        return self.__contraseña
    
    @property
    def id(self):
        return self.__id
    
    @property
    def claustro(self):
        return self.__claustro
    
    @property
    def rol(self):
        return self.__rol

    def registrar(self, base_datos: BaseDatos):
        pass

    def iniciar_sesion(self, base_datos: BaseDatos):
        pass
    
    def ver_reclamos(self, base_datos: BaseDatos):
        pass

    def adherirse_a_reclamo(self, base_datos: BaseDatos, reclamo_id):
        pass
    
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
    



