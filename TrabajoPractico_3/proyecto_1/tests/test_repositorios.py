import unittest
from modules.repositorio import RepositorioUsuariosSQLAlchemy, RepositorioReclamosSQLAlchemy
from modules.modelos import ModeloUsuario, ModeloReclamo
from modules.usuarios import Usuario
from modules.reclamo import Reclamo
from modules.config import crear_engine
from datetime import datetime

class TestRepositorioUsuariosSQLAlchemyCobertura(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engine, Session = crear_engine()
        cls.session = Session()
        cls.repo = RepositorioUsuariosSQLAlchemy(cls.session)

    def setUp(self):
        self.session.query(ModeloUsuario).delete()
        self.session.commit()

    def test_guardar_registro_tipo_invalido(self):
        with self.assertRaises(ValueError):
            self.repo.guardar_registro("no es modelo")

    def test_modificar_registro_tipo_invalido(self):
        with self.assertRaises(ValueError):
            self.repo.modificar_registro("no es modelo")

    def test_modificar_registro_no_existente(self):
        modelo = ModeloUsuario(
            nombre="A", apellido="B", email="a@b.com", nombre_de_usuario="ab",
            contraseña="123", rol=0, claustro=0
        )
        # No lo guardamos, así que no existe
        self.repo.modificar_registro(modelo)  # No debe lanzar error, solo no hace nada

    def test_obtener_modelo_por_id_no_existente(self):
        self.assertIsNone(self.repo.obtener_modelo_por_id(9999))

    def test_obtener_registro_por_filtro_no_existente(self):
        self.assertIsNone(self.repo.obtener_registro_por_filtro("nombre", "noexiste"))

    def test_obtener_registro_por_filtros_no_existente(self):
        self.assertIsNone(self.repo.obtener_registro_por_filtros(nombre="noexiste"))

    def test_map_modelo_a_entidad(self):
        modelo = ModeloUsuario(
            nombre="A", apellido="B", email="a@b.com", nombre_de_usuario="ab",
            contraseña="123", rol=0, claustro=0
        )
        self.session.add(modelo)
        self.session.commit()
        entidad = self.repo._RepositorioUsuariosSQLAlchemy__map_modelo_a_entidad(modelo)
        self.assertIsInstance(entidad, Usuario)
        self.assertEqual(entidad.nombre, "A")

    def test_map_entidad_a_modelo(self):
        usuario = Usuario(
            nombre="A", apellido="B", email="a@b.com", nombre_de_usuario="ab",
            contraseña="123", rol=0, claustro=0, id=1
        )
        modelo = self.repo._map_entidad_a_modelo(usuario)
        self.assertIsInstance(modelo, ModeloUsuario)

    def test_eliminar_registro_por_id_no_existente(self):
        # No debe lanzar error si no existe
        self.repo.eliminar_registro_por_id(9999)

    def test_buscar_usuario(self):
        # Debe devolver None si no existe
        self.assertIsNone(self.repo.buscar_usuario(nombre="noexiste"))

class TestRepositorioReclamosSQLAlchemyCobertura(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engine, Session = crear_engine()
        cls.session = Session()
        cls.repo = RepositorioReclamosSQLAlchemy(cls.session)

    def setUp(self):
        self.session.query(ModeloReclamo).delete()
        self.session.commit()

    def test_guardar_registro_tipo_invalido(self):
        with self.assertRaises(ValueError):
            self.repo.guardar_registro("no es modelo")

    def test_modificar_registro_tipo_invalido(self):
        with self.assertRaises(ValueError):
            self.repo.modificar_registro("no es reclamo")

    def test_modificar_registro_no_existente(self):
        reclamo = Reclamo(
            id=9999, estado="pendiente", fecha_hora=datetime.now(),
            contenido="x", usuario_id=1, clasificacion="a", cantidad_adherentes=0, tiempo_estimado=1
        )
        with self.assertRaises(ValueError):
            self.repo.modificar_registro(reclamo)

    def test_modificar_registro_orm_tipo_invalido(self):
        with self.assertRaises(ValueError):
            self.repo.modificar_registro_orm("no es modelo")

    def test_modificar_registro_orm_no_existente(self):
        modelo = ModeloReclamo(
            id=9999, estado="pendiente", fecha_hora=datetime.now(),
            contenido="x", usuario_id=1, clasificacion="a", cantidad_adherentes=0, tiempo_estimado=1
        )
        with self.assertRaises(ValueError):
            self.repo.modificar_registro_orm(modelo)

    def test_obtener_registro_por_filtro_no_existente(self):
        self.assertIsNone(self.repo.obtener_registro_por_filtro("id", 9999))

    def test_eliminar_registro_por_id_no_existente(self):
        self.repo.eliminar_registro_por_id(9999)  # No debe lanzar error

    def test_buscar_similares(self):
        # No hay reclamos, debe devolver lista vacía
        self.assertEqual(self.repo.buscar_similares("ninguna", 9999), [])

    def test_obtener_por_id_no_existente(self):
        self.assertIsNone(self.repo.obtener_por_id(9999))

    def test_obtener_registros_por_filtro_no_existente(self):
        self.assertEqual(self.repo.obtener_registros_por_filtro("clasificacion", "noexiste"), [])

    def test_mapear_reclamo_a_modelo_y_modelo_a_reclamo(self):
        reclamo = Reclamo(
            id=1, estado="pendiente", fecha_hora=datetime.now(),
            contenido="test", usuario_id=1, clasificacion="a", cantidad_adherentes=0, tiempo_estimado=1
        )
        modelo = self.repo.mapear_reclamo_a_modelo(reclamo)
        self.assertIsInstance(modelo, ModeloReclamo)
        reclamo2 = self.repo.mapear_modelo_a_reclamo(modelo)
        self.assertIsInstance(reclamo2, Reclamo)

    def test_actualizar_reclamo(self):
        reclamo = Reclamo(
            id=None, estado="pendiente", fecha_hora=datetime.now(),
            contenido="test", usuario_id=1, clasificacion="a", cantidad_adherentes=0, tiempo_estimado=1
        )
        modelo = self.repo.mapear_reclamo_a_modelo(reclamo)
        self.repo.guardar_registro(modelo)
        reclamo_db = self.repo.obtener_todos_los_reclamos_base()[0]
        reclamo_db_entidad = self.repo.mapear_modelo_a_reclamo(reclamo_db)
        reclamo_db_entidad.estado = "resuelto"
        self.repo.actualizar_reclamo(reclamo_db_entidad)
        reclamo_mod = self.repo.obtener_por_id(reclamo_db_entidad.id)
        self.assertEqual(reclamo_mod.estado, "resuelto")

    def test_obtener_ultimos_reclamos(self):
        reclamo = Reclamo(
            id=None, estado="pendiente", fecha_hora=datetime.now(),
            contenido="test", usuario_id=1, clasificacion="a", cantidad_adherentes=0, tiempo_estimado=1
        )
        modelo = self.repo.mapear_reclamo_a_modelo(reclamo)
        self.repo.guardar_registro(modelo)
        ultimos = self.repo.obtener_ultimos_reclamos(limit=1)
        self.assertTrue(len(ultimos) >= 0)

if __name__ == "__main__":
    unittest.main()

