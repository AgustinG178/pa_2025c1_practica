import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cajon import Cajon, AnalizadorDeCajon, GeneradorDeInforme
from modules.cinta_transportadora import CintaTransportadora
from modules.sensor import Sensor, DetectorAlimento, FabricaDeAlimentos
import coverage
import io
from contextlib import redirect_stdout

"""
El módulo `io` proporciona las herramientas necesarias para manejar flujos de entrada y salida (I/O) en Python.

En particular, permite trabajar con objetos que simulan archivos en memoria, como `io.StringIO` o `io.BytesIO`, 
los cuales son útiles para capturar y manipular datos de entrada/salida sin necesidad de acceder al sistema de archivos.

Este módulo es especialmente útil en pruebas unitarias cuando se desea capturar la salida de `print()` o simular
archivos para testear funciones que dependen de lectura/escritura.
"""

class TestCajon(unittest.TestCase):
    """
    testea que la clase cajon agregue alimentos correctamente
    """
    def test_agregar_alimento(self):
        cajon = Cajon(2)  # Capacidad de 2 alimentos
        kiwi = Kiwi(500)
        manzana = Manzana(300)
        cajon.agregar_alimento(kiwi)
        cajon.agregar_alimento(manzana)
        self.assertEqual(len(cajon), 2)

    def test_cajon_lleno(self):
        """
        Verifica que no se pueda agregar un alimento si el cajón ya está lleno."""
        cajon = Cajon(1)  # Capacidad de 1 alimento
        kiwi = Kiwi(500)
        cajon.agregar_alimento(kiwi)
        with self.assertRaises(Exception) as context:
            cajon.agregar_alimento(Manzana(300))
        self.assertEqual(str(context.exception), "El cajón está lleno")

    def test_peso_total(self):
        """
        Verifica que el peso total del cajón sea correcto.
        """
        cajon = Cajon(2)
        kiwi = Kiwi(500)
        manzana = Manzana(300)
        cajon.agregar_alimento(kiwi)
        cajon.agregar_alimento(manzana)
        resultado = AnalizadorDeCajon.calcular_metricas(cajon)
        self.assertAlmostEqual(resultado["peso_total"], 0.8)
        
    def test_cajon_iter(self):
        """
        Verifica que el cajón sea iterable y devuelva los alimentos en el orden correcto.
        """
        cajon = Cajon(2)
        cajon.agregar_alimento(Kiwi(500))
        cajon.agregar_alimento(Manzana(300))
        alimentos = list(cajon)
        self.assertEqual(len(alimentos), 2)
        self.assertIsInstance(alimentos[0], Kiwi)
        
    def test_cajon_len(self):
        """
        verifica que la longitud del cajón sea correcta.
        """
        cajon = Cajon(2)
        cajon.agregar_alimento(Kiwi(500))
        self.assertEqual(len(cajon), 1)   

class TestGeneradorDeInforme(unittest.TestCase):
    def test_generar_advertencias(self):
        """
        Verifica que se generen advertencias adecuadas según las métricas.
        """
        metricas = {
            "peso_total": 1.2,
            "aw_prom_frutas": 0.95,
            "aw_prom_verduras": 0.98,
            "aw_total": 0.92
        }
        advertencias = GeneradorDeInforme.generar_advertencias(metricas)
        self.assertIn("Advertencia: La actividad acuosa promedio de las frutas supera 0.90.", advertencias)
        self.assertIn("Advertencia: La actividad acuosa total supera 0.90.", advertencias)
        self.assertIn("Advertencia: La actividad acuosa promedio de las verduras supera 0.90.", advertencias)  
        
    def test_mostrar_metricas(self):
        """
        Verifica que las métricas se muestren correctamente en la salida estándar.
        """
        metricas = {
            "peso_total": 1.2,
            "aw_prom_frutas": 0.95,
            "aw_prom_verduras": 0.85,
            "aw_total": 0.92
        }

        buffer = io.StringIO() #Crea un objeto de texto en memoria que actúa como un archivo. buffer al ser una variable, vive en la RAM por lo cual puede ser facilmente eliminado al terminar la ejecucion del programa.
        with redirect_stdout(buffer):  # captura print() para poder analizarlo, Es un context manager del módulo contextlib que redirige temporalmente toda la salida estándar (sys.stdout) hacia otro destino.
            GeneradorDeInforme.mostrar_metricas(metricas)
        salida = buffer.getvalue() #Extrae el contenido completo que se escribió en el StringIO.

        # Comprobaciones de valores
        self.assertEqual(metricas["peso_total"], 1.2)
        self.assertEqual(metricas["aw_prom_frutas"], 0.95)
        self.assertEqual(metricas["aw_prom_verduras"], 0.85)
        self.assertEqual(metricas["aw_total"], 0.92)

        # Comprobaciones de impresión
        self.assertIn("Peso total del cajón: 1.2 kg", salida)
        self.assertIn("AW promedio de frutas: 0.95", salida)
        self.assertIn("AW promedio de verduras: 0.85", salida)
        self.assertIn("AW total del cajón: 0.92", salida)
        
if __name__ == "__main__":
    unittest.main()