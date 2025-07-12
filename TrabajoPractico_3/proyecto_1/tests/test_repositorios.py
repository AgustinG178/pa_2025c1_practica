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
        self.assertIsNone(self.repo.obtener_registro_por_filtros(**{"id":9999}))

    def test_obtener_registro_por_filtro_no_existente(self):
        self.assertIsNone(self.repo.obtener_registro_por_filtros(**{"nombre":"no existe"}))


    def test_map_entidad_a_modelo(self):
        usuario = Usuario(
            nombre="A", apellido="B", email="a@b.com", nombre_de_usuario="ab",
            contraseña="123", rol=0, claustro=0, id=1
        )
        modelo = self.repo.map_entidad_a_modelo(usuario)
        self.assertIsInstance(modelo, ModeloUsuario)

    def test_eliminar_registro_por_id_no_existente(self):
        # No debe lanzar error si no existe
        self.repo.eliminar_registro_por_id(9999)

    def test_buscar_usuario(self):
        # Debe devolver None si no existe
        self.assertIsNone(self.repo.obtener_registro_por_filtros(**{"nombre":"usuario no existe"}))

class TestRepositorioReclamosSQLAlchemy(unittest.TestCase):
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
            self.repo.modificar_registro("no es modelo")

    def test_modificar_registro_orm_no_existente(self):
        modelo = ModeloReclamo(
            id=9999, estado="pendiente", fecha_hora=datetime.now(),
            contenido="x", usuario_id=1, clasificacion="a", cantidad_adherentes=0, tiempo_estimado=1
        )
        with self.assertRaises(ValueError):
            self.repo.modificar_registro(modelo)

    def test_obtener_registro_por_filtro_no_existente(self):
    # Este test no debe lanzar errores si no existe el reclamo
        with self.assertRaises(ValueError) as contexto:
            self.repo.obtener_registro_por_filtros(**{"id":9999})

        self.assertIn("NoneType", str(contexto.exception))


    def test_eliminar_registro_por_id_no_existente(self):
        self.repo.eliminar_registro_por_id(9999)  # No debe lanzar error

    def test_buscar_similares(self):
        # No hay reclamos, debe devolver lista vacía
        self.assertEqual(self.repo.buscar_similares("ninguna", 9999), [])

    def test_obtener_registros_por_filtro_no_existente(self):
        self.assertEqual(self.repo.obtener_registros_por_filtro("clasificacion", "noexiste"), [])

    def test_obtener_registros_por_filtro_clasificacion(self):
        # Crear reclamos de prueba
        reclamo1 = ModeloReclamo(
            estado="pendiente", fecha_hora=datetime.now(),
            contenido="Reclamo 1", usuario_id=1, clasificacion="soporte", cantidad_adherentes=2
        )
        reclamo2 = ModeloReclamo(
            estado="pendiente", fecha_hora=datetime.now(),
            contenido="Reclamo 2", usuario_id=2, clasificacion="infraestructura", cantidad_adherentes=1
        )
        self.session.add_all([reclamo1, reclamo2])
        self.session.commit()

        # Filtrar por clasificación
        resultados = self.repo.obtener_registros_por_filtro(filtro="clasificacion", valor="soporte")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].clasificacion, "soporte")

    def test_obtener_registros_por_filtro_estado(self):
        # Crear reclamos de prueba
        reclamo1 = ModeloReclamo(
            estado="resuelto", fecha_hora=datetime.now(),
            contenido="Reclamo 1", usuario_id=1, clasificacion="soporte", cantidad_adherentes=2
        )
        reclamo2 = ModeloReclamo(
            estado="pendiente", fecha_hora=datetime.now(),
            contenido="Reclamo 2", usuario_id=2, clasificacion="infraestructura", cantidad_adherentes=1
        )
        self.session.add_all([reclamo1, reclamo2])
        self.session.commit()

        # Filtrar por estado
        resultados = self.repo.obtener_registros_por_filtro(filtro="estado", valor="resuelto")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].estado, "resuelto")

    def test_mapear_reclamo_a_modelo_y_modelo_a_reclamo(self):
        reclamo = Reclamo(
            id=1, estado="pendiente", fecha_hora=datetime.now(),
            contenido="test", usuario_id=1, clasificacion="a", cantidad_adherentes=0, tiempo_estimado=1
        )
        modelo = self.repo.map_entidad_a_modelo(reclamo)
        self.assertIsInstance(modelo, ModeloReclamo)
        reclamo2 = self.repo.map_modelo_a_entidad(modelo)
        self.assertIsInstance(reclamo2, Reclamo)

    def test_actualizar_reclamo(self):
        reclamo = Reclamo(
            id=None, estado="pendiente", fecha_hora=datetime.now(),
            contenido="test", usuario_id=1, clasificacion="a", cantidad_adherentes=0, tiempo_estimado=1
        )
        modelo = self.repo.map_entidad_a_modelo(reclamo)
        self.repo.guardar_registro(modelo)
        reclamo_db = self.repo.obtener_todos_los_registros()[0]
        reclamo_db_entidad = self.repo.map_modelo_a_entidad(reclamo_db)
        reclamo_db_entidad.estado = "resuelto"
        self.repo.modificar_registro(reclamo_db_entidad)
        reclamo_mod = self.repo.obtener_registro_por_filtros(**{"id":reclamo_db.id})
        self.assertEqual(reclamo_mod.estado, "resuelto")


if __name__ == "__main__":
    unittest.main()

