import unittest
from modules.usuarios import Usuario
from modules.reclamo import Reclamo
from modules.modelos import ModeloUsuario, ModeloReclamo
from modules.config import crear_engine
from sqlalchemy.orm import sessionmaker
from modules.repositorio import RepositorioUsuariosSQLAlchemy, RepositorioReclamosSQLAlchemy
from datetime import datetime

class TestRepositoriosSQLAlchemy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engine, Session = crear_engine()
        cls.session = Session()
        cls.engine = engine

        ModeloUsuario.metadata.create_all(engine)
        ModeloReclamo.metadata.create_all(engine)

    def setUp(self):
        self.session.query(ModeloReclamo).delete()
        self.session.query(ModeloUsuario).delete()
        self.session.commit()

        self.repo_usuarios = RepositorioUsuariosSQLAlchemy(self.session)
        self.repo_reclamos = RepositorioReclamosSQLAlchemy(self.session)

    def tearDown(self):
        self.session.commit()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def test_guardar_y_obtener_usuario(self):
        usuario = Usuario(
            nombre="Juan",
            apellido="Perez",
            email="juan@example.com",
            nombre_de_usuario="juanp",
            contraseña="1234",
            rol="admin",
            claustro="ing"
        )
        modelo_usuario = self.repo_usuarios._map_entidad_a_modelo(usuario)
        self.repo_usuarios.guardar_registro(modelo_usuario)

        usuarios = self.repo_usuarios.obtener_todos_los_registros()
        self.assertEqual(len(usuarios), 1)
        self.assertEqual(usuarios[0].nombre, "Juan")

    def test_modificar_usuario(self):
        usuario = Usuario(
            nombre="Ana",
            apellido="Gomez",
            email="ana@example.com",
            nombre_de_usuario="anag",
            contraseña="abcd",
            rol="user",
            claustro="cs"
        )
        modelo = self.repo_usuarios._map_entidad_a_modelo(usuario)
        self.repo_usuarios.guardar_registro(modelo)

        modelo.nombre = "Ana Maria"
        self.repo_usuarios.modificar_registro(modelo)

        usuario_modificado = self.repo_usuarios.obtener_modelo_por_id(modelo.id)
        self.assertEqual(usuario_modificado.nombre, "Ana Maria")

    def test_guardar_y_obtener_reclamo(self):
        usuario = Usuario(
            nombre="Carlos",
            apellido="Ramirez",
            email="carlos@example.com",
            nombre_de_usuario="carlitos",
            contraseña="qwerty",
            rol="user",
            claustro="ing"
        )
        modelo_usuario = self.repo_usuarios._map_entidad_a_modelo(usuario)
        self.repo_usuarios.guardar_registro(modelo_usuario)

        reclamo = Reclamo(
            estado="abierto",
            fecha_hora=datetime.now(),
            contenido="Problema con el sistema",
            usuario_id=modelo_usuario.id,
            departamento="IT",
            clasificacion="soporte"
        )
        modelo_reclamo = self.repo_reclamos.mapear_reclamo_a_modelo(reclamo)
        self.repo_reclamos.guardar_registro(modelo_reclamo)

        reclamos = self.repo_reclamos.obtener_todos_los_registros(usuario_id=modelo_usuario.id)
        self.assertEqual(len(reclamos), 1)
        self.assertEqual(reclamos[0].contenido, "Problema con el sistema")

    def test_modificar_reclamo(self):
        usuario = Usuario(
            nombre="Lucia",
            apellido="Diaz",
            email="lucia@example.com",
            nombre_de_usuario="luciad",
            contraseña="5678",
            rol="user",
            claustro="cs"
        )
        modelo_usuario = self.repo_usuarios._map_entidad_a_modelo(usuario)
        self.repo_usuarios.guardar_registro(modelo_usuario)

        reclamo = Reclamo(
            estado="abierto",
            fecha_hora=datetime.now(),
            contenido="Falló el servidor",
            usuario_id=modelo_usuario.id,
            departamento="IT",
            clasificacion="soporte"
        )
        modelo = self.repo_reclamos.mapear_reclamo_a_modelo(reclamo)
        self.repo_reclamos.guardar_registro(modelo)

        reclamo_mod = Reclamo(
            id=modelo.id,
            estado="cerrado",
            fecha_hora=reclamo.fecha_hora,
            contenido="Servidor reparado",
            usuario_id=modelo_usuario.id,
            departamento="IT",
            clasificacion="soporte"
        )
        self.repo_reclamos.modificar_registro(reclamo_mod)

        reclamo_db = self.repo_reclamos.obtener_registro_por_filtro("id", modelo.id)
        self.assertEqual(reclamo_db.estado, "cerrado")
        self.assertEqual(reclamo_db.contenido, "Servidor reparado")

if __name__ == "__main__": #pragma: no cover
    unittest.main()

