from abc import ABC, abstractmethod
from modules.modelos import Usuario, Reclamo
from modules.config import crear_engine

class RepositorioAbstracto(ABC):
    @abstractmethod
    def guardar_registro(self, entidad):
        raise NotImplementedError

    @abstractmethod
    def obtener_todos_los_registros(self) -> list:
        raise NotImplementedError
    
    @abstractmethod
    def modificar_registro(self, entidad_modificada):
        raise NotImplementedError   
    
    @abstractmethod
    def obtener_registro_por_filtro(self, filtro, valor):
        raise NotImplementedError
    
    @abstractmethod
    def eliminar_registro_por_id(self, id):
        raise NotImplementedError


def crear_repositorio():
    session = crear_engine()
    repo_reclamos =  RepositorioReclamosSQLAlchemy(session())
    repo_usuario = RepositorioUsuariosSQLAlchemy(session())
    return repo_reclamos, repo_usuario

class RepositorioUsuariosSQLAlchemy(RepositorioAbstracto):
    def __init__(self, session):
        self.__session = session
        Usuario.metadata.create_all(self.__session.bind)

    def guardar_registro(self, usuario):
        if not isinstance(usuario, Usuario):
            raise ValueError("El parámetro no es una instancia de la clase Usuario")
        self.__session.add(usuario)
        self.__session.commit()

    def obtener_todos_los_registros(self):
        return self.__session.query(Usuario).all()
    
    def modificar_registro(self, usuario_modificado):
        if not isinstance(usuario_modificado, Usuario):
            raise ValueError("El parámetro no es una instancia de la clase Usuario")
        usuario_db = self.__session.query(Usuario).filter_by(id=usuario_modificado.id).first()
        if usuario_db:
            usuario_db.nombre = usuario_modificado.nombre
            usuario_db.apellido = usuario_modificado.apellido
            usuario_db.email = usuario_modificado.email
            usuario_db.nombre_de_usuario = usuario_modificado.nombre_de_usuario
            usuario_db.contraseña = usuario_modificado.contraseña
            self.__session.commit()

    def obtener_registro_por_filtro(self, filtro, valor):
        usuario = self.__session.query(Usuario).filter_by(**{filtro: valor}).first()
        return usuario if usuario else None
    
    def eliminar_registro_por_id(self, id):
        usuario = self.__session.query(Usuario).filter_by(id=id).first()
        if usuario:
            self.__session.delete(usuario)
            self.__session.commit()

class RepositorioReclamosSQLAlchemy(RepositorioAbstracto):
    def __init__(self, session):
        self.__session = session
        Reclamo.metadata.create_all(self.__session.bind)

    def guardar_registro(self, reclamo):
        if not isinstance(reclamo, Reclamo):
            raise ValueError("El parámetro no es una instancia de la clase Reclamo")
        self.__session.add(reclamo)
        self.__session.commit()

    def obtener_todos_los_registros(self):
        return self.__session.query(Reclamo).all()
    
    def modificar_registro(self, reclamo_modificado):
        if not isinstance(reclamo_modificado, Reclamo):
            raise ValueError("El parámetro no es una instancia de la clase Reclamo")
        reclamo_db = self.__session.query(Reclamo).filter_by(id=reclamo_modificado.id).first()
        if reclamo_db:
            reclamo_db.estado = reclamo_modificado.estado
            reclamo_db.contenido = reclamo_modificado.contenido
            reclamo_db.departamento_id = reclamo_modificado.departamento_id
            reclamo_db.usuario_id = reclamo_modificado.usuario_id
            self.__session.commit()

    def obtener_registro_por_filtro(self, filtro, valor):
        reclamo = self.__session.query(Reclamo).filter_by(**{filtro: valor}).first()
        return reclamo if reclamo else None
    
    
    def eliminar_registro_por_id(self, id):
        reclamo = self.__session.query(Reclamo).filter_by(id=id).first()
        if reclamo:
            self.__session.delete(reclamo)
            self.__session.commit()
