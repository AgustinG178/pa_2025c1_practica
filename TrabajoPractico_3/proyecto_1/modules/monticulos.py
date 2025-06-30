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
        self.montos = []
        self.es_maximo = es_maximo

    def insertar(self, valor):
        """Inserta un valor y mantiene la propiedad del montículo."""
        if self.es_maximo:
            valor = -valor
        self.montos.append(valor)
        self._subir(len(self.montos) - 1)

    def extraer(self):
        """Extrae el valor raíz del montículo y reordena."""
        if not self.montos:
            return None
        raiz = self.montos[0]
        ultimo = self.montos.pop()
        if self.montos:
            self.montos[0] = ultimo
            self._bajar(0)
        return -raiz if self.es_maximo else raiz

    def top(self):
        """Devuelve el valor raíz del montículo sin extraerlo."""
        if not self.montos:
            return None
        return -self.montos[0] if self.es_maximo else self.montos[0]

    def _subir(self, i):
        """Mantiene la propiedad del montículo al subir un nodo."""
        while i > 0:
            padre = (i - 1) // 2
            if self.montos[i] < self.montos[padre]:
                self.montos[i], self.montos[padre] = self.montos[padre], self.montos[i]
                i = padre
            else:
                break

    def _bajar(self, i):
        """Mantiene la propiedad del montículo al bajar un nodo."""
        n = len(self.montos)
        while True:
            izq = 2 * i + 1
            der = 2 * i + 2
            menor = i

            if izq < n and self.montos[izq] < self.montos[menor]:
                menor = izq
            if der < n and self.montos[der] < self.montos[menor]:
                menor = der

            if menor == i:
                break
            self.montos[i], self.montos[menor] = self.montos[menor], self.montos[i]
            i = menor

    def __len__(self):
        return len(self.montos)
    
class MonticuloMediana():
    """Extiende Estadisticas para mantener la mediana usando montículos personalizados."""

    def __init__(self, datos):
        self.datos = datos
        self.monto_minimo = MonticuloBinario(es_maximo=False)  # mayores
        self.monto_maximo = MonticuloBinario(es_maximo=True)   # menores

        self._construir_monticulos()

    def _construir_monticulos(self):
        for num in self.datos:
            self.insertar(num)

    def insertar(self, valor):
        if len(self.monto_maximo) == 0 or valor <= self.monto_maximo.top():
            self.monto_maximo.insertar(valor)
        else:
            self.monto_minimo.insertar(valor)

        if len(self.monto_maximo) > len(self.monto_minimo) + 1:
            self.monto_minimo.insertar(self.monto_maximo.extraer())
        elif len(self.monto_minimo) > len(self.monto_maximo):
            self.monto_maximo.insertar(self.monto_minimo.extraer())

    def obtener_mediana(self):
        if not self.datos and len(self.monto_maximo) == 0:
            return None
        if len(self.monto_maximo) == len(self.monto_minimo):
            return (self.monto_maximo.top() + self.monto_minimo.top()) / 2
        else:
            return self.monto_maximo.top()

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

    print("Contenido del montículo máximo (menores):", [-x for x in monticulo_mediana.monto_maximo.montos])
    print("Contenido del montículo mínimo (mayores):", monticulo_mediana.monto_minimo.montos)

    monticulo_mediana.insertar(25)
    print("Mediana después de insertar 25:", monticulo_mediana.obtener_mediana())

    print("Nuevo contenido del montículo máximo (menores):", [-x for x in monticulo_mediana.monto_maximo.montos])
    print("Nuevo contenido del montículo mínimo (mayores):", monticulo_mediana.monto_minimo.montos)


