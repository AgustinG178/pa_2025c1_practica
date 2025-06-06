from sqlalchemy import create_engine, MetaData,  Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from modules.modelos import Base, ModeloUsuario, Reclamo

"""Se encarga de la conexión, las sesiones y las operaciones CRUD (crear, leer, actualizar, borrar) usando los modelos. Es el "puente" entre la logica del programa y la base de datos."""

"""El método query de SQLAlchemy se utiliza para realizar consultas a la base de datos y obtener objetos de tus modelos (tablas) de manera sencilla y orientada a objetos."""

Base = declarative_base()

#Lo mismo con esto, en la parte de modelos hace lo mismo

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

    def actualizar_reclamo(self, reclamo_actualizado:Reclamo):
        
        """
        Actualiza un objeto Reclamo existente en la base de datos.
        """
        self.session.merge(reclamo_actualizado)
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