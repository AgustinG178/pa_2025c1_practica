from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.modelos import Base
from modules.reclamo import Reclamo

"""Se encarga de la conexión, las sesiones y las operaciones CRUD (crear, leer, actualizar, borrar) usando los modelos. Es el "puente" entre la logica del programa y la base de datos."""

"""El método query de SQLAlchemy se utiliza para realizar consultas a la base de datos y obtener objetos de tus modelos (tablas) de manera sencilla y orientada a objetos."""

class GestorBaseDatos:
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
        return self.session is not None

    def desconectar(self):
        if self.session:
            self.session.close()
            self.session = None
            return True
        return False
