import heapq
from modules.repositorio import RepositorioReclamosSQLAlchemy
from modules.reportes import GeneradorReportes
from modules.config import crear_engine

"""
Este módulo utiliza el módulo estándar 'heapq' de Python para implementar operaciones eficientes sobre montículos (heaps).
'heapq' permite gestionar listas como montículos binarios, proporcionando inserciones, extracciones y consultas de mínimos en tiempo logarítmico.
Esto es útil para calcular estadísticas como la mediana, el máximo y el mínimo de manera eficiente, especialmente en grandes volúmenes de datos.
"""

class Estadisticas:
    def __init__(self, datos):
        self.datos = datos

    def obtener_mediana(self):
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
        if not self.datos:
            return None
        return max(self.datos)

    def obtener_minimo(self):
        if not self.datos:
            return None
        return min(self.datos)

    def obtener_promedio(self):
        if not self.datos:
            return None
        return sum(self.datos) / len(self.datos)

class MonticuloMediana(Estadisticas):
    def __init__(self, datos):
        super().__init__(datos)
        self.min_heap = []  # heap de mayores
        self.max_heap = []  # heap de menores (como negativos)

        self._construir_monticulos()

    def _construir_monticulos(self):
        for num in self.datos:
            self.insertar(num)

    def insertar(self, valor):
        if not self.max_heap or valor <= -self.max_heap[0]:
            heapq.heappush(self.max_heap, -valor)
        else:
            heapq.heappush(self.min_heap, valor)

        # Balanceo
        if len(self.max_heap) > len(self.min_heap) + 1:
            heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        elif len(self.min_heap) > len(self.max_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))

    def obtener_mediana(self):
        if not self.datos:
            return None
        if len(self.max_heap) == len(self.min_heap):
            return (-self.max_heap[0] + self.min_heap[0]) / 2
        else:
            return -self.max_heap[0]

class MonticuloBinario:
    def __init__(self, es_maximo=False):
        self.es_maximo = es_maximo
        self.heap = []

    def insertar(self, valor):
        if self.es_maximo:
            heapq.heappush(self.heap, -valor)
        else:
            heapq.heappush(self.heap, valor)

    def extraer(self):
        if self.es_maximo:
            return -heapq.heappop(self.heap)
        else:
            return heapq.heappop(self.heap)

    def top(self):
        if self.es_maximo:
            return -self.heap[0]
        else:
            return self.heap[0]

    def __len__(self):
        return len(self.heap)


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

