from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

"""define la estructura de las tablas y las relaciones"""

#No deberíamos tener que poner todo en privado, o al menos la contraseña? Mas allá de que sean modelos?
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String, unique=True)
    nombre_de_usuario = Column(String, unique=True)
    contraseña = Column(String)

    reclamos_creados = relationship("Reclamo", back_populates="usuario")

class Reclamo(Base):
    __tablename__ = 'reclamos'
    id = Column(Integer, primary_key=True)
    estado = Column(String)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    contenido = Column(String)
    departamento = Column(String)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))

    usuario = relationship("Usuario", back_populates="reclamos_creados")