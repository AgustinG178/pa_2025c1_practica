import unittest
from modules.monticulos import Estadisticas, MonticuloBinario, MonticuloMediana

class TestEstadisticas(unittest.TestCase):
    """Tests para la clase Estadisticas."""

    def test_obtener_mediana_par(self):
        # Arrange
        datos = [10, 2, 14, 4]
        stats = Estadisticas(datos)
        # Act
        result = stats.obtener_mediana()
        # Assert
        self.assertEqual(result, (4 + 10) / 2)

    def test_obtener_mediana_impar(self):
        # Arrange
        datos = [1, 3, 5]
        stats = Estadisticas(datos)
        # Act & Assert
        self.assertEqual(stats.obtener_mediana(), 3)

    def test_obtener_maximo(self):
        # Arrange
        datos = [5, 9, 1]
        stats = Estadisticas(datos)
        # Act & Assert
        self.assertEqual(stats.obtener_maximo(), 9)

    def test_obtener_minimo(self):
        # Arrange
        datos = [5, 9, 1]
        stats = Estadisticas(datos)
        # Act & Assert
        self.assertEqual(stats.obtener_minimo(), 1)

    def test_obtener_promedio(self):
        # Arrange
        datos = [2, 4, 6, 8]
        stats = Estadisticas(datos)
        # Act & Assert
        self.assertEqual(stats.obtener_promedio(), 5)

    def test_empty_data(self):
        # Arrange
        stats = Estadisticas([])
        # Act & Assert
        self.assertIsNone(stats.obtener_mediana())
        self.assertIsNone(stats.obtener_maximo())
        self.assertIsNone(stats.obtener_minimo())
        self.assertIsNone(stats.obtener_promedio())

class TestMonticuloMediana(unittest.TestCase):
    """Tests para la clase MonticuloMediana."""

    def test_construccion_mediana(self):
        # Arrange
        datos = [5, 15, 1, 3]
        monticulo = MonticuloMediana(datos)
        # Act & Assert
        self.assertAlmostEqual(monticulo.obtener_mediana(), (3 + 5) / 2)

    def test_insertar_y_obtener_mediana(self):
        # Arrange
        datos = [1, 2, 3]
        monticulo = MonticuloMediana(datos)
        # Act & Assert primera mediana
        self.assertEqual(monticulo.obtener_mediana(), 2)
        # Act insertar valor y obtener mediana
        monticulo.insertar(4)
        # Assert
        self.assertEqual(monticulo.obtener_mediana(), 2.5)

    def test_mediana_lista_vacia(self):
        # Arrange
        monticulo = MonticuloMediana([])
        # Act & Assert
        self.assertIsNone(monticulo.obtener_mediana())

    def test_insertar_valores(self):
        # Arrange
        monticulo = MonticuloMediana([10, 20, 30])
        # Act
        monticulo.insertar(25)
        # Assert
        self.assertEqual(monticulo.obtener_mediana(), 22.5)  # Ajusta el valor esperado

class TestMonticuloBinario(unittest.TestCase):
    """Tests para la clase MonticuloBinario."""

    def test_heap_minimo(self):
        # Arrange
        heap = MonticuloBinario(es_maximo=False)
        valores = [5, 3, 8]
        # Act
        for v in valores:
            heap.insertar(v)
        # Assert
        self.assertEqual(heap.top(), 3)
        self.assertEqual(len(heap), 3)
        self.assertEqual(heap.extraer(), 3)
        self.assertEqual(heap.top(), 5)

    def test_heap_maximo(self):
        # Arrange
        heap = MonticuloBinario(es_maximo=True)
        valores = [5, 3, 8]
        # Act
        for v in valores:
            heap.insertar(v)
        # Assert
        self.assertEqual(heap.top(), 8)
        self.assertEqual(len(heap), 3)
        self.assertEqual(heap.extraer(), 8)
        self.assertEqual(heap.top(), 5)

if __name__ == "__main__":  # pragma: no cover
    unittest.main()

