from modules.sensor import Sensor, FabricaDeAlimentos
from modules.cajon import Cajon

class CintaTransportadora:
    def __init__(self, sensor, cajon):
        self.sensor = sensor
        self.cajon = cajon

    def iniciar_transporte(self):
        while not self.detener_transporte():
            alimento = self.sensor.sensar()
            if alimento is not None:
                try:
                    self.cajon.agregar_alimento(alimento)
                except Exception as e:
                    print(f"Error al agregar alimento: {e}")

    def detener_transporte(self):
        return len(self.cajon) >= self.cajon.capacidad

if __name__ == "__main__":

    fabrica = FabricaDeAlimentos()
    sensor = Sensor(fabrica)
    cajon = Cajon(3)  # Capacidad de 3 alimentos
    cinta = CintaTransportadora(sensor, cajon)

    cinta.iniciar_transporte()

    print("Contenido del cajón después del transporte:")
    for alimento in cajon:
        print(alimento)