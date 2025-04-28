# Archivo de test para realizar pruebas unitarias del programa modularizado

import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cajon import Cajon, AnalizadorDeCajon, GeneradorDeInforme
from modules.cinta_transportadora import CintaTransportadora
from modules.sensor import Sensor, DetectorAlimento, FabricaDeAlimentos

class TestAlimentos(unittest.TestCase):
    def test_kiwi_aw(self):
        kiwi = Kiwi(500)  # 500 gramos
        self.assertAlmostEqual(kiwi.aw, 0.96, places=2)

    def test_manzana_aw(self):
        manzana = Manzana(300)  # 300 gramos
        self.assertAlmostEqual(manzana.aw, 0.96, places=2)

    def test_papa_aw(self):
        papa = Papa(400)  # 400 gramos
        self.assertAlmostEqual(papa.aw, 0.96, places=2)

    def test_zanahoria_aw(self):
        zanahoria = Zanahoria(250)  # 250 gramos
        self.assertAlmostEqual(zanahoria.aw, 0.96, places=2)

class TestFabricaDeAlimentos(unittest.TestCase):
    def test_crear_alimento_random(self):
        fabrica = FabricaDeAlimentos()
        alimento = fabrica.crear_alimento_random()
        self.assertIn(type(alimento), [Kiwi, Manzana, Papa, Zanahoria])
        self.assertGreaterEqual(alimento.peso, 0.05)  # Peso mínimo en kg
        self.assertLessEqual(alimento.peso, 0.599)  # Peso máximo en kg

class TestCajon(unittest.TestCase):
    def test_agregar_alimento(self):
        cajon = Cajon(2)  # Capacidad de 2 alimentos
        kiwi = Kiwi(500)
        manzana = Manzana(300)
        cajon.agregar_alimento(kiwi)
        cajon.agregar_alimento(manzana)
        self.assertEqual(len(cajon), 2)

    def test_cajon_lleno(self):
        cajon = Cajon(1)  # Capacidad de 1 alimento
        kiwi = Kiwi(500)
        cajon.agregar_alimento(kiwi)
        with self.assertRaises(Exception) as context:
            cajon.agregar_alimento(Manzana(300))
        self.assertEqual(str(context.exception), "El cajón está lleno.")

    def test_peso_total(self):
        cajon = Cajon(2)
        kiwi = Kiwi(500)
        manzana = Manzana(300)
        cajon.agregar_alimento(kiwi)
        cajon.agregar_alimento(manzana)
        self.assertAlmostEqual(cajon.peso_total(), 0.8)  # 0.5 + 0.3 kg

class TestAnalizadorDeCajon(unittest.TestCase):
    def test_calcular_metricas(self):
        cajon = Cajon(3)
        cajon.agregar_alimento(Kiwi(500))
        cajon.agregar_alimento(Manzana(300))
        cajon.agregar_alimento(Papa(400))
        metricas = AnalizadorDeCajon.calcular_metricas(cajon)
        # self.assertAlmostEqual(metricas["peso_total"], 1.2)  # 0.5 + 0.3 + 0.4 kg
        self.assertGreater(metricas["aw_prom_frutas"], 0)
        self.assertGreater(metricas["aw_prom_verduras"], 0)
        self.assertGreater(metricas["aw_total"], 0)

class TestGeneradorDeInforme(unittest.TestCase):
    def test_generar_advertencias(self):
        metricas = {
            "peso_total": 1.2,
            "aw_prom_frutas": 0.95,
            "aw_prom_verduras": 0.85,
            "aw_total": 0.92
        }
        advertencias = GeneradorDeInforme.generar_advertencias(metricas)
        self.assertIn("Advertencia: La actividad acuosa promedio de las frutas supera 0.90.", advertencias)
        self.assertIn("Advertencia: La actividad acuosa total supera 0.90.", advertencias)

class TestCintaTransportadora(unittest.TestCase):
    def test_iniciar_transporte(self):
        fabrica = FabricaDeAlimentos()
        sensor = Sensor(fabrica)
        cajon = Cajon(3)  # Capacidad de 3 alimentos
        cinta = CintaTransportadora(sensor, cajon)
        cinta.iniciar_transporte()
        self.assertEqual(len(cajon), 3)  # El cajón debe estar lleno

if __name__ == "__main__":
    unittest.main()