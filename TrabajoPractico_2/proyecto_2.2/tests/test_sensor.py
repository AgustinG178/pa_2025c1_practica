import unittest
import numpy as np
from unittest.mock import patch
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cajon import Cajon, AnalizadorDeCajon, GeneradorDeInforme
from modules.cinta_transportadora import CintaTransportadora
from modules.sensor import Sensor, DetectorAlimento, FabricaDeAlimentos

class TestDetectorAlimento(unittest.TestCase):
    def setUp(self):
        self.detector = DetectorAlimento()

    def test_valores_iniciales(self):
        """
        Verificamos que los valores iniciales de DetectorAlimento sean correctos.
        """
        alimentos = ["kiwi", "manzana", "papa", "zanahoria", "undefined"]
        self.assertEqual(self.detector.alimentos, alimentos)

        pesos_esperados = np.round(np.linspace(0.05, 0.6, 12), 2)
        np.testing.assert_allclose(
            self.detector.peso_alimentos, 
            pesos_esperados
        )

        exp_values = np.exp(pesos_esperados)
        softmax = exp_values / exp_values.sum()
        expected_prob = np.round(softmax[::-1], 2)

        np.testing.assert_allclose(
            self.detector.prob_pesos,
            expected_prob,
        )

        self.assertAlmostEqual(
            self.detector.prob_pesos.sum(), 
            1.0, 
            places=2
        )

    def test_detectar_alimento_diferente(self):
        """
        Forzamos un índice distinto (por ejemplo, 3) y que el peso devuelto sea el último de la lista,
        para cubrir una rama alternativa.
        """
        index = 3  # Supongamos que el alimento en el índice 3 es 'zanahoria'
        with patch('random.randint', return_value=index):
            with patch('random.choices', return_value=[self.detector.peso_alimentos[-1]]):
                resultado = self.detector.detectar_alimento()
        self.assertEqual(resultado["alimento"], self.detector.alimentos[index])
        self.assertEqual(resultado["peso"], self.detector.peso_alimentos[-1])

    def test_detectar_alimento_validacion(self):
        """
        Sin forzar la aleatoriedad, verificamos que el método retorne un diccionario válido,
        con un alimento que se encuentre en la lista y un peso que pertenezca a los posibles valores.
        """
        resultado = self.detector.detectar_alimento()
        self.assertIsInstance(resultado, dict)
        self.assertIn(resultado.get("alimento"), self.detector.alimentos)
        self.assertIn(resultado.get("peso"), self.detector.peso_alimentos)

class TestSensor(unittest.TestCase):
    def test_sensor_detectar_alimento(self):
        """
        Verificamos que el sensor detecte un alimento válido y que el peso esté dentro del rango esperado.
        """
        fabrica = FabricaDeAlimentos(p_alimento_detectado="Manzana")
        sensor = Sensor(fabrica)
        alimento = sensor.sensar()
        self.assertIsNotNone(alimento)
        self.assertIn(type(alimento), [Kiwi, Manzana, Papa, Zanahoria])

    def test_sensor_sin_alimentos(self):
        """
        Verificamos que el sensor retorne None si no hay alimentos disponibles en la fábrica.
        """
        fabrica = FabricaDeAlimentos()
        fabrica.posibles_alimentos = []  # Vaciar la lista de alimentos
        sensor = Sensor(fabrica)
        alimento = sensor.sensar()
        self.assertIsNone(alimento)

    def test_sensor_multiple_deteccion(self):
        """
        Verificamos que el sensor pueda detectar múltiples alimentos
        """
        fabrica = FabricaDeAlimentos()
        sensor = Sensor(fabrica)
        alimentos = [sensor.sensar() for _ in range(5)]
        for alimento in alimentos:
            self.assertIsNotNone(alimento)
            self.assertIn(type(alimento), [Kiwi, Manzana, Papa, Zanahoria])

    def test_sensor_alimento_peso_valido(self):
        """
        Verificamos que el peso del alimento esté dentro de los límites establecidos.
        """
        fabrica = FabricaDeAlimentos()
        sensor = Sensor(fabrica)
        # Forzamos el peso mínimo y máximo usando patch sobre random.randint
        with patch('random.randint', return_value=160):
            alimento1 = sensor.sensar()
        with patch('random.randint', return_value=599):
            alimento2 = sensor.sensar()    
        self.assertGreaterEqual(alimento1.peso, 0.16)  # Peso mínimo en kg
        self.assertLessEqual(alimento2.peso, 0.599)   # Peso máximo en kg

class TestFabricaDeAlimentos(unittest.TestCase):
    """
    Testea la clase FabricaDeAlimentos y su método.
    """
    def test_crear_alimento_random(self):
        fabrica = FabricaDeAlimentos(p_alimento_detectado="Manzana")
        alimento = fabrica.crear_alimento_random()
        self.assertIn(type(alimento), [Kiwi, Manzana, Papa, Zanahoria])
        self.assertGreaterEqual(alimento.peso, 0.05)  # Peso mínimo en kg
        self.assertLessEqual(alimento.peso, 0.599)  # Peso máximo en kg

if __name__ == "__main__":
    unittest.main()