import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cajon import Cajon, AnalizadorDeCajon, GeneradorDeInforme
from modules.cinta_transportadora import CintaTransportadora
from modules.sensor import Sensor, DetectorAlimento, FabricaDeAlimentos
import coverage


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

    def test_cajon_iter(self):
        cajon = Cajon(2)
        cajon.agregar_alimento(Kiwi(500))
        cajon.agregar_alimento(Manzana(300))
        alimentos = list(cajon)
        self.assertEqual(len(alimentos), 2)
        self.assertIsInstance(alimentos[0], Kiwi)
        
    def test_cajon_len(self):
        cajon = Cajon(2)
        cajon.agregar_alimento(Kiwi(500))
        self.assertEqual(len(cajon), 1)
        
    
class TestAnalizadorDeCajon(unittest.TestCase):
    def test_calcular_metricas(self):
        cajon = Cajon(3)
        zanahoria = Zanahoria(400)
        manzana = Manzana(300)
        kiwi = Kiwi(500)
        cajon.agregar_alimento(zanahoria)
        cajon.agregar_alimento(manzana)
        cajon.agregar_alimento(kiwi)
        metricas = AnalizadorDeCajon.calcular_metricas(cajon)
        self.assertAlmostEqual(metricas["peso_total"], 1.2)  # 0.5 + 0.3 + 0.4 kg

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
        self.assertNotIn("Advertencia: La actividad acuosa promedio de las verduras supera 0.90.", advertencias)
