import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria, Alimento
from modules.cajon import Cajon, AnalizadorDeCajon, GeneradorDeInforme
from modules.cinta_transportadora import CintaTransportadora
from modules.sensor import Sensor, DetectorAlimento, FabricaDeAlimentos
import coverage
import random

class TestAlimentos(unittest.TestCase):
    def test_kiwi_aw(self):
        kiwi = Kiwi(500)  # 500 gramos
        self.assertAlmostEqual(kiwi.aw, 0.96, places=2)

    def test_manzana_aw(self):
        manzana = Manzana(300)  # 300 gramos
        self.assertAlmostEqual(manzana.aw, 0.951, places=2)  # Ajustar el valor esperado

    def test_papa_aw(self):
        papa = Papa(400)  # 400 gramos
        self.assertAlmostEqual(papa.aw, 0.96, places=2)

    def test_zanahoria_aw(self):
        zanahoria = Zanahoria(250)  # 250 gramos
        self.assertAlmostEqual(zanahoria.aw, 0.94, places=2)
        
    def test_inicializacion_alimentos(self):
        kiwi = Kiwi(500)
        manzana = Manzana(300)
        papa = Papa(400)
        zanahoria = Zanahoria(250)

        self.assertEqual(kiwi.nombre, "kiwi")
        self.assertEqual(manzana.nombre, "manzana")
        self.assertEqual(papa.nombre, "papa")
        self.assertEqual(zanahoria.nombre, "zanahoria")

    def test_alimento_str(self):
        kiwi = Kiwi(500)
        manzana = Manzana(300)
        papa = Papa(400)
        zanahoria = Zanahoria(250)

        self.assertEqual(str(kiwi), "Kiwi (fruta) - 0.5 kg (aw: 0.96)")
        self.assertEqual(str(manzana), "Manzana (fruta) - 0.3 kg (aw: 0.96)")
        self.assertEqual(str(papa), "Papa (verdura) - 0.4 kg (aw: 0.96)")
        self.assertEqual(str(zanahoria), "Zanahoria (verdura) - 0.25 kg (aw: 0.94)")

    def test_calcular_aw(self):
        kiwi = Kiwi(500)
        manzana = Manzana(300)
        papa = Papa(400)
        zanahoria = Zanahoria(250)

        self.assertAlmostEqual(kiwi.calcular_aw(), 0.96, places=2)
        self.assertAlmostEqual(manzana.calcular_aw(), 0.96, places=2)
        self.assertAlmostEqual(papa.calcular_aw(), 0.96, places=2)
        self.assertAlmostEqual(zanahoria.calcular_aw(), 0.94, places=2)

    def test_peso_extremo(self):
        kiwi_min = Kiwi(50)  # Peso mínimo
        kiwi_max = Kiwi(599)  # Peso máximo

        self.assertAlmostEqual(kiwi_min.aw, 0.96, places=2)
        self.assertAlmostEqual(kiwi_max.aw, 0.96, places=2)

    def test_alimento_base(self):
        class MockAlimento(Alimento):
            def calcular_aw(self):
                return 0.5

            @property
            def aw(self):
                return self.calcular_aw()

        mock_alimento = MockAlimento("mock", "tipo", 1.0)
        self.assertEqual(mock_alimento.nombre, "mock")
        self.assertEqual(mock_alimento.tipo, "tipo")
        self.assertEqual(mock_alimento.peso, 1.0)
        self.assertEqual(mock_alimento.aw, 0.5)
        self.assertEqual(str(mock_alimento), "Mock (tipo) - 1.0 kg")

    def test_zanahoria_str(self):
        zanahoria = Zanahoria(250)
        self.assertEqual(str(zanahoria), "Zanahoria (verdura) - 0.25 kg (aw: 0.94)")

    def test_pesos_extremos_subclases(self):
        kiwi_min = Kiwi(50)
        kiwi_max = Kiwi(599)
        manzana_min = Manzana(50)
        manzana_max = Manzana(599)
        papa_min = Papa(50)
        papa_max = Papa(599)
        zanahoria_min = Zanahoria(50)
        zanahoria_max = Zanahoria(599)

        self.assertAlmostEqual(kiwi_min.aw, 0.96, places=2)
        self.assertAlmostEqual(kiwi_max.aw, 0.96, places=2)
        self.assertAlmostEqual(manzana_min.aw, 0.96, places=2)
        self.assertAlmostEqual(manzana_max.aw, 0.96, places=2)
        self.assertAlmostEqual(papa_min.aw, 0.96, places=2)
        self.assertAlmostEqual(papa_max.aw, 0.96, places=2)
        self.assertAlmostEqual(zanahoria_min.aw, 0.94, places=2)
        self.assertAlmostEqual(zanahoria_max.aw, 0.94, places=2)

if "__name__" == "__main__":
    unittest.main()
    coverage.process_startup()