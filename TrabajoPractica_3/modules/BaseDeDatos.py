from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from modules import Usuario, Reclamo  # Asegúrate de tener estos modelos definidos

class BaseDatos:
    def __init__(self, url_bd):
        """
        Inicializa la conexión a la base de datos.
        Args:
            url_bd (str): URL de conexión a la base de datos.
        """
        self.engine = create_engine(url_bd)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)
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
        Args:
            usuario (Usuario): Instancia del modelo Usuario a guardar.
        """
        self.session.add(usuario)
        self.session.commit()

    def guardar_reclamo(self, reclamo):
        """
        Guarda un objeto Reclamo en la base de datos.
        Args:
            reclamo (Reclamo): Instancia del modelo Reclamo a guardar.
        """
        self.session.add(reclamo)
        self.session.commit()

    def actualizar_reclamo(self, reclamo):
        """
        Actualiza un objeto Reclamo existente en la base de datos.
        Args:
            reclamo (Reclamo): Instancia del modelo Reclamo a actualizar.
        """
        self.session.merge(reclamo)
        self.session.commit()

    def obtener_reclamos(self, **filtros):
        """
        Obtiene una lista de reclamos aplicando filtros opcionales.
        Args:
            **filtros: Filtros opcionales como argumentos clave-valor.
        Returns:
            list: Lista de objetos Reclamo que cumplen con los filtros.
        """
        query = self.session.query(Reclamo)
        for attr, value in filtros.items():
            query = query.filter(getattr(Reclamo, attr) == value)
        return query.all()