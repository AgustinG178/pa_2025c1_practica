import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from modules.reclamo import Reclamo
from modules.modelos import ModeloReclamo
from modules.gestor_reclamos import GestorReclamo

class DummyUser:
    def __init__(self, id=1, nombre_de_usuario="dummy", rol="1"):
        self.id = id
        self.nombre_de_usuario = nombre_de_usuario
        self.rol = rol

class TestGestorReclamo(unittest.TestCase):
    def setUp(self):
        # Arrange
        self.repositorio = MagicMock()
        self.gestor = GestorReclamo(self.repositorio)
        self.usuario = DummyUser()

    def test_guardar_reclamo(self):
        # Arrange
        reclamo = Reclamo("pendiente", datetime.now(), self.usuario.id, "Fallo", "soporte")
        # Act
        self.gestor.guardar_reclamo(reclamo)
        # Assert
        self.repositorio.mapear_reclamo_a_modelo.assert_called_once()
        self.repositorio.guardar_registro.assert_called_once()

    def test_devolver_reclamo(self):
        # Arrange
        self.repositorio.obtener_registro_por_filtro.return_value = "MockReclamo"
        # Act
        resultado = self.gestor.devolver_reclamo(1)
        # Assert
        self.assertEqual(resultado, "MockReclamo")

    def test_buscar_reclamos_por_filtro(self):
        # Arrange
        self.repositorio.obtener_registros_por_filtro.return_value = ["R1", "R2"]
        # Act
        resultado = self.gestor.buscar_reclamos_por_filtro("estado", "pendiente")
        # Assert
        self.assertEqual(resultado, ["R1", "R2"])

    def test_devolver_reclamos_base_permitido(self):
        # Arrange
        usuario = DummyUser(rol="1")
        self.repositorio.obtener_todos_los_registros.return_value = ["R1"]
        # Act
        resultado = self.gestor.devolver_reclamos_base(usuario)
        # Assert
        self.assertEqual(resultado, ["R1"])

    def test_devolver_reclamos_base_denegado(self):
        # Arrange
        usuario = DummyUser(rol="2")
        # Act & Assert
        with self.assertRaises(PermissionError):
            self.gestor.devolver_reclamos_base(usuario)

    def test_actualizar_estado_reclamo_resolver(self):
        # Arrange
        usuario = DummyUser(rol="2")
        reclamo = Reclamo("pendiente", datetime.now() - timedelta(days=2), usuario.id, "Falla", "hw")
        reclamo.id = 1
        modelo = ModeloReclamo(id=1, tiempo_estimado=3)
        self.repositorio.obtener_registro_por_filtro.return_value = modelo
        # Act
        self.gestor.actualizar_estado_reclamo(usuario, reclamo, "resolver")
        # Assert
        self.repositorio.modificar_registro.assert_called_once()

    def test_actualizar_estado_reclamo_actualizar(self):
        # Arrange
        usuario = DummyUser(rol="2")
        reclamo = Reclamo("pendiente", datetime.now(), usuario.id, "Falla", "hw")
        reclamo.id = 1
        modelo = ModeloReclamo(id=1)
        self.repositorio.obtener_registro_por_filtro.return_value = modelo
        # Act
        self.gestor.actualizar_estado_reclamo(usuario, reclamo, "actualizar", 5)
        # Assert
        self.assertEqual(modelo.tiempo_estimado, 5)
        self.assertEqual(modelo.estado, "en proceso")
        self.repositorio.modificar_registro.assert_called_once()

    def test_invalidar_reclamo(self):
        # Arrange
        self.repositorio.eliminar_registro_por_id.return_value = None
        # Act
        msg = self.gestor.invalidar_reclamo(99)
        # Assert
        self.assertIn("se ha eliminado correctamente", msg)

    def test_obtener_ultimos_reclamos(self):
        # Arrange
        self.repositorio.obtener_ultimos_reclamos.return_value = ["R1", "R2"]
        # Act
        resultado = self.gestor.obtener_ultimos_reclamos(2)
        # Assert
        self.assertEqual(resultado, ["R1", "R2"])

    def test_modificar_reclamo(self):
        # Arrange
        reclamo = Reclamo("pendiente", datetime.now(), 1, "Desc", "tipo")
        # Act
        self.gestor.modificar_reclamo(reclamo)
        # Assert
        self.repositorio.modificar_registro.assert_called_once()

    def test_actualizar_estado_reclamo_excepcion(self):
        # Arrange
        usuario = DummyUser(rol="2")
        reclamo = Reclamo("pendiente", datetime.now(), usuario.id, "Desc", "tipo")
        reclamo.id = 999
        self.repositorio.obtener_registro_por_filtro.side_effect = Exception("DB error")
        # Act
        self.gestor.actualizar_estado_reclamo(usuario, reclamo, "resolver")
        # Assert
        self.repositorio.modificar_registro.assert_not_called()

if __name__ == "__main__":
    unittest.main()
