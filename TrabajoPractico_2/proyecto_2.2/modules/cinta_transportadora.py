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

    Args:
        nombre (str): Nombre del alimento.
        masa (float): Masa del alimento en kilogramos.

    Returns:
        float: Actividad acuosa del alimento. Devuelve 0 si el alimento no tiene fórmula definida.
    """
    if nombre in FORMULAS_AW:
        return FORMULAS_AW[nombre](masa)
    return 0  # Valor por defecto si el alimento no está en el diccionario

class alimento:
    """
    Clase que representa un alimento con atributos como nombre, tipo, peso y actividad acuosa.
    """

    def __init__(self, nombre, tipo, peso):
        """
        Inicializa un alimento.

        Args:
            nombre (str): Nombre del alimento.
            tipo (str): Tipo del alimento (fruta o verdura).
            peso (int): Peso del alimento en gramos.
        """
        self.nombre = nombre
        self.tipo = tipo
        self.peso = peso
        self.aw = calcular_aw(self.nombre, self.peso / 1000)  # Convertir peso a kg

    @classmethod
    def crear_fruta(cls, nombre, peso_minimo):
        """
        Crea una nueva instancia de un alimento de tipo fruta.

        Args:
            nombre (str): Nombre de la fruta.
            peso (int): Peso de la fruta en gramos.

        Returns:
            alimento: Nueva instancia de un alimento de tipo fruta.
        """
        return cls(nombre, "fruta", peso_minimo)

    @classmethod
    def crear_verdura(cls, nombre, peso_minimo):
        """
        Crea una nueva instancia de un alimento de tipo verdura.

        Args:
            nombre (str): Nombre de la verdura.
            peso (int): Peso de la verdura en gramos.

        Returns:
            alimento: Nueva instancia de un alimento de tipo verdura.
        """
        return cls(nombre, "verdura", peso_minimo)

class Cajon:
    def __init__(self, capacidad):
        """
        Inicializa un cajón con una capacidad máxima.
        """
        self.capacidad = capacidad
        self.alimentos = []  # Lista de alimentos en el cajón

    def agregar_alimento(self, alimento):
        """
        Agrega un alimento al cajón si hay espacio disponible.

        Args:
            alimento (alimento): Instancia de la clase alimento.

        Raises:
            Exception: Si el cajón está lleno.
        """
        if len(self.alimentos) < self.capacidad:
            self.alimentos.append(alimento)
        else:
            raise Exception("El cajón está lleno.")

    def peso_total(self):
        """
        Calcula el peso total de los alimentos en el cajón.

        Returns:
            int: Peso total en gramos.
        """
        return sum(alimento.peso for alimento in self.alimentos)

    def aw_promedio(self):
        """
        Calcula la actividad acuosa promedio de los alimentos en el cajón.

        Returns:
            float: Actividad acuosa promedio.
        """
        return sum(alimento.aw for alimento in self.alimentos) / len(self.alimentos)

    def __iter__(self):
        """
        Permite iterar sobre los alimentos en el cajón.

        Returns:
            iterator: Un iterador sobre la lista de alimentos en el cajón.
        """
        return iter(self.alimentos)

class CintaTransportadora:
    def __init__(self, alimentos):
        """
        Inicializa la cinta transportadora con alimentos.

        Args:
            sensor (Sensor): Instancia de la clase Sensor.
        """
        self.alimentos =[
            {"alimento": "kiwi", "tipo": "fruta", "peso": random.randint(50, 599)},
            {"alimento": "manzana", "tipo": "fruta", "peso": random.randint(100, 599)},
            {"alimento": "papa", "tipo": "verdura", "peso": random.randint(200, 599)},
            {"alimento": "zanahoria", "tipo": "verdura", "peso": random.randint(100, 599)},
            {"alimento": "undefined", "tipo": None, "peso": 0}
        ]

    def definir_alimento(self):
        """
        Detecta un alimento utilizando el sensor.

        Returns:
            alimento: Instancia de la clase alimento detectada por el sensor.
            None: Si no se detecta un alimento válido.
        """
        deteccion = random.choice(self.alimentos)
        if deteccion["alimento"] == "undefined":
            return None  # Alimento no válido
        return alimento(deteccion["alimento"], deteccion["tipo"], deteccion["peso"])

class Controlador:
    def __init__(self, cinta, cajon, total_alimentos_deseados):
        """
        Inicializa el controlador.

        Args:
            cinta (CintaTransportadora): Instancia de la clase CintaTransportadora.
            cajon (Cajon): Instancia de la clase Cajon.
            total_alimentos_deseados (int): Cantidad total de alimentos deseados.
        """
        self.cinta = cinta
        self.cajon = cajon
        self.total_alimentos_deseados = total_alimentos_deseados

        # Divide aleatoriamente la cantidad total entre frutas y verduras
        self.frutas_deseadas = random.randint(0, total_alimentos_deseados)
        self.verduras_deseadas = total_alimentos_deseados - self.frutas_deseadas

    def iniciar_transporte(self):
        """
        Inicia el transporte de alimentos desde la cinta transportadora al cajón.
        """
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
        """
        Calcula métricas del cajón, como el peso total y las actividades acuosas promedio.

        Returns:
            dict: Diccionario con las métricas calculadas.
        """
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
