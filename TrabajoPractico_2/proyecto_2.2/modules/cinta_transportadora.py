from modules.sensor import Sensor, FabricaDeAlimentos
from modules.cajon import Cajon
import logging

"""
Este módulo utiliza `logging`, una biblioteca estándar de Python para registrar mensajes de log.
El módulo `logging` permite rastrear eventos en el código, como errores, advertencias o información general,
y es útil para depuración y monitoreo de aplicaciones.
"""

logger = logging.getLogger("modules.cinta_transportadora") # Crea un logger para este módulo

class CintaTransportadora:
    """
    Clase que representa una cinta transportadora que mueve alimentos detectados por un sensor hacia un cajón.
    """
    def __init__(self, sensor, cajon):
        """
        Inicializa la cinta transportadora con un sensor y un cajón.
        """
        self.__sensor = sensor
        self.__cajon = cajon

    @property
    def sensor(self):
        """
        Devuelve el sensor asociado a la cinta transportadora.
        """
        return self.__sensor
    
    @property
    def cajon(self):
        """
        Devuelve el cajón asociado a la cinta transportadora.
        """
        return self.__cajon

    def iniciar_transporte(self, max_intentos=1000):
        """
        Inicia el proceso de transporte de alimentos desde el sensor al cajón.
        """
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
        """
        Determina si se debe detener el transporte según la capacidad del cajón.
        """
        return len(self.cajon.alimentos) >= self.cajon.capacidad

if __name__ == "__main__": #pragma: no cover
    """
    Ejemplo de uso del módulo: crea una cinta transportadora, un sensor y un cajón, y transporta alimentos.
    """
    fabrica = FabricaDeAlimentos()
    sensor = Sensor(fabrica)
    cajon = Cajon(3)  # Capacidad de 3 alimentos
    cinta = CintaTransportadora(sensor, cajon)

    cinta.iniciar_transporte()

    print("Contenido del cajón después del transporte:")
    for alimento in cajon:
        print(alimento)