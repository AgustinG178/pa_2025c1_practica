# Archivo de test para realizar pruebas unitarias del modulo1
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,session
from modules.gestor_reclamos import GestorReclamo
from modules.gestor_usuario import GestorDeUsuarios
from modules.modelos import Base
class TestGestorReclamo(unittest.TestCase):

    def setUp(self):
        """
        Se crea una base de datos de solo para pruebas
        """
        self.engine = create_engine('sqlite:///:memory:')

        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)

        self.session = self.Session()
        
    def tearDown(self):

        """
        Luego de cada test, se cierra la base de datos
        """
        self.session.close()

        self.engine.dispose()
