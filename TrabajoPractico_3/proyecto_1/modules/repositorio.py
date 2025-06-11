from modules.modelos import ModeloUsuario, ModeloReclamo
from modules.config import crear_engine
from modules.usuarios import Usuario
from modules.reclamo import Reclamo
from modules.repositorio_ABC import Repositorio
from sqlalchemy.orm import Session as SessionSQL

engine, Session = crear_engine()  # Session es sessionmaker

def crear_repositorio():
    session1 = SessionSQL()  # crea una sesión activa
    session2 = SessionSQL()  # otra sesión independiente
    repo_reclamos = RepositorioReclamosSQLAlchemy(session1)
    repo_usuario = RepositorioUsuariosSQLAlchemy(session2)
    return repo_reclamos, repo_usuario

class RepositorioUsuariosSQLAlchemy(Repositorio):
    def __init__(self, session: SessionSQL):
        self.__session = session
        ModeloUsuario.metadata.create_all(engine)

    def guardar_registro(self, usuario:ModeloUsuario):
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
     
    def obtener_modelo_por_id(self, id):
        """obtener_modelo_por_id da una instancia directa de SQLAlchemy."""
        return self.__session.query(ModeloUsuario).filter_by(id=id).first()
                    
    def obtener_registro_por_filtro(self, campo, valor, campo2=None, valor2=None):
        
        #Implementación para el método abstracto esperado
        query = self.__session.query(ModeloUsuario).filter(getattr(ModeloUsuario, campo) == valor)
        if campo2 and valor2:
            query = query.filter(getattr(ModeloUsuario, campo2) == valor2)
        modelo = query.first()
        if modelo:
            return self.__map_modelo_a_entidad(modelo)
        return None

    def obtener_registro_por_filtros(self, **filtros):
        modelo = self.__session.query(ModeloUsuario).filter_by(**filtros).first()
        if modelo:
            return self.__map_modelo_a_entidad(modelo)
        return None
    
    def __map_modelo_a_entidad(self, modelo: ModeloUsuario):
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
    def __init__(self, session: SessionSQL):
        self.__session = session
        ModeloReclamo.metadata.create_all(engine)
        
    def commit(self):
        """
        Commit de la sesión actual.
        """
        self.__session.commit()
        
    @property
    def session(self):
        return self.__session

    @staticmethod
    def mapear_reclamo_a_modelo(reclamo: Reclamo) -> ModeloReclamo:
        # Incluye el id si está presente en el objeto Reclamo
        kwargs = {}
        if hasattr(reclamo, 'id') and reclamo.id is not None:
            kwargs['id'] = reclamo.id
        return ModeloReclamo(
            estado=reclamo.estado,
            fecha_hora=reclamo.fecha_hora,
            contenido=reclamo.contenido,
            usuario_id=reclamo.usuario_id,
            departamento=reclamo.departamento,
            clasificacion=reclamo.clasificacion,
            **kwargs
        )
        
    @staticmethod
    def mapear_modelo_a_reclamo(modelo: ModeloReclamo) -> Reclamo:
        return Reclamo(
            id=modelo.id,
            estado=modelo.estado,
            fecha_hora=modelo.fecha_hora,
            contenido=modelo.contenido,
            usuario_id=modelo.usuario_id,
            departamento=modelo.departamento,
            clasificacion=modelo.clasificacion,
            cantidad_adherentes=modelo.cantidad_adherentes
        )

    def guardar_registro(self, modelo_reclamo: ModeloReclamo):
        if not isinstance(modelo_reclamo, ModeloReclamo):
            raise ValueError("El parámetro debe ser un ModeloReclamo")
        self.__session.add(modelo_reclamo)
        self.__session.commit()

    def obtener_todos_los_registros(self, usuario_id):
        return self.__session.query(ModeloReclamo).filter_by(usuario_id=usuario_id).all()

    def modificar_registro(self, reclamo_a_modificar: Reclamo):
        """
        Modifica un reclamo existente en la base de datos con los datos proporcionados.
        """
        if not isinstance(reclamo_a_modificar, Reclamo):
            raise ValueError("El parámetro no es una instancia de la clase Reclamo")

        reclamo_db = self.__session.query(ModeloReclamo).filter_by(id=reclamo_a_modificar.id).first()
        if not reclamo_db:
            raise ValueError(f"No se encontró un reclamo con ID {reclamo_a_modificar.id}")

        reclamo_db.estado = reclamo_a_modificar.estado
        reclamo_db.contenido = reclamo_a_modificar.contenido

        self.__session.commit()

    def obtener_registro_por_filtro(self, filtro, valor, mapeado=True):
        modelo = self.__session.query(ModeloReclamo).filter_by(**{filtro: valor}).first()
        return self.mapear_modelo_a_reclamo(modelo) if modelo and mapeado else modelo
    
    def eliminar_registro_por_id(self, id):
        reclamo = self.__session.query(ModeloReclamo).filter_by(id=id).first()
        if reclamo:
            self.__session.delete(reclamo)
            self.__session.commit()

    def actualizar_reclamo(self,reclamo:Reclamo):
        """
        Se actualiza la información de un reclamo
        """
        modelo = self.mapear_reclamo_a_modelo(reclamo)
        self.__session.merge(modelo)
        self.__session.commit()
        
    def buscar_similares(self, clasificacion, reclamo_id):
        return (
            self.__session.query(ModeloReclamo)
            .filter_by(clasificacion=clasificacion)
            .filter(ModeloReclamo.id != reclamo_id)
            .all()
        )

    def obtener_ultimos_reclamos(self, limit=4):
        return (
            self.__session.query(ModeloReclamo)
            .order_by(ModeloReclamo.fecha_hora.desc())
            .limit(limit)
            .all()
        )
        
    def obtener_por_id(self, id_reclamo):
        return self.__session.query(ModeloReclamo).filter_by(id=id_reclamo).first()

    def obtener_registros_por_filtro(self, filtro,valor):
        
        """
        Obtiene todos los registros que coinciden con un filtro específico.
        """
        modelos = self.__session.query(ModeloReclamo).filter_by(**{filtro: valor}).all()
        return [self.mapear_modelo_a_reclamo(modelo) for modelo in modelos]

if __name__ == "__main__": #pragma: no cover
    from modules.config import crear_engine
    from datetime import datetime

    # # Crear engine y sesión
    # engine, Session = crear_engine()
    # session = Session()

    # # Instanciar el repositorio
    # repo = RepositorioReclamosSQLAlchemy(session)

    # # Crear reclamo de prueba
    # reclamo_prueba = Reclamo(
    #     estado="pendiente",
    #     fecha_hora=datetime.now(),
    #     contenido="Reclamo de prueba",
    #     departamento="soporte",  # o lo que uses para 'departamento_id'
    #     clasificacion = "general", # o lo que uses para 'clasificacion_id'
    #     usuario_id=None  # Este campo se asignará manualmente más tarde
    # )

    # # Asignar usuario_id manualmente (debería coincidir con uno real en la tabla usuarios)
    # reclamo_prueba.usuario_id = 1

    # # Mapear y guardar
    # modelo = repo.mapear_reclamo_a_modelo(reclamo_prueba)
    # repo.guardar_registro(modelo)

    # # Verificar que se guardó correctamente
    # reclamos_guardados = repo.obtener_todos_los_registros(usuario_id=1)
    # # for r in reclamos_guardados:
    # #     print(f"ID: {r.id}, Estado: {r.estado}, Contenido: {r.contenido}, Usuario: {r.usuario_id}")
    engine, Session = crear_engine()
    session = Session()
    repo = RepositorioReclamosSQLAlchemy(session)
    ultimos = repo.obtener_ultimos_reclamos(limit=4)
    print(f"Últimos {len(ultimos)} reclamos:")
    for r in ultimos:
        print(f"ID: {r.id} - Contenido: {r.contenido} - Fecha: {r.fecha_hora} - Clasificación: {r.clasificacion}")
