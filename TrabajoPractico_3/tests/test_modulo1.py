# Archivo de test para realizar pruebas unitarias del modulo1
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,session
from modules.usuarios import UsuarioFinal
from modules.modelos import Base,Usuario
from modules.repositorio import RepositorioUsuariosSQLAlchemy

class TestRepositorioReclamos(unittest.TestCase):

    def setUp(self):
        """
        Se crea una base de datos de solo para pruebas
        """
        self.engine = create_engine('sqlite:///:memory:')

        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)

        self.session = self.Session()

        self.repo = RepositorioUsuariosSQLAlchemy(self.session)

    def tearDown(self):

        self.session.close()

        self.engine.dispose()
    def test_guardar_usuario(self):

        p_usuario = UsuarioFinal(nombre="Juan", email="juan@gmai.com", contraseña="juan123", apellido="pereira", nombre_de_usuario="juanpe124",claustro="estudiante",rol=None)

        usuario_tabla = p_usuario.map_to_modelo_bd()

        self.repo.guardar_registro(usuario=usuario_tabla)

        usuario_base_datos = self.session.query(Usuario).filter_by(nombre_de_usuario="juanpe124").first()

        self.assertIsNotNone(usuario_base_datos)
        self.assertEqual(usuario_base_datos.email, "juan@gmai.com")

if __name__ == "__main__":
    unittest.main()