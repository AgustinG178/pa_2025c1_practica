from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

"""define la estructura de las tablas y las relaciones"""

#No deberíamos tener que poner todo en privado, o al menos la contraseña? Mas allá de que sean modelos?
Base = declarative_base()

class Departamento(Base):
    __tablename__ = 'departamento'
    id = Column(Integer, primary_key = True)
    nombre = Column(String)
    jefe = Column(String,ForeignKey("usuario.id"))

    reclamos_departamento = relationship("Reclamo", back_populates="Departamento")
    jefe_departamento = relationship("Usuario",back_populates="Departamento")

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String, unique=True)
    nombre_de_usuario = Column(String, unique=True)
    contraseña = Column(String)
    claustro = Column(String)
    rol = Column(String)
    jefe_de = Column(String)


    reclamos_creados = relationship("Reclamo", back_populates="usuario")
    departamento_asociado = relationship("Departamento",back_populates="usuario")

class Reclamo(Base):
    __tablename__ = 'reclamos'
    id = Column(Integer, primary_key=True)
    estado = Column(String)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    contenido = Column(String)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    departamento = Column(String, ForeignKey('departamento.nombre'))


    usuario = relationship("Usuario", back_populates="reclamos_creados")
    departamento_obj = relationship("Departamento", back_populates="reclamos_departamento")

    @property
    def departamento(self):
        return self.departamento_obj.nombre if self.departamento_obj else None