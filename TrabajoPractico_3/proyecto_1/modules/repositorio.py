from modules.modelos import ModeloUsuario, ModeloReclamo
from modules.config import crear_engine
from modules.usuarios import Usuario
from modules.reclamo import Reclamo
from modules.repositorio_ABC import Repositorio
from sqlalchemy.orm import Session as SessionSQL

engine, Session = crear_engine()  # Session es sessionmaker
"""
def crear_repositorio():
    Crea y devuelve dos repositorios separados para reclamos y usuarios.
    session1 = SessionSQL()  # crea una sesión activa
    session2 = SessionSQL()  # otra sesión independiente
    repo_reclamos = RepositorioReclamosSQLAlchemy(session1)
    repo_usuario = RepositorioUsuariosSQLAlchemy(session2)
    return repo_reclamos, repo_usuario
"""
class RepositorioUsuariosSQLAlchemy(Repositorio):
    """Repositorio para gestionar registros de usuarios con SQLAlchemy."""

    def __init__(self, session: SessionSQL):
        """Inicializa el repositorio y asegura que la tabla de usuarios exista."""
        self.__session = session #session es una instancia de SessionSQL (note la 's' minúscula)
        ModeloUsuario.metadata.create_all(engine)

    def guardar_registro(self, usuario: ModeloUsuario):
        """Guarda un nuevo registro de usuario en la base de datos."""
        if not isinstance(usuario, ModeloUsuario):
            raise ValueError("El parámetro no es una instancia de la clase ModeloUsuario")
        self.__session.add(usuario)
        self.__session.commit()

    def obtener_todos_los_registros(self):
        """Devuelve todos los registros de usuarios en la base de datos."""
        return self.__session.query(ModeloUsuario).all()
    
    def modificar_registro(self, usuario_modificado:ModeloUsuario):
        """Modifica los datos de un usuario existente en la base de datos."""
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

    def obtener_registro_por_filtros(self, mapeo=True, **kgwargs):

        try:
            
            modelo = self.__session.query(ModeloUsuario).filter_by(**kgwargs).first()
            if modelo:
                return self.map_modelo_a_entidad(modelo) if mapeo else modelo
        except Exception as e:
            raise ValueError(f"Error al obtener registro: {e}")
        
    def obtener_registros_por_filtro(self, filtro, valor, mapeo=True):
        
        try:
            modelos = self.__session.query(ModeloUsuario).filter_by(**{filtro: valor}).all()

            if mapeo:
                return [self.map_modelo_a_entidad(modelo) for modelo in modelos]

            else:
                return modelos        
        except Exception as e:
            raise ValueError(f"Error al obtener el registro filtrado por: {filtro}:{valor}, {e}")
        
    def map_modelo_a_entidad(self, modelo: ModeloUsuario):
        return Usuario(
            nombre=modelo.nombre,
            apellido=modelo.apellido,
            email=modelo.email,
            nombre_de_usuario=modelo.nombre_de_usuario,
            contraseña=modelo.contraseña,
            rol=modelo.rol,         
            claustro=modelo.claustro,  
            id=modelo.id
        )

    def map_entidad_a_modelo(self, entidad: Usuario):
    
        return ModeloUsuario(
            nombre=entidad.nombre,
            apellido=entidad.apellido,
            email=entidad.email,
            nombre_de_usuario=entidad.nombre_de_usuario,
            contraseña=entidad.contraseña,
            rol=entidad.rol,       
            claustro=entidad.claustro  
        )

    def eliminar_registro_por_id(self, id):
        """Elimina un usuario de la base de datos usando su ID."""
        usuario = self.__session.query(ModeloUsuario).filter_by(id=id).first()
        if usuario:
            self.__session.delete(usuario)
            self.__session.commit()

class RepositorioReclamosSQLAlchemy(Repositorio):

    """Repositorio para gestionar reclamos en la base de datos."""

    def __init__(self, session: SessionSQL):
        """Inicializa el repositorio y crea la tabla de reclamos si no existe."""
        self.__session = session
        ModeloReclamo.metadata.create_all(engine)


    @property
    def session(self):
        return self.__session
    def commit(self):
        """
        Se realiza un commit en la sesión SQL.
        """
        self.__session.commit()


    def guardar_registro(self, modelo_reclamo: ModeloReclamo):
        """Guarda un nuevo reclamo en la base de datos."""
        if not isinstance(modelo_reclamo, ModeloReclamo):
            raise ValueError("El parámetro debe ser un ModeloReclamo")
        self.__session.add(modelo_reclamo)
        self.__session.commit()
        
    def obtener_todos_los_registros(self):
        """Devuelve todos los reclamos en la base de datos."""
        modelos_reclamos_bd = self.__session.query(ModeloReclamo).all()
        return [self.map_modelo_a_entidad(modelo) for modelo in modelos_reclamos_bd ]

    def modificar_registro(self, reclamo_a_modificar: Reclamo):
        if not isinstance(reclamo_a_modificar, Reclamo):
            raise ValueError("El parámetro no es una instancia de la clase Reclamo")

        reclamo_db = self.__session.query(ModeloReclamo).filter_by(id=reclamo_a_modificar.id).first()
        if not reclamo_db:
            raise ValueError(f"No se encontró un reclamo con ID {reclamo_a_modificar.id}")

        reclamo_db.estado = reclamo_a_modificar.estado
        reclamo_db.contenido = reclamo_a_modificar.contenido
        reclamo_db.clasificacion = reclamo_a_modificar.clasificacion
        reclamo_db.tiempo_estimado = reclamo_a_modificar.tiempo_estimado

        reclamo_db.resuelto_en = reclamo_a_modificar.resuelto_en

        self.__session.commit()



    def obtener_registro_por_filtros(self,mapeo=True, **kgwargs):

        try:

            modelo = self.__session.query(ModeloReclamo).filter_by(**kgwargs).first()

            return self.map_modelo_a_entidad(modelo) if mapeo else modelo

        except Exception as e:

            raise ValueError(f"Error al obtener el registro filtrado por: {kgwargs}, {e}")
  
    def obtener_registros_por_filtro(self, filtro,valor,mapeo=True):
        
        """
        Obtiene todos los registros que coinciden con un filtro específico.
        """
        modelos = self.__session.query(ModeloReclamo).filter_by(**{filtro: valor}).all()
        if not mapeo:
            return modelos
        else:

            return [self.map_modelo_a_entidad(modelo) for modelo in modelos]
        
    def map_modelo_a_entidad(self,modelo:ModeloReclamo):
        """Convierte un modelo de SQLAlchemy en una entidad Reclamo."""
        return Reclamo(
            id=modelo.id,
            estado=modelo.estado,
            fecha_hora=modelo.fecha_hora,
            contenido=modelo.contenido,
            usuario_id=modelo.usuario_id,
            clasificacion=modelo.clasificacion,
            cantidad_adherentes=modelo.cantidad_adherentes,
            tiempo_estimado = modelo.tiempo_estimado,
            resuelto_en = modelo.resuelto_en
        )


    def map_entidad_a_modelo(self,reclamo: Reclamo) -> ModeloReclamo:
        """Convierte una entidad Reclamo a su modelo equivalente."""
        kwargs = {}
        if hasattr(reclamo, 'id') and reclamo.id is not None:
            kwargs['id'] = reclamo.id
        if hasattr(reclamo, 'resuelto_en') and reclamo.resuelto_en is not None:
            kwargs['resuelto_en'] = reclamo.resuelto_en
        return ModeloReclamo(
            estado=reclamo.estado,
            fecha_hora=reclamo.fecha_hora,
            contenido=reclamo.contenido,
            usuario_id=reclamo.usuario_id,
            clasificacion=reclamo.clasificacion,
            tiempo_estimado=reclamo.tiempo_estimado,
            **kwargs
        )

    def eliminar_registro_por_id(self, id):
        """Elimina un reclamo por su ID."""
        reclamo = self.__session.query(ModeloReclamo).filter_by(id=id).first()
        if reclamo:
            self.__session.delete(reclamo)
            self.__session.commit()
    


    def buscar_similares(self, clasificacion, reclamo_id):
        """Busca reclamos con la misma clasificación excluyendo un ID específico."""
        return (
            self.__session.query(ModeloReclamo)
            .filter_by(clasificacion=clasificacion)
            .filter(ModeloReclamo.id != reclamo_id)
            .all()
        )

    def ultimo_reclamo_creado_por_usuario(self, usuario_id):

        return self.__session.query(ModeloReclamo).filter_by(usuario_id=usuario_id).order_by(ModeloReclamo.id.desc()).first()
    
    
if __name__ == "__main__": #pragma: no cover
    
    engine, Session = crear_engine()
    session = Session()
    repo = RepositorioReclamosSQLAlchemy(session)
