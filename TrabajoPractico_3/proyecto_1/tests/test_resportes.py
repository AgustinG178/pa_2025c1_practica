import pytest
import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from collections import namedtuple
from modules.reportes import GeneradorReportes
from modules.modelos import ModeloReclamo

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

    def test_cantidad_promedio_adherentes(self):
        # Simulamos que avg devuelve 10.5
        self.mock_repositorio.session.query.return_value.scalar.return_value = 10.5
        
        resultado = self.generador.cantidad_promedio_adherentes()
        
        self.assertEqual(resultado, 10.5)
        self.mock_repositorio.session.query.assert_called_once()

    def test_reclamos_recientes(self):
        # Simulamos que la consulta devuelve una lista de reclamos
        reclamos_simulados = ['reclamo1', 'reclamo2']
        self.mock_repositorio.session.query.return_value.filter.return_value.all.return_value = reclamos_simulados
        
        resultado = self.generador.reclamos_recientes(dias=7)
        
        self.assertEqual(resultado, reclamos_simulados)
        self.mock_repositorio.session.query.assert_called_once()
        self.mock_repositorio.session.query.return_value.filter.assert_called_once()

if __name__ == '__main__':
    unittest.main()
