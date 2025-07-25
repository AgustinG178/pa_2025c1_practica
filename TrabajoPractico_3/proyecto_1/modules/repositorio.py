from modules.modelos import ModeloUsuario, ModeloReclamo
from modules.config import crear_engine
from modules.usuarios import Usuario
from modules.reclamo import Reclamo
from modules.repositorio_ABC import Repositorio
from sqlalchemy.orm import Session as SessionSQL
from sqlalchemy.orm import joinedload

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
    
    def modificar_registro(self, usuario_modificado):
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

    def obtener_modelo_por_id(self, id):
        """Devuelve una instancia del modelo de usuario según el ID."""
        return self.__session.query(ModeloUsuario).filter_by(id=id).first()

    def obtener_registro_por_filtro(self, campo, valor,mapeo=True, campo2=None, valor2=None):
        """Obtiene un registro de usuario según uno o dos filtros especificados."""
        
        query = self.__session.query(ModeloUsuario).filter(getattr(ModeloUsuario, campo) == valor)
        if campo2 and valor2:
            query = query.filter(getattr(ModeloUsuario, campo2) == valor2)
        modelo = query.first()
        if modelo and mapeo:
            return self.__map_modelo_a_entidad(modelo)
        
        return modelo

    def obtener_registro_por_filtros(self, **filtros):
        """Devuelve un registro de usuario aplicando múltiples filtros."""
        modelo = self.__session.query(ModeloUsuario).filter_by(**filtros).first()
        if modelo:
            return self.__map_modelo_a_entidad(modelo)
        return None

    def __map_modelo_a_entidad(self, modelo: ModeloUsuario):
        """Convierte un modelo de SQLAlchemy en una entidad de dominio."""
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

    def _map_entidad_a_modelo(self, entidad: Usuario):
        """Convierte una entidad de dominio en un modelo de SQLAlchemy."""
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

    def buscar_usuario(self, **kwargs):
        """Busca un usuario por uno o más campos específicos."""
        return self.__session.query(ModeloUsuario).filter_by(**kwargs).first()


class RepositorioReclamosSQLAlchemy(Repositorio):

    """Repositorio para gestionar reclamos en la base de datos."""

    def __init__(self, session: SessionSQL):
        """Inicializa el repositorio y crea la tabla de reclamos si no existe."""
        self.__session = session
        ModeloReclamo.metadata.create_all(engine)

    def commit(self):
        """Confirma los cambios realizados en la sesión."""
        self.__session.commit()

    @property
    def session(self):
        """Devuelve la sesión activa de SQLAlchemy."""
        return self.__session

    @staticmethod
    def mapear_reclamo_a_modelo(reclamo: Reclamo) -> ModeloReclamo:
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

    @staticmethod
    def mapear_modelo_a_reclamo(modelo: ModeloReclamo) -> Reclamo:
        """Convierte un modelo de SQLAlchemy en una entidad Reclamo."""
        ids_adherentes = [u.id for u in modelo.usuarios] if modelo.usuarios else []
        reclamo = Reclamo(
            id=modelo.id,
            estado=modelo.estado,
            fecha_hora=modelo.fecha_hora,
            contenido=modelo.contenido,
            usuario_id=modelo.usuario_id,
            clasificacion=modelo.clasificacion,
            cantidad_adherentes=modelo.cantidad_adherentes,
            tiempo_estimado = modelo.tiempo_estimado,
            resuelto_en = modelo.resuelto_en,
            usuarios_adheridos=ids_adherentes 
        )
        
        reclamo.id = modelo.id
        
        return reclamo
        
    def guardar_registro(self, modelo_reclamo: ModeloReclamo):
        """Guarda un nuevo reclamo en la base de datos."""
        if not isinstance(modelo_reclamo, ModeloReclamo):
            raise ValueError("El parámetro debe ser un ModeloReclamo")
        self.__session.add(modelo_reclamo)
        self.__session.commit()

    def obtener_registro_por_filtro(self, filtro, valor,mapeo=True):
        """Obtiene un reclamo aplicando un filtro; puede devolverlo mapeado o como modelo."""
        modelo = self.__session.query(ModeloReclamo).filter_by(**{filtro: valor}).first()

        return self.mapear_modelo_a_reclamo(modelo) if mapeo else modelo

    def obtener_registros_por_filtro(self, filtro, valor, mapeo=True):
        query = self.__session.query(ModeloReclamo).filter_by(**{filtro: valor})
        query = query.options(joinedload(ModeloReclamo.usuarios))  # Carga los usuarios adheridos, joinedload(ModeloReclamo.usuarios) fuerza el eager loading de la relación usuarios en la misma consulta, evitando lazy‐loading y problemas de N+1 queries.
        modelos = query.all()
        if not mapeo:
            return modelos
        return [self.mapear_modelo_a_reclamo(modelo) for modelo in modelos]

    def obtener_todos_los_registros(self):
        """Devuelve todos los reclamos en la base de datos."""
        modelos_reclamos_bd = self.__session.query(ModeloReclamo).all()
        return [self.mapear_modelo_a_reclamo(modelo) for modelo in modelos_reclamos_bd ]

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
        # Actualizar también el campo resuelto_en
        reclamo_db.resuelto_en = reclamo_a_modificar.resuelto_en

        self.__session.commit()

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

    def obtener_ultimos_reclamos(self, limit=4):
        """Devuelve los últimos reclamos ordenados por fecha de creación."""
        print("[DEBUG] Tipo de self.__session:", type(self.__session))
        print("[DEBUG] Contenido de self.__session:", self.__session)
        return (
            self.__session.query(ModeloReclamo)
            .order_by(ModeloReclamo.fecha_hora.desc())
            .limit(limit)
            .all()
        )

    def obtener_por_id(self, id_reclamo):

        """Obtiene un reclamo según su ID."""

        return self.__session.query(ModeloReclamo).filter_by(id=id_reclamo).first()


if __name__ == "__main__": #pragma: no cover
    
    engine, Session = crear_engine()
    session = Session()
    repo = RepositorioReclamosSQLAlchemy(session)
    ultimos = repo.obtener_ultimos_reclamos(limit=4)
    print(f"Últimos {len(ultimos)} reclamos:")
    for r in ultimos:
        print(f"ID: {r.id} - Contenido: {r.contenido} - Fecha: {r.fecha_hora} - Clasificación: {r.clasificacion}")
