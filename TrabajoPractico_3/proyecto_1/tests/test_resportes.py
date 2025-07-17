import unittest
from unittest.mock import MagicMock
from collections import namedtuple
from modules.reportes import GeneradorReportes

"""Un mock es un objeto "falso" que simula el comportamiento de otro objeto real, pero de forma controlada y predecible, para poder hacer pruebas unitarias sin depender de componentes externos (como bases de datos, APIs, archivos, etc)."""

MockReclamo = namedtuple('MockReclamo', ['estado', 'departamento', 'clasificacion', 'cantidad_adherentes', 'fecha_hora', 'usuario_id'])

# Asumimos que GeneradorReportes ya está importada

class TestGeneradorReportes(unittest.TestCase):
    def setUp(self):
        # Crear un mock del repositorio con una sesión simulada
        self.mock_repositorio = MagicMock()
        self.generador = GeneradorReportes(self.mock_repositorio)

    def test_cantidad_total_reclamos(self):
        # Configuramos el mock para que la consulta retorne 5 reclamos
        self.mock_repositorio.session.query.return_value.count.return_value = 5
        
        resultado = self.generador.cantidad_total_reclamos()
        
        self.assertEqual(resultado, 5)
        self.mock_repositorio.session.query.assert_called_once()

if __name__ == '__main__': #pragma: no cover
    unittest.main()
