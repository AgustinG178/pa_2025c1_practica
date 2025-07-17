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
        self.repositorio = MagicMock()
        self.gestor = GestorReclamo(self.repositorio)
        self.usuario = DummyUser()

    def test_guardar_reclamo(self):
        reclamo = Reclamo("pendiente", datetime.now(), self.usuario.id, "Fallo", "soporte")
        self.gestor.guardar_reclamo(reclamo)
        self.repositorio.mapear_reclamo_a_modelo.assert_called_once()
        self.repositorio.guardar_registro.assert_called_once()

    def test_devolver_reclamo(self):
        self.repositorio.obtener_registro_por_filtro.return_value = "MockReclamo"
        resultado = self.gestor.devolver_reclamo(1)
        self.assertEqual(resultado, "MockReclamo")

    def test_buscar_reclamos_por_filtro(self):
        self.repositorio.obtener_registros_por_filtro.return_value = ["R1", "R2"]
        resultado = self.gestor.buscar_reclamos_por_filtro("estado", "pendiente")
        self.assertEqual(resultado, ["R1", "R2"])

    def test_devolver_reclamos_base_permitido(self):
        usuario = DummyUser(rol="1")
        self.repositorio.obtener_todos_los_registros.return_value = ["R1"]
        resultado = self.gestor.devolver_reclamos_base(usuario)
        self.assertEqual(resultado, ["R1"])

    def test_devolver_reclamos_base_denegado(self):
        usuario = DummyUser(rol="2")
        with self.assertRaises(PermissionError):
            self.gestor.devolver_reclamos_base(usuario)

    def test_actualizar_estado_reclamo_resolver(self):
        usuario = DummyUser(rol="2")
        reclamo = Reclamo("pendiente", datetime.now() - timedelta(days=2), usuario.id, "Falla", "hw")
        reclamo.id = 1
        modelo = ModeloReclamo(id=1, tiempo_estimado=3)
        self.repositorio.obtener_registro_por_filtro.return_value = modelo
        self.gestor.actualizar_estado_reclamo(usuario, reclamo, "resolver")
        self.repositorio.modificar_registro.assert_called_once()

    def test_actualizar_estado_reclamo_actualizar(self):
        usuario = DummyUser(rol="2")
        reclamo = Reclamo("pendiente", datetime.now(), usuario.id, "Falla", "hw")
        reclamo.id = 1
        modelo = ModeloReclamo(id=1)
        self.repositorio.obtener_registro_por_filtro.return_value = modelo
        self.gestor.actualizar_estado_reclamo(usuario, reclamo, "actualizar", 5)
        self.assertEqual(modelo.tiempo_estimado, 5)
        self.assertEqual(modelo.estado, "en proceso")
        self.repositorio.modificar_registro.assert_called_once()

    def test_invalidar_reclamo(self):
        self.repositorio.eliminar_registro_por_id.return_value = None
        msg = self.gestor.invalidar_reclamo(99)
        self.assertIn("se ha eliminado correctamente", msg)

    def test_obtener_ultimos_reclamos(self):
        self.repositorio.obtener_ultimos_reclamos.return_value = ["R1", "R2"]
        resultado = self.gestor.obtener_ultimos_reclamos(2)
        self.assertEqual(resultado, ["R1", "R2"])

    def test_modificar_reclamo(self):
        reclamo = Reclamo("pendiente", datetime.now(), 1, "Desc", "tipo")
        self.gestor.modificar_reclamo(reclamo)
        self.repositorio.modificar_registro.assert_called_once()

    def test_actualizar_estado_reclamo_excepcion(self):
        usuario = DummyUser(rol="2")
        reclamo = Reclamo("pendiente", datetime.now(), usuario.id, "Desc", "tipo")
        reclamo.id = 999
        self.repositorio.obtener_registro_por_filtro.side_effect = Exception("DB error")

        self.gestor.actualizar_estado_reclamo(usuario, reclamo, "resolver")

        self.repositorio.modificar_registro.assert_not_called()


if __name__ == "__main__":
    unittest.main()