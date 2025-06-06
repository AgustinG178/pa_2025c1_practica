from modules.modelos import ModeloUsuario, ModeloReclamo
from modules.config import crear_engine
from modules.usuarios import Usuario
from modules.reclamo import Reclamo
from modules.repositorio_ABC import Repositorio
from sqlalchemy.orm import Session

def crear_repositorio():
    session = crear_engine()
    repo_reclamos =  RepositorioReclamosSQLAlchemy(session())
    repo_usuario = RepositorioUsuariosSQLAlchemy(session())
    return repo_reclamos, repo_usuario

class RepositorioUsuariosSQLAlchemy(Repositorio):
    def __init__(self, session: Session):
        self.__session: Session = session
        ModeloUsuario.metadata.create_all(self.__session.bind)

    def guardar_registro(self, usuario):
        if not isinstance(usuario, ModeloUsuario):
            raise ValueError("El parámetro no es una instancia de la clase ModeloUsuario")
        self.__session.add(usuario)
        self.__session.commit()

    def obtener_todos_los_registros(self):
        return self.__session.query(ModeloUsuario).all()
    
    def modificar_registro(self, usuario_modificado):
        if not isinstance(usuario_modificado, ModeloUsuario):
            raise ValueError("El parámetro no es una instancia de la clase ModeloUsuario")
        usuario_db = self.__session.query(ModeloUsuario).filter_by(id=usuario_modificado.id).first()
        if usuario_db:
            usuario_db.nombre = usuario_modificado.nombre
            usuario_db.apellido = usuario_modificado.apellido
            usuario_db.email = usuario_modificado.email
            usuario_db.nombre_de_usuario = usuario_modificado.nombre_de_usuario
            usuario_db.contraseña = usuario_modificado.contraseña
            self.__session.commit()
                    
    def __map_modelo_a_entidad(self, modelo: ModeloUsuario):
        return Usuario(
            modelo.id,
            modelo.nombre,
            modelo.apellido,
            modelo.email,
            modelo.nombre_de_usuario,
            modelo.contraseña,
            modelo.claustro,
            modelo.rol, 
        )        
    def __map_entidad_a_modelo(self, entidad: Usuario):
        return ModeloUsuario(
            nombre=entidad.nombre,
            apellido=entidad.apellido,
            email=entidad.email,
            nombre_de_usuario=entidad.nombre_de_usuario,
            contraseña=entidad.contraseña,
            claustro=entidad.claustro,
            rol=entidad.rol
        )

    def obtener_registro_por_filtro(self, filtro, valor):
        usuario = self.__session.query(ModeloUsuario).filter_by(**{filtro: valor}).first()
        return self.__map_modelo_a_entidad(usuario) if usuario else None
    
    def eliminar_registro_por_id(self, id):
        usuario = self.__session.query(ModeloUsuario).filter_by(id=id).first()
        if usuario:
            self.__session.delete(usuario)
            self.__session.commit()
    
    def buscar_usuario(self, **kwargs):
        """
        Busca un usuario por cualquier campo (por ejemplo, nombre_de_usuario, email, etc.)
        """
        return self.__session.query(ModeloUsuario).filter_by(**kwargs).first()

class RepositorioReclamosSQLAlchemy(Repositorio):
    def __init__(self, session: Session):
        self.__session: Session = session
        ModeloReclamo.metadata.create_all(self.__session.bind)

    def guardar_registro(self, reclamo):
        if not isinstance(reclamo, Reclamo):
            raise ValueError("El parámetro no es una instancia de la clase Reclamo")
        self.__session.add(reclamo)
        self.__session.commit()

    def obtener_todos_los_registros(self):
        return self.__session.query(Reclamo).all()

    def modificar_registro(self, reclamo_a_modificar: Reclamo):
        """
        Modifica un reclamo existente en la base de datos con los datos proporcionados.
        """
        if not isinstance(reclamo_a_modificar, Reclamo):
            raise ValueError("El parámetro no es una instancia de la clase Reclamo")

        reclamo_db = self.__session.query(ModeloReclamo).filter_by(id=reclamo_a_modificar.ID).first()
        if not reclamo_db:
            raise ValueError(f"No se encontró un reclamo con ID {reclamo_a_modificar.ID}")

        reclamo_db.estado = reclamo_a_modificar.estado
        reclamo_db.contenido = reclamo_a_modificar.contenido

        self.__session.commit()

    def obtener_registro_por_filtro(self, filtro, valor):
        reclamo = self.__session.query(Reclamo).filter_by(**{filtro: valor}).first()
        return reclamo if reclamo else None
    
    def eliminar_registro_por_id(self, id):
        reclamo = self.__session.query(Reclamo).filter_by(id=id).first()
        if reclamo:
            self.__session.delete(reclamo)
            self.__session.commit()

    def actualizar_reclamo(self,reclamo:Reclamo):
        """
        Se actualiza la información de un reclamo
        """
        self.__session.merge(reclamo)

        self.__session.commit()