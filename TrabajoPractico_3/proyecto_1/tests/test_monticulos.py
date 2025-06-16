import unittest
from modules.monticulos import Estadisticas, MonticuloBinario, MonticuloMediana

# Asumimos que las clases Estadisticas, MonticuloMediana y MonticuloBinario ya están importadas

class TestEstadisticas(unittest.TestCase):
    """Tests para la clase Estadisticas."""

    def test_obtener_mediana_par(self):
        """Verifica la mediana para una lista par de elementos."""
        #arrange
        datos = [10, 2, 14, 4]
        stats = Estadisticas(datos)
        #act
        result = stats.obtener_mediana()
        #assert
        self.assertEqual(result, (4 + 10) / 2)

    def test_obtener_mediana_impar(self):
        """Verifica la mediana para una lista impar de elementos."""
        datos = [1, 3, 5]
        stats = Estadisticas(datos)
        self.assertEqual(stats.obtener_mediana(), 3)

    def test_obtener_maximo(self):
        """Verifica el valor máximo de la lista."""
        datos = [5, 9, 1]
        stats = Estadisticas(datos)
        self.assertEqual(stats.obtener_maximo(), 9)

    def test_obtener_minimo(self):
        """Verifica el valor mínimo de la lista."""
        datos = [5, 9, 1]
        stats = Estadisticas(datos)
        self.assertEqual(stats.obtener_minimo(), 1)

    def test_obtener_promedio(self):
        """Verifica el promedio de la lista."""
        datos = [2, 4, 6, 8]
        stats = Estadisticas(datos)
        self.assertEqual(stats.obtener_promedio(), 5)

    def test_empty_data(self):
        """Verifica que los métodos retornan None para listas vacías."""
        stats = Estadisticas([])
        self.assertIsNone(stats.obtener_mediana())
        self.assertIsNone(stats.obtener_maximo())
        self.assertIsNone(stats.obtener_minimo())
        self.assertIsNone(stats.obtener_promedio())

class TestMonticuloMediana(unittest.TestCase):
    """Tests para la clase MonticuloMediana."""

    def test_construccion_mediana(self):
        """Verifica la mediana al construir el montículo con datos."""
        datos = [5, 15, 1, 3]
        monticulo = MonticuloMediana(datos)
        self.assertAlmostEqual(monticulo.obtener_mediana(), (3 + 5) / 2)

    def test_insertar_y_obtener_mediana(self):
        """Verifica la mediana tras insertar un nuevo valor."""
        datos = [1, 2, 3]
        monticulo = MonticuloMediana(datos)
        self.assertEqual(monticulo.obtener_mediana(), 2)
        monticulo.insertar(4)
        self.assertEqual(monticulo.obtener_mediana(), 2.5)

    def test_mediana_lista_vacia(self):
        """Verifica que la mediana de una lista vacía es None."""
        monticulo = MonticuloMediana([])
        self.assertIsNone(monticulo.obtener_mediana())

    def test_insertar_valores(self):
        monticulo = MonticuloMediana([10, 20, 30])
        monticulo.insertar(25)
        self.assertEqual(monticulo.obtener_mediana(), 22.5)  # Ajusta el valor esperado
        
class TestMonticuloBinario(unittest.TestCase):
    """Tests para la clase MonticuloBinario."""

    def test_heap_minimo(self):
        """Verifica el comportamiento del heap mínimo."""
        heap = MonticuloBinario(es_maximo=False)
        valores = [5, 3, 8]
        for v in valores:
            heap.insertar(v)
        self.assertEqual(heap.top(), 3)
        self.assertEqual(len(heap), 3)
        self.assertEqual(heap.extraer(), 3)
        self.assertEqual(heap.top(), 5)

    def test_heap_maximo(self):
        """Verifica el comportamiento del heap máximo."""
        heap = MonticuloBinario(es_maximo=True)
        valores = [5, 3, 8]
        for v in valores:
            heap.insertar(v)
        self.assertEqual(heap.top(), 8)
        self.assertEqual(len(heap), 3)
        self.assertEqual(heap.extraer(), 8)
        self.assertEqual(heap.top(), 5)

if __name__ == "__main__": #pragma: no cover
    unittest.main()
