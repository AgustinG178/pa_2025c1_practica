import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cajon import Cajon, AnalizadorDeCajon, GeneradorDeInforme
from modules.cinta_transportadora import CintaTransportadora, logger
from modules.sensor import Sensor, DetectorAlimento, FabricaDeAlimentos
import coverage
import logging
from unittest.mock import patch

"""
Este módulo contiene pruebas unitarias para la clase CintaTransportadora.

Utiliza la biblioteca estándar `logging` de Python para verificar el comportamiento del sistema
cuando ocurren errores durante el proceso de transporte. `logging` permite registrar mensajes de diferentes
niveles (DEBUG, INFO, WARNING, ERROR, CRITICAL) y es útil para detectar fallos, monitorear ejecución,
y generar informes detallados sin interrumpir el flujo del programa.
"""


logger = logging.getLogger("modules.cinta_transportadora")

class TestCintaTransportadora(unittest.TestCase):
    def test_iniciar_transporte(self):
        """
        Verifica que la cinta transportadora agregue correctamente alimentos hasta llenar el cajón.
        """
        fabrica = FabricaDeAlimentos()
        sensor = Sensor(fabrica)
        cajon = Cajon(3)  # Capacidad de 3 alimentos
        cinta = CintaTransportadora(sensor, cajon)
        cinta.iniciar_transporte()
        self.assertEqual(len(cajon), 3)  # El cajón debe estar lleno

    def test_cinta_detener_transporte(self):
        """
        Comprueba que la cinta se detenga al alcanzar la capacidad máxima del cajón.
        """
        fabrica = FabricaDeAlimentos(p_alimento_detectado="Manzana")
        sensor = Sensor(fabrica)
        cajon = Cajon(1)  # Capacidad de 1 alimento
        cinta = CintaTransportadora(sensor, cajon)
        cinta.iniciar_transporte()
        self.assertEqual(len(cajon), 1)

    def test_cinta_no_agrega_si_cajon_lleno(self):
        """
        Asegura que no se agreguen alimentos adicionales si el cajón ya está lleno antes de iniciar.
        """
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
        """
        Verifica que los errores al intentar agregar alimentos se registren correctamente en los logs.
        """
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
        """
        Comprueba que si no hay alimentos en la fábrica, el cajón permanezca vacío.
        """
        fabrica = FabricaDeAlimentos([])
        sensor = Sensor(fabrica)
        cajon = Cajon(5)
        cinta = CintaTransportadora(sensor, cajon)

        cinta.iniciar_transporte(max_intentos=10)

        self.assertEqual(len(cajon.alimentos), 0)

    def test_cinta_excepcion_al_agregar(self):
        """
        Simula un error controlado al agregar alimentos y verifica que el mensaje de error sea loggeado.
        """
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
        """
        Verifica que la cinta no agregue alimentos si se alcanza el número máximo de intentos.
        """
        fabrica = FabricaDeAlimentos()
        sensor = Sensor(fabrica)
        cajon = Cajon(1)  # Capacidad de 1 alimento
        cinta = CintaTransportadora(sensor, cajon)

        cinta.iniciar_transporte(max_intentos=1)  # Forzar el límite de intentos
        self.assertEqual(len(cajon.alimentos), 1)  # No se debe agregar ningún alimento

if __name__ == "__main__":
    unittest.main()
    print(logging.getLevelName(logger))

    