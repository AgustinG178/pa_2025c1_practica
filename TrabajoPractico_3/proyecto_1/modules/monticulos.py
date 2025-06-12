from modules.repositorio import RepositorioReclamosSQLAlchemy
from modules.reportes import GeneradorReportes
from modules.config import crear_engine

"""
Este módulo utiliza el módulo estándar 'heapq' de Python para implementar operaciones eficientes sobre montículos (heaps).
'heapq' permite gestionar listas como montículos binarios, proporcionando inserciones, extracciones y consultas de mínimos en tiempo logarítmico.
Esto es útil para calcular estadísticas como la mediana, el máximo y el mínimo de manera eficiente, especialmente en grandes volúmenes de datos.
"""

class Estadisticas:
    """Clase base para calcular estadísticas básicas sobre una lista de datos."""

    def __init__(self, datos):
        """Inicializa la clase con una lista de datos."""
        self.datos = datos

    def obtener_mediana(self):
        """Calcula y devuelve la mediana de los datos."""
        if not self.datos:
            return None
        datos_ordenados = sorted(self.datos)
        n = len(datos_ordenados)
        medio = n // 2
        if n % 2 == 0:
            return (datos_ordenados[medio - 1] + datos_ordenados[medio]) / 2
        else:
            return datos_ordenados[medio]

    def obtener_maximo(self):
        """Devuelve el valor máximo de los datos."""
        if not self.datos:
            return None
        return max(self.datos)

    def obtener_minimo(self):
        """Devuelve el valor mínimo de los datos."""
        if not self.datos:
            return None
        return min(self.datos)

    def obtener_promedio(self):
        """Calcula y devuelve el promedio de los datos."""
        if not self.datos:
            return None
        return sum(self.datos) / len(self.datos)

class MonticuloBinario:
    """Implementa un montículo binario mínimo o máximo sin usar 'heapq'."""

    def __init__(self, es_maximo=False):
        self.heap = []
        self.es_maximo = es_maximo

    def insertar(self, valor):
        """Inserta un valor y mantiene la propiedad del montículo."""
        if self.es_maximo:
            valor = -valor
        self.heap.append(valor)
        self._subir(len(self.heap) - 1)

    def extraer(self):
        """Extrae el valor raíz del montículo y reordena."""
        if not self.heap:
            return None
        raiz = self.heap[0]
        ultimo = self.heap.pop()
        if self.heap:
            self.heap[0] = ultimo
            self._bajar(0)
        return -raiz if self.es_maximo else raiz

    def top(self):
        """Devuelve el valor raíz del montículo sin extraerlo."""
        if not self.heap:
            return None
        return -self.heap[0] if self.es_maximo else self.heap[0]

    def _subir(self, i):
        """Mantiene la propiedad del montículo al subir un nodo."""
        while i > 0:
            padre = (i - 1) // 2
            if self.heap[i] < self.heap[padre]:
                self.heap[i], self.heap[padre] = self.heap[padre], self.heap[i]
                i = padre
            else:
                break

    def _bajar(self, i):
        """Mantiene la propiedad del montículo al bajar un nodo."""
        n = len(self.heap)
        while True:
            izq = 2 * i + 1
            der = 2 * i + 2
            menor = i

            if izq < n and self.heap[izq] < self.heap[menor]:
                menor = izq
            if der < n and self.heap[der] < self.heap[menor]:
                menor = der

            if menor == i:
                break
            self.heap[i], self.heap[menor] = self.heap[menor], self.heap[i]
            i = menor

    def __len__(self):
        return len(self.heap)
    
class MonticuloMediana():
    """Extiende Estadisticas para mantener la mediana usando montículos personalizados."""

    def __init__(self, datos):
        super().__init__(datos)
        self.min_heap = MonticuloBinario(es_maximo=False)  # mayores
        self.max_heap = MonticuloBinario(es_maximo=True)   # menores

        self._construir_monticulos()

    def _construir_monticulos(self):
        for num in self.datos:
            self.insertar(num)

    def insertar(self, valor):
        if len(self.max_heap) == 0 or valor <= self.max_heap.top():
            self.max_heap.insertar(valor)
        else:
            self.min_heap.insertar(valor)

        # Balancear
        if len(self.max_heap) > len(self.min_heap) + 1:
            self.min_heap.insertar(self.max_heap.extraer())
        elif len(self.min_heap) > len(self.max_heap):
            self.max_heap.insertar(self.min_heap.extraer())

    def obtener_mediana(self):
        if not self.datos and len(self.max_heap) == 0:
            return None
        if len(self.max_heap) == len(self.min_heap):
            return (self.max_heap.top() + self.min_heap.top()) / 2
        else:
            return self.max_heap.top()

if __name__ == "__main__":
    enigne, Session = crear_engine()
    session = Session()
    repo_reclamos = RepositorioReclamosSQLAlchemy(session)
    generador = GeneradorReportes(repo_reclamos)

    datos_adherentes = generador.obtener_cantidades_adherentes(dias=365)

    print("Datos de adherentes:", datos_adherentes)

    monticulo_mediana = MonticuloMediana(datos_adherentes)
    mediana = monticulo_mediana.obtener_mediana()
    print("Mediana calculada con montículos:", mediana)

    # Probamos insertar un nuevo dato
    monticulo_mediana.insertar(25)
    print("Mediana después de insertar 25:", monticulo_mediana.obtener_mediana())

