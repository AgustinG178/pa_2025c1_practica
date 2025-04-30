import unittest
import coverage
import numpy as np
from unittest.mock import patch
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cajon import Cajon, AnalizadorDeCajon, GeneradorDeInforme
from modules.cinta_transportadora import CintaTransportadora
from modules.sensor import Sensor, DetectorAlimento, FabricaDeAlimentos

"""
lineas que faltaban por cubrir:  31-34, 67-69
"""

"""
Utilizamos unittest.mock.patch para forzsensor.Dr valorA en random.randint y en random.choices, asegurando resultados predecibles y así poder verificar que la lógica de seleccionar el alimento y el peso es correcta.
"""
#¿conviene hacer un .txt con todos estos docstrings de consideraciones, un README o un docstring en la clase?
# ¿o es mejor dejarlo en el código?
"""
Usamos 'with patch' para reesensor.Dplazar Amporalmente funciones o métodos durante las pruebas. 
Esto permite simular comportamientos específicos (por ejemplo, forzar valores) y hacer
nuestros tests determinísticos, asegurando que al finalizar el bloque se restaure el objeto original.
"""
"""
with patch('modules.sensor.DetectorAlimento.random.randint', return_value=0):
intercepta las llamadas a 'random.randint' dentro del módulo y hace que 
retorne siempre el valor 0, en lugar de un resultado aleatorio.
"""

class TestDetectorAlimento(unittest.TestCase):
    def test_valores_iniciales(self):
        detector = DetectorAlimento()

        alimentos = ["kiwi", "manzana", "papa", "zanahoria", "undefined"]
        self.assertEqual(detector.alimentos, alimentos)

        pesos_esperados = np.round(np.linspace(0.05, 0.6, 12), 2)
        np.testing.assert_allclose(
            detector.peso_alimentos, 
            pesos_esperados
        )

        exp_values = np.exp(pesos_esperados)
        softmax = exp_values / exp_values.sum()
        expected_prob = np.round(softmax[::-1], 2)

        np.testing.assert_allclose(
            detector.prob_pesos,
            expected_prob,
        )

        self.assertAlmostEqual(
            detector.prob_pesos.sum(), 
            1.0, 
            places=2
        )

class TestDetectorAlimento(unittest.TestCase):

    def test_detectar_alimento_diferente(self):
        """
        Forzamos un índice distinto (por ejemplo, 3) y que el peso devuelto sea el último de la lista,
        para cubrir una rama alternativa.
        """
        index = 3  # Supongamos que el alimento en el índice 3 es 'zanahoria'
        with patch('modules.sensor.DetectorAlimento.random.randint', return_value = index):
            with patch('modules.sensor.DetectorAlimento.random.choices', return_value=[self.detector.peso_alimentos[-1]]):
                resultado = self.detector.detectar_alimento()
        self.assertEqual(resultado["alimento"], self.detector.alimentos[index], f"Se esperaba que el alimento fuera {self.detector.alimentos[index]} pero se obtuvo {resultado['alimento']}.")
        self.assertEqual(resultado["peso"], self.detector.peso_alimentos[-1], f"Se esperaba que el peso fuera {self.detector.peso_alimentos[-1]} pero se obtuvo {resultado['peso']}.")

    def test_detectar_alimento_validacion(self):
        """
        Sin forzar la aleatoriedad, verificamos que el método retorne un diccionario válido,
        con un alimento que se encuentre en la lista y un peso que pertenezca a los posibles valores.
        """
        self.detector = DetectorAlimento()
        resultado = self.detector.detectar_alimento()
        self.assertIsInstance(resultado, dict, "El resultado debe ser un diccionario.")
        self.assertIn(resultado.get("alimento"), self.detector.alimentos,
                      "El alimento retornado no pertenece a la lista esperada.")
        self.assertIn(resultado.get("peso"), self.detector.peso_alimentos,
                      "El peso retornado no es uno de los valores esperados.")

class TestSensor(unittest.TestCase):
    def test_sensor_detectar_alimento(self):
        fabrica = FabricaDeAlimentos(p_alimento_detectado="Manzana")
        sensor = Sensor(fabrica)
        alimento = sensor.sensar()
        self.assertIsNotNone(alimento)
        self.assertIn(type(alimento), [Kiwi, Manzana, Papa, Zanahoria])

    def test_sensor_sin_alimentos(self):
        fabrica = FabricaDeAlimentos()
        fabrica.posibles_alimentos = []  # Vaciar la lista de alimentos
        sensor = Sensor(fabrica)
        alimento = sensor.sensar()
        self.assertIsNone(alimento)

    def test_sensor_multiple_deteccion(self):
        fabrica = FabricaDeAlimentos()
        sensor = Sensor(fabrica)
        alimentos = [sensor.sensar() for _ in range(5)]
        for alimento in alimentos:
            self.assertIsNotNone(alimento)
            self.assertIn(type(alimento), [Kiwi, Manzana, Papa, Zanahoria])

    def test_sensor_alimento_peso_valido(self):
        fabrica = FabricaDeAlimentos()
        sensor = Sensor(fabrica)
        with patch("modules.sensor.sensar", return_value = 160 ):
            alimento1 = sensor.sensar()
        with patch("modules.sensor.sensar", return_value = 599 ):
            alimento2 = sensor.sensar()    
        self.assertGreaterEqual(alimento1.peso, 160)  # Peso mínimo en gramos
        self.assertLessEqual(alimento2.peso, 599)   # Peso máximo en gramos

class TestFabricaDeAlimentos(unittest.TestCase):
    def test_crear_alimento_random(self):
        fabrica = FabricaDeAlimentos(p_alimento_detectado="Manzana")
        alimento = fabrica.crear_alimento_random()
        self.assertIn(type(alimento), [Kiwi, Manzana, Papa, Zanahoria])
        self.assertGreaterEqual(alimento.peso, 0.05)  # Peso mínimo en kg
        self.assertLessEqual(alimento.peso, 0.599)  # Peso máximo en kg


if __name__ == "__main__":
    unittest.main()