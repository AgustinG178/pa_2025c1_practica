from abc import ABC, abstractmethod, abstractproperty
from math import exp

class Alimento(ABC):
    """
    Clase abstracta que representa un alimento.
    """
    def __init__(self, nombre, tipo, peso):
        self.nombre = nombre
        self.tipo = tipo
        self.peso = peso # en gramos
    
    @abstractmethod
    def calcular_aw(self):
        pass
    
    @abstractproperty
    def aw(self):
        """
        Propiedad abstracta que calcula la actividad acuosa (aw) del alimento.
        """
        return self.calcular_aw()
    
    def __str__(self):
        return f"{self.nombre.capitalize()} ({self.tipo}) - {self.peso} kg"

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
        return 0.96 * (1 - exp(-18 * self.peso)) / (1 + exp(-18 * self.peso))

    @property
    def aw(self):
        return round(self.calcular_aw(), 3)
    
    def __str__(self):
        return f"{self.nombre.capitalize()} ({self.tipo}) - {self.peso} kg (aw: {self.aw})"


class Manzana(Fruta):
    def __init__(self, peso):
        super().__init__("manzana", "fruta", peso / 1000)

    def calcular_aw(self):
        return 0.96 * (1 - exp(-18 * self.peso)) / (1 + exp(-18 * self.peso))

    @property
    def aw(self):
        return round(self.calcular_aw(), 3)
    
    def __str__(self):
        return f"{self.nombre.capitalize()} ({self.tipo}) - {self.peso} kg (aw: {self.aw})"


class Papa(Verdura):
    def __init__(self, peso):
        super().__init__("papa", "verdura", peso / 1000)

    def calcular_aw(self):
        return 0.96 * (1 - exp(-18 * self.peso)) / (1 + exp(-18 * self.peso))

    @property
    def aw(self):
        return round(self.calcular_aw(), 3)
    
    def __str__(self):
        return f"{self.nombre.capitalize()} ({self.tipo}) - {self.peso} kg (aw: {self.aw})"


class Zanahoria(Verdura):
    def __init__(self, peso):
        super().__init__("zanahoria", "verdura", peso / 1000)

    def calcular_aw(self):
        return 0.96 * (1 - exp(-18 * self.peso)) / (1 + exp(-18 * self.peso))

    @property
    def aw(self):
        return round(self.calcular_aw(), 3)
    
    def __str__(self):
        return f"{self.nombre.capitalize()} ({self.tipo}) - {self.peso} kg (aw: {self.aw})"

if __name__ == "__main__":
    kiwi = Kiwi(500)  # 500 gramos
    manzana = Manzana(300)  # 300 gramos
    papa = Papa(400)  # 400 gramos
    zanahoria = Zanahoria(250)  # 250 gramos

    print(kiwi)
    print(manzana)
    print(papa)
    print(zanahoria)