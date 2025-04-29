from modules.sensor import Sensor, FabricaDeAlimentos
from modules.cajon import Cajon
import logging

"""
Este módulo utiliza `logging`, una biblioteca estándar de Python para registrar mensajes de log.
El módulo `logging` permite rastrear eventos en el código, como errores, advertencias o información general,
y es útil para depuración y monitoreo de aplicaciones.
"""

logger = logging.getLogger(__name__)


class CintaTransportadora:
    def __init__(self, sensor, cajon):
        self.sensor = sensor
        self.cajon = cajon

    def iniciar_transporte(self, max_intentos=1000):
        intentos = 0
        while not self.detener_transporte() and intentos < max_intentos:
            alimento = self.sensor.sensar()
            if alimento is not None:
                try:
                    self.cajon.agregar_alimento(alimento)
                except Exception as e:
                    logger.exception(f"Error al agregar alimento: {e}")
            intentos += 1

    def detener_transporte(self):
        return len(self.cajon.alimentos) >= self.cajon.capacidad

if __name__ == "__main__": #pragma: no cover

    fabrica = FabricaDeAlimentos()
    sensor = Sensor(fabrica)
    cajon = Cajon(3)  # Capacidad de 3 alimentos
    cinta = CintaTransportadora(sensor, cajon)

    cinta.iniciar_transporte()

    print("Contenido del cajón después del transporte:")
    for alimento in cajon:
        print(alimento)