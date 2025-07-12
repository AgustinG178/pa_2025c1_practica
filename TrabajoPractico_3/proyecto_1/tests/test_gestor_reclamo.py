import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from modules.reclamo import Reclamo
from modules.modelos import ModeloUsuario, ModeloReclamo
from modules.gestor_reclamos import GestorReclamo

class DummyUser:
    def __init__(self, id=1, nombre_de_usuario="dummy", rol="1"):
        self.id = id
        self.nombre_de_usuario = nombre_de_usuario
        self.rol = rol

class TestGestorReclamoExtra(unittest.TestCase):
    def setUp(self):
        self.repositorio_reclamo = MagicMock()
        self.gestor = GestorReclamo(self.repositorio_reclamo)
        self.usuario = DummyUser()

    def test_guardar_reclamo(self):
        reclamo = Reclamo("pendiente", datetime.now(), self.usuario.id, "Fallo", "soporte")
        self.gestor.guardar_reclamo(reclamo)
        self.repositorio_reclamo.map_entidad_a_modelo.assert_called_once()
        self.repositorio_reclamo.guardar_registro.assert_called_once()

    def test_devolver_reclamo(self):
        self.repositorio_reclamo.obtener_registro_por_filtros.return_value = "MockReclamo"
        resultado = self.gestor.buscar_reclamo_por_filtro("id", 1)
        self.assertEqual(resultado, "MockReclamo")

    def test_buscar_reclamos_por_filtro(self):

        self.repositorio_reclamo.obtener_registros_por_filtro.return_value = ["R1","R2"]
        
        resultado = self.gestor.buscar_reclamos_por_filtro("estado", "pendiente")

        self.assertEqual(resultado, ["R1", "R2"])

    def test_devolver_reclamos_base_permitido(self):
        usuario = DummyUser(rol="1")
        self.repositorio_reclamo.obtener_todos_los_registros.return_value = ["R1"]
        resultado = self.gestor.devolver_reclamos_base(usuario)
        self.assertEqual(resultado, ["R1"])

    def test_devolver_reclamos_base_denegado(self):
        usuario = DummyUser(rol="2")
        with self.assertRaises(PermissionError):
            self.gestor.devolver_reclamos_base(usuario)

    def test_buscar_reclamos_similares(self):
        self.repositorio_reclamo.buscar_similares.return_value = ["Sim1"]
        resultado = self.gestor.buscar_reclamos_similares("soporte", 1)
        self.assertEqual(resultado, ["Sim1"])

    def test_actualizar_estado_reclamo_resolver(self):
        usuario = DummyUser(rol="2")
        reclamo = Reclamo("pendiente", datetime.now() - timedelta(days=2), usuario.id, "Falla", "hw",id=1)
        modelo = ModeloReclamo(id=1, tiempo_estimado=3)
        self.repositorio_reclamo.obtener_registro_por_filtros.return_value = modelo
        self.gestor.actualizar_estado_reclamo(usuario, reclamo, "resolver")
        self.repositorio_reclamo.modificar_registro.assert_called_once()

    def test_actualizar_estado_reclamo_actualizar(self):
        usuario = DummyUser(rol="2")
        reclamo = Reclamo("pendiente", datetime.now(), usuario.id, "Falla", "hw",id=1)
        modelo = ModeloReclamo(id=1)
        self.repositorio_reclamo.obtener_registro_por_filtros.return_value = modelo
        self.gestor.actualizar_estado_reclamo(usuario, reclamo, "actualizar", 5)

        self.assertEqual(modelo.tiempo_estimado, 5)
        self.assertEqual(modelo.estado, "en proceso")
        self.repositorio_reclamo.modificar_registro.assert_called_once()

    def test_invalidar_reclamo(self):
        self.repositorio_reclamo.eliminar_registro_por_id.return_value = None
        from modules.gestor_imagen_reclamo import GestorImagenReclamo
        gestor_imagen = MagicMock(spec=GestorImagenReclamo)
        msg = self.gestor.invalidar_reclamo(99,gestor_imagen=gestor_imagen)
        self.assertIn("se ha eliminado correctamente", msg)


    def test_derivar_reclamo(self):
        reclamo = Reclamo("pendiente", datetime.now(), "Desc", "tipo", id=1)
        nuevo_departamento = "nuevo_depto"
        self.gestor.modificar_reclamo(reclamo.id,nuevo_dpto=nuevo_departamento)
        self.repositorio_reclamo.modificar_registro.assert_called_once()

    def test_modificar_reclamo(self):
        reclamo = Reclamo("pendiente", datetime.now(), "Desc", "tipo", id=1)
        clasificador = MagicMock()
        clasificador.clasificar.return_value = "nueva_clasificacion"
        self.gestor.modificar_reclamo(reclamo.id, nuevo_contenido="Nuevo contenido",clasificador=clasificador)
        self.repositorio_reclamo.modificar_registro.assert_called_once()
        #buscamos el reclamo modificado
        reclamo_modificado = self.repositorio_reclamo.obtener_registro_por_filtro.return_value = Reclamo("pendiente", datetime.now(), "Nuevo contenido", "nueva_clasificacion", id=1)
        self.assertEqual(reclamo_modificado.contenido, "Nuevo contenido")
        self.assertEqual(reclamo_modificado.clasificacion, "nueva_clasificacion")

    def test_actualizar_estado_reclamo_excepcion(self):
        usuario = DummyUser(rol="2")
        reclamo = Reclamo("pendiente", datetime.now(), usuario.id, "Desc", "tipo",id=999)
        self.repositorio_reclamo.obtener_registro_por_filtros.side_effect = Exception("DB error")

        self.gestor.actualizar_estado_reclamo(usuario, reclamo, "resolver")

        self.repositorio_reclamo.modificar_registro.assert_not_called()


if __name__ == "__main__":
    unittest.main()