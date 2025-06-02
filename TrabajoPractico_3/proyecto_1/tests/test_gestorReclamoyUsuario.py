# Archivo de test para realizar pruebas unitarias del modulo1
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,session
from modules.gestor_reclamos import GestorReclamo
from modules.gestor_usuario import GestorDeUsuarios
from modules.modelos import Base,Usuario,Reclamo,Departamento
from modules.usuarios import UsuarioFinal
from modules.repositorio import RepositorioReclamosSQLAlchemy,RepositorioUsuariosSQLAlchemy
class TestGestorReclamo(unittest.TestCase):

    def setUp(self):
        """
        Se crea una base de datos de solo para pruebas
        """
        self.engine = create_engine('sqlite:///:memory:')

        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)

        self.session = self.Session()

        self.repo_usuarios = RepositorioUsuariosSQLAlchemy(self.session)

        self.repo_reclamos = RepositorioReclamosSQLAlchemy(self.session)

        self.gestor_reclamo = GestorReclamo

        self.gestor_usuario = GestorDeUsuarios

    def tearDown(self):

        """
        Luego de cada test, se cierra la base de datos
        """
        self.session.close()

        self.engine.dispose()
    
    
    def test_crear_reclamo(self):
        
        """
        Se testea el gestor_reclamo para crear reclamos 
        """

        p_usuario = UsuarioFinal(nombre="Juan", email="juan@gmai.com", contraseña="juan123", apellido="pereira", nombre_de_usuario="juanpe124",claustro="estudiante",rol=None)

        usuario_tabla = p_usuario.map_to_modelo_bd()

        dpto_prueba = Departamento(nombre="matematica",jefe=usuario_tabla.id)

        descripcion = "No hay papel"

        self.gestor_reclamo.crear_reclamo(usuario=usuario_tabla, descripcion=descripcion, departamento=dpto_prueba)

        reclamo_base = self.session.query(Reclamo).filter_by(contenido = descripcion).first()

        self.assertEqual(reclamo_base.contenido,descripcion)

    def test_buscar_reclamos_por_usuario(self):

        """
        Se testea la capacidad de devolver todos los reclamos relacionados a un usuarios
        """

        
