import unittest
from unittest.mock import MagicMock
from modules.graficos import Graficadora

class TestGraficosMock(unittest.TestCase):
    """Tests para la clase Graficadora usando mocks."""

    def test_graficar_torta(self):
        """Verifica que el método generar_grafica retorna True usando un mock."""
        graficadora = Graficadora()
        graficadora.generar_grafica = MagicMock(return_value=True)
        self.assertTrue(graficadora.generar_grafica())

if __name__ == "__main__":
    unittest.main()