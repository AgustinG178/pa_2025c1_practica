from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, DeclarativeBase
from datetime import datetime, UTC

"""
relationship() crea una relación entre dos clases en SQLAlchemy, como por ejemplo uno-a-muchos o muchos-a-muchos.  
Permite acceder desde un objeto a los objetos relacionados en otra tabla, como `usuario.reclamos` o `reclamo.usuario`.
"""

# Base de datos base para los modelos
class Base(DeclarativeBase):
    """
    DeclarativeBase es la clase base moderna para todos los modelos de SQLAlchemy.
    Esta clase base actúa como el punto de partida para todos los modelos ORM y contiene la metadata que describe las tablas asociadas.

    Todos los modelos que representan tablas en la base de datos deben heredar de esta clase.
    """
    pass

# Tabla intermedia para la relación muchos a muchos entre reclamos y usuarios
usuarios_reclamos = Table(
    'usuarios_reclamos', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.id')),
    Column('reclamo_id', Integer, ForeignKey('reclamos.id'))
)

class ModeloUsuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String, unique=True)
    nombre_de_usuario = Column(String, unique=True)
    contraseña = Column(String)
    rol = Column(String)
    claustro = Column(String)

    reclamos = relationship(
        "ModeloReclamo",
        secondary=usuarios_reclamos,
        back_populates="usuarios"
    )
    
    def __str__(self):  
        return f"Usuario: Nombre = {self.nombre}, Apellido = {self.apellido}, Email = {self.email}, Nombre_de_usuario = {self.nombre_de_usuario}, Rol = {self.rol}"

    def __init__(self, nombre, apellido, email, nombre_de_usuario, contraseña, rol, claustro):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.nombre_de_usuario = nombre_de_usuario
        self.contraseña = contraseña
        self.rol = rol
        self.claustro = claustro
        

class ModeloReclamo(Base):
    __tablename__ = 'reclamos'
    id = Column(Integer, primary_key=True)
    estado = Column(String, default="pendiente")
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    contenido = Column(String)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    clasificacion = Column(String)
    cantidad_adherentes = Column(Integer, default=1) #Se contabiliza como adherente el usuario que crea el reclamo
    tiempo_estimado = Column(Integer,default=0) #Solo se cambia cuando el reclamo pasa de pendiente -->en proceso
    resuelto_en = Column(Integer,default=None) #Representa la cantidad de días que se tardó en resolver un reclamo
    
    ''' Relación muchos a muchos con Usuario
    Una relación muchos a muchos en SQL permite que múltiples registros de una tabla se asocien con múltiples registros de otra tabla. 
    Esto se implementa mediante una tabla intermedia que contiene claves foráneas de ambas tablas relacionadas. 
    Esta estructura facilita modelar relaciones complejas, como estudiantes inscritos en varios cursos o productos en múltiples órdenes. 
    '''

    usuarios = relationship(
        "ModeloUsuario",
        secondary=usuarios_reclamos,
        back_populates="reclamos"
    )
    usuario = relationship("ModeloUsuario", foreign_keys=[usuario_id], backref="reclamos_creados")

    @property
    def adherentes_ids(self):
        """Devuelve una lista de IDs de los usuarios adherentes a este reclamo."""
        return [usuario.id for usuario in self.usuarios]

    # @property
    # def departamento(self):
    #     return self.departamento_obj.nombre if self.departamento_obj else None
    
# class ModeloDepartamento(Base):
#     __tablename__ = 'departamento'
#     id = Column(Integer, primary_key=True)
#     nombre = Column(String)
