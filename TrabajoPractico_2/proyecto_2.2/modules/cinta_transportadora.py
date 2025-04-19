"""
Consignas a seguir:
-  El peso total del cajón 
-  La  actividad  acuosa  promedio  de  cada alimento (aw_prom_*: promedio de las aw de cada 
   alimento, por ejemplo aw_prom_kiwi)  
-  La actividad acuosa promedio por tipo de alimento (aw_prom_frutas y aw_prom_verduras) 
-  La actividad acuosa promedio total del conjunto de alimentos (aw_total)

m < 600g

El programa debe avisar al operario mediante un mensaje de advertencia si alguno 
de los promedios calculados supera el valor de 0.90.

considerar al cajón como un contenedor iterable
"""

import random
from math import exp, atan

class Sensor:
    def detectar(self):
        # Simula la detección de un alimento
        alimentos = [
            {"alimento": "kiwi", "tipo": "fruta", "peso": random.randint(50, 599)},
            {"alimento": "manzana", "tipo": "fruta", "peso": random.randint(100, 599)},
            {"alimento": "papa", "tipo": "verdura", "peso": random.randint(200, 599)},
            {"alimento": "zanahoria", "tipo": "verdura", "peso": random.randint(100, 599)},
            {"alimento": "undefined", "tipo": None, "peso": 0}  
        ]
        return random.choice(alimentos)

class alimento:
    def __init__(self, nombre, tipo, peso):
        self.nombre = nombre  
        self.tipo = tipo      
        self.peso = peso      
        self.aw = self.calcular_aw(self.peso)

    def calcular_aw(self, masa):
        masa = self.peso / 1000  # Convertir a kg para las fórmulas
        # Fórmulas específicas para cada alimento
        if self.nombre == "kiwi":
            return (0.97 * ((15*masa)**2)/(1+(15*masa)**2))
        elif self.nombre == "manzana":
            return (0.96 * (1-exp(-18 * masa))/(1+exp(-18 * masa)))
        elif self.nombre == "papa":
            return (0.66 * atan(18 * masa))
        elif self.nombre == "zanahoria":
            return (0.96 * (1-exp(-10 * masa)))
        else:
            return 0  # Valor por defecto

class Cajon:
    def __init__(self, capacidad):
        self.capacidad = capacidad  # Número máximo de alimentos
        self.alimentos = []         # Lista de alimentos en el cajón

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

class CintaTransportadora:
    def __init__(self, sensor):
        self.sensor = sensor  # Sensor para detectar alimentos

    def detectar_alimento(self):
        # Simula la detección de un alimento
        deteccion = self.sensor.detectar()
        if deteccion["alimento"] == "undefined":
            return None  # Alimento no válido
        return alimento(deteccion["alimento"], deteccion["tipo"], deteccion["peso"])

class Controlador:
    def __init__(self, cinta, cajon, total_alimentos_deseados):
        self.cinta = cinta
        self.cajon = cajon
        self.total_alimentos_deseados = total_alimentos_deseados

        # Divide aleatoriamente la cantidad total entre frutas y verduras
        self.frutas_deseadas = random.randint(0, total_alimentos_deseados)
        self.verduras_deseadas = total_alimentos_deseados - self.frutas_deseadas

    def iniciar_transporte(self):
        frutas_actuales = 0
        verduras_actuales = 0

        while len(self.cajon.alimentos) < self.cajon.capacidad:
            alimento = self.cinta.detectar_alimento()
            if alimento:
                if alimento.tipo == "fruta" and frutas_actuales < self.frutas_deseadas:
                    self.cajon.agregar_alimento(alimento)
                    frutas_actuales += 1
                elif alimento.tipo == "verdura" and verduras_actuales < self.verduras_deseadas:
                    self.cajon.agregar_alimento(alimento)
                    verduras_actuales += 1

            # Si ya se alcanzaron las cantidades deseadas de frutas y verduras, salir del bucle
            if frutas_actuales >= self.frutas_deseadas and verduras_actuales >= self.verduras_deseadas:
                break

    def calcular_metricas(self):
        frutas = [alimento for alimento in self.cajon if alimento.tipo == "fruta"]
        verduras = [alimento for alimento in self.cajon if alimento.tipo == "verdura"]

        aw_prom_frutas = sum(alimento.aw for alimento in frutas) / len(frutas) if frutas else 0
        aw_prom_verduras = sum(alimento.aw for alimento in verduras) / len(verduras) if verduras else 0
        aw_total = self.cajon.aw_promedio()

        return {
            "peso_total": round((self.cajon.peso_total()) / 1000, 2),  # Convertir a kg
            "aw_prom_frutas": round(aw_prom_frutas, 2),
            "aw_prom_verduras": round(aw_prom_verduras, 2),
            "aw_total": round(aw_total, 2)
        }


