from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, DeclarativeBase
from datetime import datetime, UTC

# Base de datos base para los modelos
class Base(DeclarativeBase):
    """
    DeclarativeBase es la clase base moderna para todos los modelos de SQLAlchemy.
    Esta clase base actúa como el punto de partida para todos los modelos ORM y contiene la metadata que describe las tablas asociadas.

    Todos los modelos que representan tablas en la base de datos deben heredar de esta clase.
    """
    pass

# Tabla intermedia para la relación muchos a muchos
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
    claustro = Column(String)
    rol = Column(String)
    jefe_de = Column(String)

    reclamos = relationship(
        "Reclamo",
        secondary=usuarios_reclamos,
        back_populates="usuarios"
    )
    departamento_asociado = relationship("Departamento", back_populates="jefe_departamento")
    
    def __str__(self):  
        return f"Usuario: Nombre = {self.nombre}, Apellido = {self.apellido}, Email = {self.email}, Nombre_de_usuario = {self.nombre_de_usuario}, Rol = {self.rol}"

    def __init__(self, nombre, apellido, email, nombre_de_usuario, contraseña, claustro, rol):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.nombre_de_usuario = nombre_de_usuario
        self.contraseña = contraseña
        self.claustro = claustro
        self.rol = rol

class ModeloReclamo(Base):
    __tablename__ = 'reclamos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    estado = Column(String, default="pendiente")
    fecha_hora = Column(DateTime, default=lambda: datetime.now(UTC))
    contenido = Column(String)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    departamento_id = Column(String, ForeignKey('departamento.id'))

    # Relación muchos a muchos con Usuario
    usuarios = relationship(
        "Usuario",
        secondary=usuarios_reclamos,
        back_populates="reclamos"
    )
    usuario = relationship("Usuario", foreign_keys=[usuario_id], backref="reclamos_creados")
    departamento_obj = relationship("Departamento", back_populates="reclamos_departamento")

    # @property
    # def departamento(self):
    #     return self.departamento_obj.nombre if self.departamento_obj else None

