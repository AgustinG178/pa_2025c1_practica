from abc import ABC, abstractmethod, abstractproperty
from math import exp

class Alimento(ABC):
    """
    Clase abstracta que representa un alimento.
    """
    def __init__(self, nombre, tipo, peso):
        self._nombre = nombre
        self._peso = peso # en gramos
    
    @abstractmethod 
    def calcular_aw(self):
        pass #pragma: no cover
    
    @abstractproperty
    def peso(self):
        """
        Propiedad abstracta que devuelve el peso del alimento.
        """
        return self._peso
    
    @abstractproperty
    def aw(self):
        """
        Propiedad abstracta que calcula la actividad acuosa (aw) del alimento.
        """
        return self.calcular_aw() #pragma: no cover
    
    def __str__(self):
        return f"{self._nombre.capitalize()} - {self._peso} kg"

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

class Kiwi(Fruta):
    def __init__(self, peso):
        super().__init__("kiwi", "fruta", peso / 1000)

    def calcular_aw(self):
        return 0.96 * (1 - exp(-18 * self._peso)) / (1 + exp(-18 * self._peso))

    @property
    def aw(self):
        return round(self.calcular_aw(), 3)
    
    def __str__(self):
        return f"{self._nombre.capitalize()} - {self._peso} kg (aw: {self.aw})"
    
    @property
    def peso(self):
        return self._peso
  
class Manzana(Fruta):
    def __init__(self, peso):
        super().__init__("manzana", "fruta", peso / 1000)

    def calcular_aw(self):
        return 0.96 * (1 - exp(-18 * self._peso)) / (1 + exp(-18 * self._peso))

    @property
    def aw(self):
        return round(self.calcular_aw(), 3)
    
    @property
    def peso(self):
        return self._peso
    
    def __str__(self):
        return f"{self._nombre.capitalize()} - {self._peso} kg (aw: {self.aw})"


class Papa(Verdura):
    def __init__(self, peso):
        super().__init__("papa", "verdura", peso / 1000)

    def calcular_aw(self):
        return 0.96 * (1 - exp(-18 * self._peso)) / (1 + exp(-18 * self._peso))

    @property
    def aw(self):
        return round(self.calcular_aw(), 3)
    
    @property
    def peso(self):
        return self._peso
    
    def __str__(self):
        return f"{self._nombre.capitalize()} - {self._peso} kg (aw: {self.aw})"


class Zanahoria(Verdura):
    def __init__(self, peso):
        super().__init__("zanahoria", "verdura", peso / 1000)

    def calcular_aw(self):
        return 0.96 * (1 - exp(-18 * self._peso)) / (1 + exp(-18 * self._peso))

    @property
    def aw(self):
        return round(self.calcular_aw(), 3)
    
    @property
    def peso(self):
        return self._peso
    
    def __str__(self):
        return f"{self._nombre.capitalize()} - {self._peso} kg (aw: {self.aw})"

if __name__ == "__main__": #pragma: no cover
    kiwi = Kiwi(500)  # 500 gramos
    kiwi2 = Kiwi(300)
    kiwi3 = Kiwi(100)
    manzana = Manzana(300)  # 300 gramos
    papa = Papa(400)  # 400 gramos
    zanahoria = Zanahoria(250)  # 250 gramos

    print(kiwi)
    print(kiwi2)
    print(kiwi3)    
    print(manzana)
    print(papa)
    print(zanahoria)