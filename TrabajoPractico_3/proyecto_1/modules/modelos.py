from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime, UTC

Base = declarative_base()

# Tabla intermedia para la relación muchos a muchos
usuarios_reclamos = Table(
    'usuarios_reclamos', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.id')),
    Column('reclamo_id', Integer, ForeignKey('reclamos.id'))
)

class Departamento(Base):
    __tablename__ = 'departamento'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    jefe = Column(Integer, ForeignKey("usuarios.id"))
    reclamos_departamento = relationship("Reclamo", back_populates="departamento_obj")
    jefe_departamento = relationship("Usuario", back_populates="departamento_asociado")

class Usuario(Base):
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

    def solicitar_reclamo(self, gestor_reclamo, descripcion, datos_adicionales):
        gestor_reclamo.crear_reclamo(self, descripcion, datos_adicionales)

    def ver_reclamos(self, gestor_reclamo):
        return gestor_reclamo.buscar_reclamos_por_usuario(self)

class Reclamo(Base):
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

    @property
    def departamento(self):
        return self.departamento_obj.nombre if self.departamento_obj else None

