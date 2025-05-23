from abc import ABC, abstractmethod
from modules.BaseDeDatos import BaseDatos
from modules import reclamos

class Usuario(ABC):
    def __init__(self, nombre, apellido, email, nombre_de_usuario, contraseña, **kwargs):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__email = email
        self.__nombre_de_usuario = nombre_de_usuario
        self.__contraseña = contraseña
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

    @abstractmethod
    def registrar(self, base_datos: BaseDatos):
        pass

    @abstractmethod
    def iniciar_sesion(self, base_datos: BaseDatos):
        pass

    @abstractmethod
    def ver_reclamos(self, base_datos: BaseDatos):
        pass

    @abstractmethod
    def crear_reclamos(self, base_datos: BaseDatos, contenido, departamento):
        pass

    @abstractmethod
    def adherirse_a_reclamo(self, base_datos: BaseDatos, reclamo_id):
        pass

class UsuarioFinal(Usuario):
    def __init__(self, nombre, apellido, email, nombre_de_usuario, contraseña, **kwargs):
        super().__init__(nombre, apellido, email, nombre_de_usuario, contraseña, **kwargs)

    def registrar(self, base_datos: BaseDatos):
        base_datos.guardar_usuario(self)

    def iniciar_sesion(self, base_datos: BaseDatos):
        usuarios = base_datos.session.query(UsuarioFinal).filter_by(_Usuario__nombre_de_usuario=self.nombre_de_usuario,_Usuario__contraseña=self.contraseña).all()
        return len(usuarios) > 0

    def ver_reclamos(self, base_datos: BaseDatos):
        # Devuelve los reclamos creados por este usuario
        return base_datos.obtener_reclamos(usuario_id=self.nombre_de_usuario)

    def crear_reclamos(self, base_datos: BaseDatos, contenido, departamento):
        nuevo_reclamo = reclamos(
            estado="pendiente",
            contenido=contenido,
            departamento=departamento,
            usuario_id=self.nombre_de_usuario
        )
        base_datos.guardar_reclamo(nuevo_reclamo)
        return nuevo_reclamo

    def adherirse_a_reclamo(self, base_datos: BaseDatos, reclamo_id):
        reclamo = base_datos.session.query(reclamo).get(reclamo_id)
        if reclamo:
            if self not in reclamo.adherentes:
                reclamo.adherentes.append(self)
                base_datos.actualizar_reclamo(reclamo)
                return True
        return False

class SecretarioTecnico(Usuario):
    def __init__(self, nombre, apellido, email, nombre_de_usuario, contraseña, **kwargs):
        super().__init__(nombre, apellido, email, nombre_de_usuario, contraseña, **kwargs)

    def registrar(self, base_datos: BaseDatos):
        base_datos.guardar_usuario(self)

    def iniciar_sesion(self, base_datos: BaseDatos):
        usuarios = base_datos.session.query(SecretarioTecnico).filter_by(
            _Usuario__nombre_de_usuario=self.nombre_de_usuario,
            _Usuario__contraseña=self.contraseña
        ).all()
        return len(usuarios) > 0

    def ver_reclamos(self, base_datos: BaseDatos):
        # Puede ver todos los reclamos
        return base_datos.obtener_reclamos()

    def crear_reclamos(self, base_datos: BaseDatos, contenido, departamento):
        nuevo_reclamo = reclamos(
            estado="pendiente",
            contenido=contenido,
            departamento=departamento,
            usuario_id=self.nombre_de_usuario
        )
        base_datos.guardar_reclamo(nuevo_reclamo)
        return nuevo_reclamo

    def adherirse_a_reclamo(self, base_datos: BaseDatos, reclamo_id):
        reclamo = base_datos.session.query(reclamo).get(reclamo_id)
        if reclamo:
            if self not in reclamo.adherentes:
                reclamo.adherentes.append(self)
                base_datos.actualizar_reclamo(reclamo)
                return True
        return False

    def derivar_reclamo(self, base_datos: BaseDatos, reclamo_id, nuevo_departamento):
        reclamo = base_datos.session.query(reclamo).get(reclamo_id)
        if reclamo:
            reclamo.departamento = nuevo_departamento
            base_datos.actualizar_reclamo(reclamo)
            return True
        return False

class JefeDepartamento(Usuario):
    def __init__(self, nombre, apellido, email, nombre_de_usuario, contraseña, **kwargs):
        super().__init__(nombre, apellido, email, nombre_de_usuario, contraseña, **kwargs)

    def registrar(self, base_datos: BaseDatos):
        base_datos.guardar_usuario(self)

    def iniciar_sesion(self, base_datos: BaseDatos):
        usuarios = base_datos.session.query(JefeDepartamento).filter_by(
            _Usuario__nombre_de_usuario=self.nombre_de_usuario,
            _Usuario__contraseña=self.contraseña
        ).all()
        return len(usuarios) > 0

    def ver_reclamos(self, base_datos: BaseDatos):
        # Puede ver reclamos de su departamento
        return base_datos.obtener_reclamos(departamento=self.departamento)

    def crear_reclamos(self, base_datos: BaseDatos, contenido, departamento):
        nuevo_reclamo = reclamos(
            estado="pendiente",
            contenido=contenido,
            departamento=departamento,
            usuario_id=self.nombre_de_usuario
        )
        base_datos.guardar_reclamo(nuevo_reclamo)
        return nuevo_reclamo

    def adherirse_a_reclamo(self, base_datos: BaseDatos, reclamo_id):
        reclamo = base_datos.session.query(reclamo).get(reclamo_id)
        if reclamo:
            if self not in reclamo.adherentes:
                reclamo.adherentes.append(self)
                base_datos.actualizar_reclamo(reclamo)
                return True
        return False

    def manejar_reclamos(self, base_datos: BaseDatos):
        # Lógica para manejar reclamos de su departamento
        return base_datos.obtener_reclamos(departamento=self.departamento)

    def ver_analitica(self, base_datos: BaseDatos):
        # Aquí iría la lógica para ver estadísticas/analítica
        pass



