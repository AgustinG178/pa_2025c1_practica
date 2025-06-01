from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime,UTC

"""define la estructura de las tablas y las relaciones"""

#No deberíamos tener que poner todo en privado, o al menos la contraseña? Mas allá de que sean modelos?
Base = declarative_base()

class Departamento(Base):
    __tablename__ = 'departamento'
    id = Column(Integer, primary_key = True,autoincrement=True)
    nombre = Column(String)
    jefe = Column(Integer,ForeignKey("usuarios.id"))
    
    reclamos_departamento = relationship("Reclamo", back_populates="departamento_obj")

    jefe_departamento = relationship("Usuario",back_populates="departamento_asociado")

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True,autoincrement=True)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String, unique=True)
    nombre_de_usuario = Column(String, unique=True)
    contraseña = Column(String)
    claustro = Column(String)
    rol = Column(String)
    jefe_de = Column(String)


    reclamos_creados = relationship("Reclamo", back_populates="usuario")
    departamento_asociado = relationship("Departamento",back_populates="jefe_departamento")

class Reclamo(Base):
    __tablename__ = 'reclamos'
    id = Column(Integer, primary_key=True,autoincrement=True)
    estado = Column(String,default="pendiente") 
    fecha_hora = Column(DateTime, default=datetime.now(UTC))
    contenido = Column(String)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    departamento_id = Column(String, ForeignKey('departamento.id'))


    usuario = relationship("Usuario", back_populates="reclamos_creados")
    departamento_obj = relationship("Departamento", back_populates="reclamos_departamento")

    @property
    def departamento(self):
        return self.departamento_obj.nombre if self.departamento_obj else None