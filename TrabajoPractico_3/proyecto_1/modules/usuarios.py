class Usuario:
    """
    Representa un usuario del sistema con atributos personales y de acceso.

    """
    
    def __init__(self, nombre, apellido, email, nombre_de_usuario, contraseña, rol, claustro, id=None):
        """
        Inicializa una nueva instancia de Usuario.
        """
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.nombre_de_usuario = nombre_de_usuario
        self.contraseña = contraseña
        self.rol = rol
        self.claustro = claustro
        self.__id = id

    @property
    def nombre(self):
        """Obtiene el nombre del usuario."""
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        """Establece el nombre del usuario."""
        if not isinstance(nuevo_nombre, str):
            raise ValueError("El nombre debe ser una cadena de texto")
        self.__nombre = nuevo_nombre

    @property
    def apellido(self):
        """Obtiene el apellido del usuario."""
        return self.__apellido

    @apellido.setter
    def apellido(self, nuevo_apellido: str):
        """Establece el apellido del usuario."""
        if not isinstance(nuevo_apellido, str):
            raise ValueError("El apellido debe ser una cadena de texto")
        self.__apellido = nuevo_apellido

    @property
    def email(self):
        """Obtiene el correo electrónico del usuario."""
        return self.__email

    @email.setter
    def email(self, nuevo_email: str):
        """Establece el correo electrónico del usuario."""
        if not isinstance(nuevo_email, str):
            raise ValueError("El email debe ser una cadena de texto")
        self.__email = nuevo_email

    @property
    def nombre_de_usuario(self):
        """Obtiene el nombre de usuario del sistema."""
        return self.__nombre_de_usuario

    @nombre_de_usuario.setter
    def nombre_de_usuario(self, nuevo_nombre_de_usuario: str):
        """Establece el nombre de usuario del sistema."""
        if not isinstance(nuevo_nombre_de_usuario, str):
            raise ValueError("El nombre de usuario debe ser una cadena de texto")
        self.__nombre_de_usuario = nuevo_nombre_de_usuario

    @property
    def contraseña(self):
        """Obtiene la contraseña del usuario."""
        return self.__contraseña

    @contraseña.setter
    def contraseña(self, value):
        """Establece la contraseña del usuario."""
        self.__contraseña = value

    @property
    def rol(self):
        """Obtiene el rol del usuario en el sistema."""
        return self.__rol

    @rol.setter
    def rol(self, value):
        """Establece el rol del usuario en el sistema."""
        self.__rol = value

    @property
    def claustro(self):
        """Obtiene el claustro al que pertenece el usuario."""
        return self.__claustro

    @claustro.setter
    def claustro(self, value):
        """Establece el claustro al que pertenece el usuario."""
        self.__claustro = value

    @property
    def id(self):
        """Obtiene el ID del usuario."""
        return self.__id

    def to_dict(self):
        """
        Retorna un diccionario con los datos del usuario.
        """
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "nombre_de_usuario": self.nombre_de_usuario,
            "contraseña": self.contraseña,
            "rol": self.rol,
            "claustro": self.claustro,
            "id": self.id
        }

    def __str__(self):
        """
        Retorna una representación legible del usuario.
        """
        return (f"Usuario(nombre={self.nombre}, apellido={self.apellido}, email={self.email}, "
                f"nombre_de_usuario={self.nombre_de_usuario}, claustro={self.claustro}, "
                f"rol={self.rol}, id={self.id})")



