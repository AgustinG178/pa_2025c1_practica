import unittest
import heapq
from modules.monticulos import Estadisticas, MonticuloBinario, MonticuloMediana

# Asumimos que las clases Estadisticas, MonticuloMediana y MonticuloBinario ya están importadas

class TestEstadisticas(unittest.TestCase):
    """Test de la clase Estadisticas para operaciones estadísticas básicas."""

    def test_obtener_mediana_par(self):
        """Mediana de lista con cantidad par de elementos."""
        datos = [10, 2, 14, 4]
        stats = Estadisticas(datos)
        self.assertEqual(stats.obtener_mediana(), (4 + 10) / 2)

    def test_obtener_mediana_impar(self):
        """Mediana de lista con cantidad impar de elementos."""
        datos = [1, 3, 5]
        stats = Estadisticas(datos)
        self.assertEqual(stats.obtener_mediana(), 3)

    def test_obtener_maximo(self):
        """Máximo valor en la lista."""
        datos = [5, 9, 1]
        stats = Estadisticas(datos)
        self.assertEqual(stats.obtener_maximo(), 9)

    def test_obtener_minimo(self):
        """Mínimo valor en la lista."""
        datos = [5, 9, 1]
        stats = Estadisticas(datos)
        self.assertEqual(stats.obtener_minimo(), 1)

    def test_obtener_promedio(self):
        """Promedio de los valores en la lista."""
        datos = [2, 4, 6, 8]
        stats = Estadisticas(datos)
        self.assertEqual(stats.obtener_promedio(), 5)

    def test_empty_data(self):
        """Resultados con lista vacía deben ser None."""
        stats = Estadisticas([])
        self.assertIsNone(stats.obtener_mediana())
        self.assertIsNone(stats.obtener_maximo())
        self.assertIsNone(stats.obtener_minimo())
        self.assertIsNone(stats.obtener_promedio())

class TestMonticuloMediana(unittest.TestCase):
    """Test de MonticuloMediana para cálculo eficiente de la mediana."""

    def test_construccion_mediana(self):
        """Mediana correcta al construir el montículo con datos."""
        datos = [5, 15, 1, 3]
        monticulo = MonticuloMediana(datos)
        self.assertAlmostEqual(monticulo.obtener_mediana(), (3 + 5) / 2)

    def test_insertar_y_obtener_mediana(self):
        """Mediana correcta tras insertar un nuevo valor."""
        datos = [1, 2, 3]
        monticulo = MonticuloMediana(datos)
        self.assertEqual(monticulo.obtener_mediana(), 2)
        monticulo.insertar(4)
        self.assertEqual(monticulo.obtener_mediana(), 2.5)

    def test_mediana_lista_vacia(self):
        """Mediana de lista vacía debe ser None."""
        monticulo = MonticuloMediana([])
        self.assertIsNone(monticulo.obtener_mediana())

class TestMonticuloBinario(unittest.TestCase):
    """Test del MonticuloBinario para heap mínimo y máximo."""

    def test_heap_minimo(self):
        """Comportamiento básico del heap mínimo."""
        heap = MonticuloBinario(es_maximo=False)
        valores = [5, 3, 8]
        for v in valores:
            heap.insertar(v)
        self.assertEqual(heap.top(), 3)
        self.assertEqual(len(heap), 3)
        self.assertEqual(heap.extraer(), 3)
        self.assertEqual(heap.top(), 5)

    def test_heap_maximo(self):
        """Comportamiento básico del heap máximo."""
        heap = MonticuloBinario(es_maximo=True)
        valores = [5, 3, 8]
        for v in valores:
            heap.insertar(v)
        self.assertEqual(heap.top(), 8)
        self.assertEqual(len(heap), 3)
        self.assertEqual(heap.extraer(), 8)
        self.assertEqual(heap.top(), 5)

if __name__ == "__main__":
    unittest.main()
