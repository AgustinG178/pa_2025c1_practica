from sqlalchemy import create_engine, MetaData,  Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from modules import usuarios, reclamos 
from sqlalchemy.ext.declarative import declarative_base
from modules.modelos import Base, Usuario, Reclamo

"""Se encarga de la conexión, las sesiones y las operaciones CRUD (crear, leer, actualizar, borrar) usando los modelos. Es el "puente" entre la logica del programa y la base de datos."""

"""El método query de SQLAlchemy se utiliza para realizar consultas a la base de datos y obtener objetos de tus modelos (tablas) de manera sencilla y orientada a objetos."""

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
    claustro = Column(String)
    usuario = relationship("Usuario", back_populates="reclamos_creados")

class BaseDatos:
    def __init__(self, url_bd):
        """
        Inicializa la conexión a la base de datos y crea las tablas si no existen.
        """
        self.engine = create_engine(url_bd)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = None

    def conectar(self):
        """
        Crea una nueva sesión para interactuar con la base de datos.
        """
        self.session = self.Session()

    def guardar_usuario(self, usuario):
        """
        Guarda un objeto Usuario en la base de datos.
        """
        self.session.add(usuario)
        self.session.commit()

    def guardar_reclamo(self, reclamo):
        """
        Guarda un objeto Reclamo en la base de datos.
        """
        self.session.add(reclamo)
        self.session.commit()

    def actualizar_reclamo(self, reclamo):
        """
        Actualiza un objeto Reclamo existente en la base de datos.
        """
        self.session.merge(reclamo)
        self.session.commit()

    def obtener_reclamos(self, **filtros):
        """
        Obtiene una lista de reclamos aplicando filtros opcionales.
        """
        query = self.session.query(Reclamo)
        for attr, value in filtros.items():
            query = query.filter(getattr(Reclamo, attr) == value)
        return query.all()
    
    def obtener_reclamo_por_id(self,reclamo_id):
        """
        Obtiene un reclamo por su ID.
        """
        return self.session.query(Reclamo).filter_by(id=reclamo_id)