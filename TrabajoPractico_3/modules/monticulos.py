import heapq

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

    def separar_en_monticulo(self):
        # Separa los datos en dos montículos para calcular la mediana
        min_heap = []
        max_heap = []
        for num in self.datos:
            if not max_heap or num <= -max_heap[0]:
                heapq.heappush(max_heap, -num)
            else:
                heapq.heappush(min_heap, num)
            # Balancear los montículos
            if len(max_heap) > len(min_heap) + 1:
                heapq.heappush(min_heap, -heapq.heappop(max_heap))
            elif len(min_heap) > len(max_heap):
                heapq.heappush(max_heap, -heapq.heappop(min_heap))
        return [-x for x in max_heap], min_heap
    

class MonticuloMaxima:
    def calcular_maxima(self, datos):
        if not datos:
            return None
        return -heapq.nlargest(1, [-x for x in datos])[0]

class MonticuloMinima:
    def calcular_minima(self, datos):
        if not datos:
            return None
        return heapq.nsmallest(1, datos)[0]