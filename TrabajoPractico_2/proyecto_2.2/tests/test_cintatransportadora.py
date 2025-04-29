import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cajon import Cajon, AnalizadorDeCajon, GeneradorDeInforme
from modules.cinta_transportadora import CintaTransportadora, logger
from modules.sensor import Sensor, DetectorAlimento, FabricaDeAlimentos
import coverage
import logging
from unittest.mock import patch

logger = logging.getLogger("modules.cinta_transportadora")

class TestCintaTransportadora(unittest.TestCase):
    def test_iniciar_transporte(self):
        fabrica = FabricaDeAlimentos()
        sensor = Sensor(fabrica)
        cajon = Cajon(3)  # Capacidad de 3 alimentos
        cinta = CintaTransportadora(sensor, cajon)
        cinta.iniciar_transporte()
        self.assertEqual(len(cajon), 3)  # El cajón debe estar lleno

    def test_cinta_detener_transporte(self):
        fabrica = FabricaDeAlimentos(p_alimento_detectado="Manzana")
        sensor = Sensor(fabrica)
        cajon = Cajon(1)  # Capacidad de 1 alimento
        cinta = CintaTransportadora(sensor, cajon)
        cinta.iniciar_transporte()
        self.assertEqual(len(cajon), 1)

    def test_cinta_no_agrega_si_cajon_lleno(self):
        fabrica = FabricaDeAlimentos()
        sensor = Sensor(fabrica)
        cajon = Cajon(1)  # Solo un alimento permitido
        cinta = CintaTransportadora(sensor, cajon)

        primer_alimento = sensor.sensar()
        cajon.agregar_alimento(primer_alimento)  # Llenamos el cajón

        cinta.iniciar_transporte(max_intentos=10)

        # Aseguramos que el cajón no superó su capacidad
        self.assertEqual(len(cajon.alimentos), 1)
    
    def test_cinta_excepcion_loggeada(self):
        fabrica = FabricaDeAlimentos()
        sensor = Sensor(fabrica)
        cajon = Cajon(1)
        cinta = CintaTransportadora(sensor, cajon)

        # Llenamos el cajón para forzar el error al agregar otro alimento.
        primer_alimento = sensor.sensar()
        cajon.agregar_alimento(primer_alimento)
        
        # Forzamos la ejecución del bucle ignorando la condición de detención.
        cinta.detener_transporte = lambda: False

        with self.assertLogs(level='ERROR') as log:
            cinta.iniciar_transporte(max_intentos=10)

        # Verificamos que se haya registrado el mensaje de error esperado.
        self.assertTrue(any("Error al agregar alimento" in mensaje for mensaje in log.output))

    def test_cinta_sin_alimentos(self):
        fabrica = FabricaDeAlimentos([])
        sensor = Sensor(fabrica)
        cajon = Cajon(5)
        cinta = CintaTransportadora(sensor, cajon)

        cinta.iniciar_transporte(max_intentos=10)

        self.assertEqual(len(cajon.alimentos), 0)

class TestCintaTransportadora(unittest.TestCase):
    def test_cinta_excepcion_al_agregar(self):
        fabrica = FabricaDeAlimentos()
        sensor = Sensor(fabrica)
        cajon = Cajon(1)
        cinta = CintaTransportadora(sensor, cajon)

        # Llenamos el cajón para provocar fallo al agregar otro alimento.
        primer_alimento = sensor.sensar()
        cajon.agregar_alimento(primer_alimento)

        # Forzamos que el bucle nunca se detenga
        cinta.detener_transporte = lambda: False

        # Forzamos que cada intento de agregar alimento lance excepción
        with patch.object(cajon, 'agregar_alimento', side_effect=Exception("Cajón lleno")):
            # Capturamos todos los logs a nivel ERROR
            with self.assertLogs(level='ERROR') as log:
                cinta.iniciar_transporte(max_intentos=10)

        # Verificamos que se haya registrado el error esperado
        self.assertTrue(
            any("Error al agregar alimento" in mensaje for mensaje in log.output),
            f"No se encontró 'Error al agregar alimento' en los logs: {log.output}"
        )

    def test_cinta_max_intentos(self):
        fabrica = FabricaDeAlimentos()
        sensor = Sensor(fabrica)
        cajon = Cajon(1)  # Capacidad de 1 alimento
        cinta = CintaTransportadora(sensor, cajon)

        cinta.iniciar_transporte(max_intentos=1)  # Forzar el límite de intentos
        self.assertEqual(len(cajon.alimentos), 1)  # No se debe agregar ningún alimento

if __name__ == "__main__":
    unittest.main()
    print(logging.getLevelName(logger))

    