import numpy as np
import random
import matplotlib.pyplot as plt
import random
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria

"""
¿porque la fabrica esta en este archivo? porque sino se genera un bucle de importaciones
circular, ya que la fabrica necesita el sensor y el sensor necesita la fabrica.
"""

class DetectorAlimento:
    """clase que representa un conjunto de sensores de la cinta transportadora
    para detectar el tipo de alimento y su peso.
    """
    def __init__(self):
        self.alimentos = ["kiwi", "manzana", "papa", "zanahoria", "undefined"]
        self.peso_alimentos = np.round(np.linspace(0.05, 0.6, 12),2)
        self.prob_pesos = np.round(self.__softmax(self.peso_alimentos)[::-1], 2)

    def __softmax(self, x):
        """función softmax para crear vector de probabilidades 
        que sumen 1 en total
        """
        return (np.exp(x - np.max(x)) / np.exp(x - np.max(x)).sum())

    def detectar_alimento(self):
        """método que simula la detección del alimento y devuelve un diccionario
        con la información del tipo y el peso del alimento.
        """
        n_alimentos = len(self.alimentos)
        alimento_detectado = self.alimentos[random.randint(0, n_alimentos-1)]
        peso_detectado = random.choices(self.peso_alimentos, self.prob_pesos)[0]
        return {"alimento": alimento_detectado, "peso": peso_detectado}

class FabricaDeAlimentos:
    """
    Se encarga de instanciar los alimentos.
    """
    def __init__(self, p_alimento_detectado):
        self.posibles_alimentos = [Kiwi, Manzana, Papa, Zanahoria]
        self.p_alimento_detectado = DetectorAlimento()
        
    def crear_alimento_random(self):
        clase_alimento = self.posibles_alimentos(self.p_alimento_detectado)
        peso = random.randint(50, 599) # Peso aleatorio entre 50 y 599 gramos
        return clase_alimento(peso)
    
if __name__ == "__main__":
    fabrica = FabricaDeAlimentos()
    alimento = fabrica.crear_alimento_random()
    print(f"Alimento generado: {alimento}")
    
class Sensor:
    def __init__(self, fabrica):
        self.fabrica = fabrica

    def sensar(self):
        return self.fabrica.crear_alimento_random()
    
