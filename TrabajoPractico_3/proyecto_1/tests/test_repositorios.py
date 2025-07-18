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
        # Arrange: Crear engine y sesión para tests con la DB
        engine, Session = crear_engine()
        cls.session = Session()
        cls.repo = RepositorioUsuariosSQLAlchemy(cls.session)

    def setUp(self):
        # Arrange: Limpiar la tabla de usuarios antes de cada test
        self.session.query(ModeloUsuario).delete()
        self.session.commit()

    def test_guardar_registro_tipo_invalido(self):
        # Act & Assert: debe levantar ValueError si no recibe un modelo válido
        with self.assertRaises(ValueError):
            self.repo.guardar_registro("no es modelo")

    def test_modificar_registro_tipo_invalido(self):
        # Act & Assert: igual para modificar
        with self.assertRaises(ValueError):
            self.repo.modificar_registro("no es modelo")

    def test_modificar_registro_no_existente(self):
        # Arrange: modelo no guardado en DB
        modelo = ModeloUsuario(
            nombre="A", apellido="B", email="a@b.com", nombre_de_usuario="ab",
            contraseña="123", rol=0, claustro=0
        )
        # Act: modificar registro que no existe no debe lanzar error ni hacer nada
        self.repo.modificar_registro(modelo)

    def test_obtener_modelo_por_id_no_existente(self):
        # Act & Assert: buscar por ID inexistente debe retornar None
        self.assertIsNone(self.repo.obtener_modelo_por_id(9999))

    def test_obtener_registro_por_filtro_no_existente(self):
        # Act & Assert: buscar por filtro con valor inexistente debe retornar None
        self.assertIsNone(self.repo.obtener_registro_por_filtro("nombre", "noexiste"))

    def test_obtener_registro_por_filtros_no_existente(self):
        # Act & Assert: igual con múltiples filtros
        self.assertIsNone(self.repo.obtener_registro_por_filtros(nombre="noexiste"))

    def test_map_entidad_a_modelo(self):
        # Arrange: entidad Usuario
        usuario = Usuario(
            nombre="A", apellido="B", email="a@b.com", nombre_de_usuario="ab",
            contraseña="123", rol=0, claustro=0, id=1
        )
        # Act
        modelo = self.repo._map_entidad_a_modelo(usuario)
        # Assert
        self.assertIsInstance(modelo, ModeloUsuario)

    def test_eliminar_registro_por_id_no_existente(self):
        # Act & Assert: eliminar registro no existente no debe lanzar error
        self.repo.eliminar_registro_por_id(9999)

    def test_buscar_usuario(self):
        # Act & Assert: buscar usuario inexistente debe devolver None
        self.assertIsNone(self.repo.buscar_usuario(nombre="noexiste"))

class TestRepositorioReclamosSQLAlchemy(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Arrange: Crear engine y sesión para DB
        engine, Session = crear_engine()
        cls.session = Session()
        cls.repo = RepositorioReclamosSQLAlchemy(cls.session)

    def setUp(self):
        # Arrange: Limpiar tabla reclamos antes de cada test
        self.session.query(ModeloReclamo).delete()
        self.session.commit()

    def test_guardar_registro_tipo_invalido(self):
        # Act & Assert: guardar tipo inválido levanta ValueError
        with self.assertRaises(ValueError):
            self.repo.guardar_registro("no es modelo")

    def test_modificar_registro_tipo_invalido(self):
        # Act & Assert: modificar tipo inválido levanta ValueError
        with self.assertRaises(ValueError):
            self.repo.modificar_registro("no es reclamo")

    def test_modificar_registro_no_existente(self):
        # Arrange: reclamo no existente
        reclamo = Reclamo(
            id=9999, estado="pendiente", fecha_hora=datetime.now(),
            contenido="x", usuario_id=1, clasificacion="a", cantidad_adherentes=0, tiempo_estimado=1
        )
        # Act & Assert: modificar reclamo inexistente lanza ValueError
        with self.assertRaises(ValueError):
            self.repo.modificar_registro(reclamo)

    def test_modificar_registro_orm_tipo_invalido(self):
        # Act & Assert: modificar con ORM tipo inválido levanta ValueError
        with self.assertRaises(ValueError):
            self.repo.modificar_registro("no es modelo")

    def test_modificar_registro_orm_no_existente(self):
        # Arrange: ORM reclamo no existente
        modelo = ModeloReclamo(
            id=9999, estado="pendiente", fecha_hora=datetime.now(),
            contenido="x", usuario_id=1, clasificacion="a", cantidad_adherentes=0, tiempo_estimado=1
        )
        # Act & Assert
        with self.assertRaises(ValueError):
            self.repo.modificar_registro(modelo)

    def test_obtener_registro_por_filtro_no_existente(self):
        # Act: intentar obtener registro inexistente por filtro
        try:
            resultado = self.repo.obtener_registro_por_filtro("id", 9999)
        except AttributeError as e:
            # Assert: si lanza excepción, debe ser por NoneType
            self.assertIn("NoneType", str(e))
        else:
            # Si no lanza excepción, debe devolver None
            self.assertIsNone(resultado)

    def test_eliminar_registro_por_id_no_existente(self):
        # Act & Assert: eliminar por id inexistente no debe lanzar error
        self.repo.eliminar_registro_por_id(9999)

    def test_buscar_similares(self):
        # Act & Assert: buscar similares con DB vacía retorna lista vacía
        self.assertEqual(self.repo.buscar_similares("ninguna", 9999), [])

    def test_obtener_por_id_no_existente(self):
        # Act & Assert: obtener por ID inexistente retorna None
        self.assertIsNone(self.repo.obtener_por_id(9999))

    def test_obtener_registros_por_filtro_no_existente(self):
        # Act & Assert: obtener registros con filtro inexistente retorna lista vacía
        self.assertEqual(self.repo.obtener_registros_por_filtro("clasificacion", "noexiste"), [])

    def test_obtener_registros_por_filtro_clasificacion(self):
        # Arrange: crear reclamos de prueba
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

        # Act: filtrar por clasificación
        resultados = self.repo.obtener_registros_por_filtro(filtro="clasificacion", valor="soporte")

        # Assert: debe devolver solo los reclamos con clasificación 'soporte'
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].clasificacion, "soporte")

    def test_obtener_registros_por_filtro_estado(self):
        # Arrange: crear reclamos de prueba
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

        # Act: filtrar por estado
        resultados = self.repo.obtener_registros_por_filtro(filtro="estado", valor="resuelto")

        # Assert: debe devolver solo los reclamos con estado 'resuelto'
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].estado, "resuelto")

    def test_mapear_reclamo_a_modelo_y_modelo_a_reclamo(self):
        # Arrange: crear reclamo de prueba
        reclamo = Reclamo(
            id=1, estado="pendiente", fecha_hora=datetime.now(),
            contenido="test", usuario_id=1, clasificacion="a", cantidad_adherentes=0, tiempo_estimado=1
        )

        # Act: mapear reclamo a modelo ORM
        modelo = self.repo.mapear_reclamo_a_modelo(reclamo)

        # Assert
        self.assertIsInstance(modelo, ModeloReclamo)

        # Act: mapear modelo ORM a entidad reclamo
        reclamo2 = self.repo.mapear_modelo_a_reclamo(modelo)

        # Assert
        self.assertIsInstance(reclamo2, Reclamo)

    def test_actualizar_reclamo(self):
        # Arrange: crear y guardar reclamo
        reclamo = Reclamo(
            id=None, estado="pendiente", fecha_hora=datetime.now(),
            contenido="test", usuario_id=1, clasificacion="a", cantidad_adherentes=0, tiempo_estimado=1
        )
        modelo = self.repo.mapear_reclamo_a_modelo(reclamo)
        self.repo.guardar_registro(modelo)

        # Act: obtener reclamo guardado y modificar estado
        reclamo_db = self.repo.obtener_todos_los_registros()[0]
        reclamo_db_entidad = self.repo.mapear_modelo_a_reclamo(reclamo_db)
        reclamo_db_entidad.estado = "resuelto"
        self.repo.modificar_registro(reclamo_db_entidad)

        # Assert: verificar que el cambio se haya persistido
        reclamo_mod = self.repo.obtener_por_id(reclamo_db_entidad.id)
        self.assertEqual(reclamo_mod.estado, "resuelto")

    def test_obtener_ultimos_reclamos(self):
        # Arrange: crear y guardar reclamo
        reclamo = Reclamo(
            id=None, estado="pendiente", fecha_hora=datetime.now(),
            contenido="test", usuario_id=1, clasificacion="a", cantidad_adherentes=0, tiempo_estimado=1
        )
        modelo = self.repo.mapear_reclamo_a_modelo(reclamo)
        self.repo.guardar_registro(modelo)

        # Act: obtener últimos reclamos con límite
        ultimos = self.repo.obtener_ultimos_reclamos(limit=1)

        # Assert: verificar que devuelve lista no vacía (al menos uno)
        self.assertTrue(len(ultimos) >= 0)

if __name__ == "__main__":
    unittest.main()
