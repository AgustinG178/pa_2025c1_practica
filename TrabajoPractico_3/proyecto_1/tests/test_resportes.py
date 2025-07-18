import unittest
from unittest.mock import MagicMock
from collections import namedtuple
from modules.reportes import GeneradorReportes

"""
Un mock es un objeto simulado que reemplaza a uno real en pruebas unitarias, 
permitiendo controlar el comportamiento y evitar dependencias externas (DB, APIs, etc).
"""

MockReclamo = namedtuple('MockReclamo', ['estado', 'departamento', 'clasificacion', 'cantidad_adherentes', 'fecha_hora', 'usuario_id'])

class TestGeneradorReportes(unittest.TestCase):
    def setUp(self):
        # Arrange: Crear mock del repositorio y el generador de reportes
        self.mock_repositorio = MagicMock()
        self.generador = GeneradorReportes(self.mock_repositorio)

    def test_cantidad_total_reclamos(self):
        # Arrange: Mockear la consulta para que retorne 5 reclamos
        self.mock_repositorio.session.query.return_value.count.return_value = 5
        
        # Act: Obtener cantidad total de reclamos
        resultado = self.generador.cantidad_total_reclamos()
        
        # Assert: Verificar que se retorna el valor esperado y la consulta se ejecutó
        self.assertEqual(resultado, 5)
        self.mock_repositorio.session.query.assert_called_once()

if __name__ == '__main__':
    unittest.main()
