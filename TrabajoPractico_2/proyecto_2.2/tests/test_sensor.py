import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cajon import Cajon, AnalizadorDeCajon, GeneradorDeInforme
from modules.cinta_transportadora import CintaTransportadora
from modules.sensor import Sensor, DetectorAlimento, FabricaDeAlimentos
import coverage

class TestSensor(unittest.TestCase):
    def test_sensor_detectar_alimento(self):
        # Configurar la fábrica y el sensor
        fabrica = FabricaDeAlimentos(p_alimento_detectado="Manzana")
        sensor = Sensor(fabrica)

        # Detectar un alimento
        alimento = sensor.sensar()

        # Verificar que se detectó un alimento válido
        self.assertIsNotNone(alimento)
        self.assertIn(type(alimento), [Kiwi, Manzana, Papa, Zanahoria])

    def test_sensor_sin_alimentos(self):
        # Configurar la fábrica sin alimentos
        fabrica = FabricaDeAlimentos()
        fabrica.posibles_alimentos = []  # Vaciar la lista de alimentos
        sensor = Sensor(fabrica)

        # Intentar detectar un alimento
        alimento = sensor.sensar()

        # Verificar que no se detectó ningún alimento
        self.assertIsNone(alimento)

    def test_sensor_multiple_deteccion(self):
        # Configurar la fábrica y el sensor
        fabrica = FabricaDeAlimentos()
        sensor = Sensor(fabrica)

        # Detectar múltiples alimentos
        alimentos = [sensor.sensar() for _ in range(5)]

        # Verificar que se detectaron alimentos válidos
        for alimento in alimentos:
            self.assertIsNotNone(alimento)
            self.assertIn(type(alimento), [Kiwi, Manzana, Papa, Zanahoria])

    def test_sensor_alimento_peso_valido(self):
        # Configurar la fábrica y el sensor
        fabrica = FabricaDeAlimentos()
        sensor = Sensor(fabrica)

        # Detectar un alimento
        alimento = sensor.sensar()

        # Verificar que el peso del alimento está dentro del rango esperado
        self.assertGreaterEqual(alimento.peso, 50)  # Peso mínimo en gramos
        self.assertLessEqual(alimento.peso, 599)   # Peso máximo en gramos

class TestFabricaDeAlimentos(unittest.TestCase):
    def test_crear_alimento_random(self):
        fabrica = FabricaDeAlimentos(p_alimento_detectado="Manzana")
        alimento = fabrica.crear_alimento_random()
        self.assertIn(type(alimento), [Kiwi, Manzana, Papa, Zanahoria])
        self.assertGreaterEqual(alimento.peso, 0.05)  # Peso mínimo en kg
        self.assertLessEqual(alimento.peso, 0.599)  # Peso máximo en kg


if __name__ == "__main__":
    unittest.main()