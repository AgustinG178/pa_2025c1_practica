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

class ModeloUsuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String, unique=True)
    nombre_de_usuario = Column(String, unique=True)
    contraseña = Column(String)
    rol = Column(String)
    claustro = Column(String)

    # Relación muchos a muchos con ModeloReclamo
    reclamos = relationship(
        "ModeloReclamo",
        secondary="reclamos_usuarios",
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
        
@property
def adherentes_ids(self):
    return [usuario.id for usuario in self.usuarios]

class ModeloReclamo(Base):
    __tablename__ = 'reclamos'

    id = Column(Integer, primary_key=True)
    estado = Column(String, default="pendiente")
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    contenido = Column(String)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    clasificacion = Column(String)
    tiempo_estimado = Column(Integer, default=0)  
    resuelto_en = Column(Integer, default=0)  
    # Relación muchos a muchos con ModeloUsuario
    usuarios = relationship(
        "ModeloUsuario",
        secondary="reclamos_usuarios",
        back_populates="reclamos"
    )

reclamos_usuarios = Table(
    'reclamos_usuarios',
    Base.metadata,
    Column('reclamo_id', Integer, ForeignKey('reclamos.id')),
    Column('usuario_id', Integer, ForeignKey('usuarios.id'))
)
