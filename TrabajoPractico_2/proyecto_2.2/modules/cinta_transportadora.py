"""
Módulo para simular una cinta transportadora con sensores, alimentos y un cajón para almacenar los alimentos procesados.
Incluye funcionalidades para calcular métricas como el peso total y la actividad acuosa promedio.
"""

import random
from math import exp, atan
from abc import ABC, abstractmethod, abstractproperty

#Elimine el diccionario para que cumpla con el principio de responsabilidad única y no mezcle la lógica de negocio con la lógica de presentación.

class Alimento(ABC):
    """
    Clase abstracta que representa un alimento.
    """
    def __init__(self, nombre, tipo, peso):
        self.nombre = nombre
        self.tipo = tipo
        self.peso = peso # en gramos
    
    @abstractmethod
    def calcular_aw(self): #agregue un decorador de metodo abstracto para que cumpla con el principio de responsabilidad única y de abierto a cambios/cerrado a modificaciones
        pass
    
    @abstractproperty
    def aw(self):
        """
        Propiedad abstracta que calcula la actividad acuosa (aw) del alimento.
        """
        return self.calcular_aw()
    
    def __str__(self):
        return f"{self.nombre.capitalize()} ({self.tipo}) - {self.peso} g"

class Fruta(Alimento):
    """
    Clase hija que representa una fruta.
    """
    pass

class Verdura(Alimento):
    """
    Clase hija que representa una verdura.
    """
    pass

# Clases específicas para cada alimento
# agregue el decorador de metodo abstracto para que cumpla con el principio de responsabilidad única y de abierto a cambios/cerrado a modificaciones a cada clase hija de Alimento, eliminando asi el diccionario global
class Kiwi(Fruta):
    def __init__(self, peso):
        super().__init__("kiwi", "fruta", peso / 1000)

    def calcular_aw(self):
        return 0.96 * (1 - exp(-18 * self.peso)) / (1 + exp(-18 * self.peso))

    @property
    def aw(self):
        return round(self.calcular_aw(), 3)
    
    def __str__(self):
        return f"{self.nombre.capitalize()} ({self.tipo}) - {self.peso} g (aw: {self.aw})"


class Manzana(Fruta):
    def __init__(self, peso):
        super().__init__("manzana", "fruta", peso / 1000)

    def calcular_aw(self):
        return 0.96 * (1 - exp(-18 * self.peso)) / (1 + exp(-18 * self.peso))

    @property
    def aw(self):
        return round(self.calcular_aw(), 3)
    
    def __str__(self):
        return f"{self.nombre.capitalize()} ({self.tipo}) - {self.peso} g (aw: {self.aw})"


class Papa(Verdura):
    def __init__(self, peso):
        super().__init__("papa", "verdura", peso / 1000)

    def calcular_aw(self):
        return 0.96 * (1 - exp(-18 * self.peso)) / (1 + exp(-18 * self.peso))

    @property
    def aw(self):
        return round(self.calcular_aw(), 3)
    
    def __str__(self):
        return f"{self.nombre.capitalize()} ({self.tipo}) - {self.peso} g (aw: {self.aw})"


class Zanahoria(Verdura):
    def __init__(self, peso):
        super().__init__("zanahoria", "verdura", peso / 1000)

    def calcular_aw(self):
        return 0.96 * (1 - exp(-18 * self.peso)) / (1 + exp(-18 * self.peso))

    @property
    def aw(self):
        return round(self.calcular_aw(), 3)
    
    def __str__(self):
        return f"{self.nombre.capitalize()} ({self.tipo}) - {self.peso} g (aw: {self.aw})"
    
class FabricaDeAlimentos:
    """
    Se encarga de instanciar los alimentos.
    """
    def __init__(self):
        self.posibles_alimentos = [Kiwi, Manzana, Papa, Zanahoria]

    def crear_alimento_random(self):
        clase_alimento = random.choice(self.posibles_alimentos)
        peso = random.randint(50, 599) # Peso aleatorio entre 50 y 599 gramos
        return clase_alimento(peso)
    
class AnalizadorDeCajon:
    @staticmethod
    def calcular_metricas(cajon):
        frutas = [alimento for alimento in cajon if alimento.tipo == "fruta"]
        verduras = [alimento for alimento in cajon if alimento.tipo == "verdura"]

        aw_prom_frutas = sum(alimento.aw for alimento in frutas) / len(frutas) if frutas else 0
        aw_prom_verduras = sum(alimento.aw for alimento in verduras) / len(verduras) if verduras else 0
        aw_total = sum(alimento.aw for alimento in cajon) / len(cajon)

        return {
            "peso_total": round((sum(alimento.peso for alimento in cajon)) / 1000, 2),
            "aw_prom_frutas": round(aw_prom_frutas, 2),
            "aw_prom_verduras": round(aw_prom_verduras, 2),
            "aw_total": round(aw_total, 2)
        }    
    
class Sensor:
    def __init__(self, fabrica):
        self.fabrica = fabrica

    def detectar_alimento(self):
        return self.fabrica.crear_alimento_random()

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

    def __iter__(self):
        return iter(self.alimentos)
    
    def __len__(self):
        return len(self.alimentos)

class CintaTransportadora:
    def __init__(self, sensor, cajon):
        self.sensor = sensor
        self.cajon = cajon

    def iniciar_transporte(self):
        max_iteraciones = 1000  # Límite máximo de iteraciones para evitar bucles infinitos
        iteraciones = 0
        while not self.detener_transporte():
            if iteraciones >= max_iteraciones:
                print("Se alcanzó el límite máximo de iteraciones. Deteniendo transporte.")
                break
            alimento = self.sensor.detectar_alimento()
            if alimento is not None:
                try:
                    self.cajon.agregar_alimento(alimento)
                except Exception as e:
                    print(f"Error al agregar alimento: {e}")
            iteraciones += 1

    def detener_transporte(self):
        return len(self.cajon.alimentos) >= self.cajon.capacidad

class GeneradorDeInforme:
    @staticmethod
    def mostrar_metricas(metricas):
        print("Métricas calculadas:")
        print(f"Peso total del cajón: {metricas['peso_total']} kg")
        print(f"AW promedio de frutas: {metricas['aw_prom_frutas']}")
        print(f"AW promedio de verduras: {metricas['aw_prom_verduras']}")
        print(f"AW total del cajón: {metricas['aw_total']}")

if __name__ == "__main__":
    fabrica = FabricaDeAlimentos()
    sensor = Sensor(fabrica)

    while True:
        try:
            capacidad_cajon = int(input("Ingrese la capacidad del cajón (cantidad de alimentos): "))
            if capacidad_cajon > 0:
                break
            else:
                print("Por favor, ingrese un número entero positivo.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.")
    cajon = Cajon(capacidad=capacidad_cajon)

    cinta = CintaTransportadora(sensor, cajon)
    cinta.iniciar_transporte()

    metricas = AnalizadorDeCajon.calcular_metricas(cajon)

    GeneradorDeInforme.mostrar_metricas(metricas)
    print("Cinta transportadora detenida.")

    print("Contenido del cajón:")
    for alimento in cajon:
        print(f"{alimento}")


