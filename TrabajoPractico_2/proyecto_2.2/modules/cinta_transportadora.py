"""
Módulo para simular una cinta transportadora con sensores, alimentos y un cajón para almacenar los alimentos procesados.
Incluye funcionalidades para calcular métricas como el peso total y la actividad acuosa promedio.
"""

import random
from math import exp, atan

# Diccionario de fórmulas para calcular aw
FORMULAS_AW = {
    "kiwi": lambda masa: (0.97 * ((15 * masa) ** 2) / (1 + (15 * masa) ** 2)),
    "manzana": lambda masa: (0.96 * (1 - exp(-18 * masa)) / (1 + exp(-18 * masa))),
    "papa": lambda masa: (0.66 * atan(18 * masa)),
    "zanahoria": lambda masa: (0.96 * (1 - exp(-10 * masa))),
}

def calcular_aw(nombre, masa):
    """
    Calcula la actividad acuosa (aw) de un alimento dado su nombre y masa.
    """
    if nombre in FORMULAS_AW:
        return FORMULAS_AW[nombre](masa)
    return 0  # Valor por defecto si el alimento no está en el diccionario

class Alimento:
    """
    Clase base que representa un alimento.
    """
    def __init__(self, nombre, tipo, peso):
        self.nombre = nombre
        self.tipo = tipo
        self.peso = peso
        self.aw = calcular_aw(self.nombre, self.peso / 1000)  # Convertir peso a kg

class Fruta(Alimento):
    """
    Subclase que representa una fruta.
    """
    pass

class Verdura(Alimento):
    """
    Subclase que representa una verdura.
    """
    pass

# Clases específicas para cada alimento
class Kiwi(Fruta):
    def __init__(self, peso):
        super().__init__("kiwi", "fruta", peso)

class Manzana(Fruta):
    def __init__(self, peso):
        super().__init__("manzana", "fruta", peso)

class Papa(Verdura):
    def __init__(self, peso):
        super().__init__("papa", "verdura", peso)

class Zanahoria(Verdura):
    def __init__(self, peso):
        super().__init__("zanahoria", "verdura", peso)

class Sensor:
    """
    Clase que representa un sensor para detectar alimentos.
    """
    def __init__(self):
        self.alimentos = [
            Kiwi(random.randint(50, 599)),
            Manzana(random.randint(100, 599)),
            Papa(random.randint(200, 599)),
            Zanahoria(random.randint(100, 599)),
            None  # Representa un alimento no válido
        ]

    def detectar_alimento(self):
        """
        Simula la detección de un alimento.

        Returns:
            Alimento o None: El alimento detectado o None si no se detecta nada.
        """
        return random.choice(self.alimentos)

class Cajon:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.alimentos = []

    def agregar_alimento(self, alimento):
        if len(self.alimentos) < self.capacidad:
            self.alimentos.append(alimento)
        else:
            raise Exception("El cajón está lleno.")

    def peso_total(self):
        return sum(alimento.peso for alimento in self.alimentos)

    def aw_promedio(self):
        return sum(alimento.aw for alimento in self.alimentos) / len(self.alimentos)

    def calcular_metricas(self):
        frutas = [alimento for alimento in self.alimentos if alimento.tipo == "fruta"]
        verduras = [alimento for alimento in self.alimentos if alimento.tipo == "verdura"]

        aw_prom_frutas = sum(alimento.aw for alimento in frutas) / len(frutas) if frutas else 0
        aw_prom_verduras = sum(alimento.aw for alimento in verduras) / len(verduras) if verduras else 0
        aw_total = self.aw_promedio()

        return {
            "peso_total": round((self.peso_total()) / 1000, 2),
            "aw_prom_frutas": round(aw_prom_frutas, 2),
            "aw_prom_verduras": round(aw_prom_verduras, 2),
            "aw_total": round(aw_total, 2)
        }

    def __iter__(self):
        return iter(self.alimentos)

class CintaTransportadora:
    def __init__(self, sensor, cajon):
        self.sensor = sensor
        self.cajon = cajon

    def iniciar_transporte(self):
        while len(self.cajon.alimentos) < self.cajon.capacidad:
            alimento = self.sensor.detectar_alimento()
            if alimento:
                #crear objetco de la clase Alimento aca
                self.cajon.agregar_alimento(alimento)

if __name__ == "__main__":

    sensor = Sensor()

    capacidad_cajon = int(input("Ingrese la capacidad del cajón (cantidad de alimentos): "))

    cajon = Cajon(capacidad=capacidad_cajon)

    cinta = CintaTransportadora(sensor, cajon)

    cinta.iniciar_transporte()

    metricas = cajon.calcular_metricas()
    print("Métricas calculadas:")
    print(f"Peso total del cajón: {metricas['peso_total']} kg")
    print(f"AW promedio de frutas: {metricas['aw_prom_frutas']}")
    print(f"AW promedio de verduras: {metricas['aw_prom_verduras']}")
    print(f"AW total del cajón: {metricas['aw_total']}")
    print("")
   
    for alimento in cajon: 
        print(f"{alimento}: {alimento.peso} g") 
 

