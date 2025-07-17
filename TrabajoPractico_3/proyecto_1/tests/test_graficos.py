import unittest
from unittest.mock import patch, MagicMock
from modules.graficos import (
    GraficadoraTorta,
    GraficadoraHistograma,
    GraficadoraNubePalabras,
    Graficadora,
)
import os

import matplotlib
matplotlib.use('Agg')

class TestGraficadoraTorta(unittest.TestCase):
    @patch("modules.graficos.plt")
    @patch("modules.graficos.os.makedirs")
    def test_graficar_torta(self, mock_makedirs, mock_plt):
        """Verifica que se puede generar un gráfico de torta."""
        graficadora = GraficadoraTorta()
        datos = {"pendiente": 5, "resuelto": 3}
        ruta_esperada = os.path.join("static", "graficos", "test", "torta_test.png")
        ruta_carpeta_esperada = os.path.join("static", "graficos", "test")


        ruta = graficadora.graficar(datos, "torta_test.png", "test")

        mock_makedirs.assert_called_once_with(ruta_carpeta_esperada, exist_ok=True)
        mock_plt.savefig.assert_called_once_with(ruta_esperada)
        self.assertEqual(ruta, "graficos/test/torta_test.png")


class TestGraficadoraHistograma(unittest.TestCase):
    @patch("modules.graficos.plt")
    @patch("modules.graficos.os.makedirs")
    def test_graficar_histograma(self, mock_makedirs, mock_plt):
        """Verifica que se puede generar un histograma."""
        graficadora = GraficadoraHistograma()
        datos = [1, 2, 2, 3, 3, 3, 4, 5]
        ruta_esperada = os.path.join("static", "graficos", "test", "histograma_test.png")
        ruta_carpeta_esperada = os.path.join("static", "graficos", "test")


        ruta = graficadora.graficar(
            datos,
            titulo="Histograma Test",
            xlabel="Valores",
            ylabel="Frecuencia",
            nombre_archivo="histograma_test.png",
            subcarpeta="test",
        )

        mock_makedirs.assert_called_once_with(ruta_carpeta_esperada, exist_ok=True)
        mock_plt.savefig.assert_called_once_with(ruta_esperada)
        self.assertEqual(ruta, "graficos/test/histograma_test.png")

    @patch("modules.graficos.plt")
    def test_graficar_histograma_sin_datos(self, mock_plt):
        """Verifica que no se genera un histograma si no hay datos."""
        graficadora = GraficadoraHistograma()
        ruta = graficadora.graficar(
            datos=[],
            titulo="Histograma Vacío",
            xlabel="Valores",
            ylabel="Frecuencia",
            nombre_archivo="histograma_vacio.png",
            subcarpeta="test",
        )
        self.assertIsNone(ruta)
        mock_plt.savefig.assert_not_called()


class TestGraficadoraNubePalabras(unittest.TestCase):
    @patch("modules.graficos.WordCloud.to_file")
    @patch("modules.graficos.os.makedirs")
    def test_generar_nube_palabras(self, mock_makedirs, mock_to_file):
        """Verifica que se puede generar una nube de palabras."""
        graficadora = GraficadoraNubePalabras()
        reclamos = [
            MagicMock(contenido="El proyector no funciona"),
            MagicMock(contenido="El aire acondicionado está roto"),
        ]
        ruta_esperada = os.path.join("static", "graficos", "test", "nube_test.png")
        ruta_carpeta_esperada = os.path.join("static", "graficos", "test")


        ruta = graficadora.generar_nube_palabras(
            reclamos, nombre_archivo="nube_test.png", subcarpeta="test"
        )

        mock_makedirs.assert_called_once_with(ruta_carpeta_esperada, exist_ok=True)
        mock_to_file.assert_called_once_with(ruta_esperada)
        self.assertEqual(ruta, "graficos/test/nube_test.png")

    def test_generar_nube_palabras_sin_contenido(self):
        """Verifica que no se genera una nube de palabras si no hay contenido."""
        graficadora = GraficadoraNubePalabras()
        reclamos = [MagicMock(contenido=""), MagicMock(contenido=None)]
        ruta = graficadora.generar_nube_palabras(reclamos)
        self.assertIsNone(ruta)


class TestGraficadora(unittest.TestCase):
    @patch("modules.graficos.GraficadoraTorta.graficar")
    @patch("modules.graficos.GraficadoraHistograma.graficar")
    @patch("modules.graficos.GraficadoraNubePalabras.generar_nube_palabras")
    def test_graficar_todo(self, mock_nube, mock_histograma, mock_torta):
        """Verifica que se generan todos los gráficos correctamente."""
        generador_mock = MagicMock()
        graficadora = Graficadora(
            generador_mock,
            GraficadoraTorta(),
            GraficadoraHistograma(),
            GraficadoraNubePalabras(),
        )

        reclamos = [
            MagicMock(
                contenido="El proyector no funciona",
                clasificacion="soporte informático",
                cantidad_adherentes=3,
            ),
            MagicMock(
                contenido="El aire acondicionado está roto",
                clasificacion="maestranza",
                cantidad_adherentes=5,
            ),
        ]

        mock_torta.return_value = "ruta_torta.png"
        mock_histograma.return_value = "ruta_histograma.png"
        mock_nube.return_value = "ruta_nube.png"

        rutas = graficadora.graficar_todo(reclamos, clasificacion="soporte informático")

        self.assertEqual(rutas["torta"], "ruta_torta.png")
        self.assertEqual(rutas["histograma"], "ruta_histograma.png")
        self.assertEqual(rutas["nube_palabras"], "ruta_nube.png")

    @patch("modules.graficos.GraficadoraTorta.graficar")
    def test_graficar_torta_por_rol(self, mock_torta):
        """Verifica que se genera un gráfico de torta por rol."""
        generador_mock = MagicMock()
        graficadora = Graficadora(
            generador_mock,
            GraficadoraTorta(),
            GraficadoraHistograma(),
            GraficadoraNubePalabras(),
        )

        mock_torta.return_value = "ruta_torta_rol.png"
        ruta = graficadora.graficar_torta_por_rol("2", "torta_rol.png", "test")
        self.assertEqual(ruta, "ruta_torta_rol.png")

    @patch("modules.graficos.GraficadoraHistograma.graficar")
    def test_graficar_histograma_por_rol(self, mock_histograma):
        """Verifica que se genera un histograma por rol."""
        generador_mock = MagicMock()
        graficadora = Graficadora(
            generador_mock,
            GraficadoraTorta(),
            GraficadoraHistograma(),
            GraficadoraNubePalabras(),
        )

        graficadora.graficar_histograma_por_rol("2", "histograma_rol.png", "test")
        mock_histograma.assert_called_once()

import pytest
from modules.graficos import GraficadoraTorta
from unittest.mock import patch

@patch("matplotlib.pyplot.savefig")
@patch("os.makedirs")
@patch("matplotlib.pyplot.close")
def test_graficadora_torta(mock_close, mock_makedirs, mock_savefig):
    graficadora = GraficadoraTorta()
    datos = {"Abierto": 5, "Cerrado": 10}
    resultado = graficadora.graficar(datos, "test_torta.png", "test_subcarpeta")
    
    assert "graficos/test_subcarpeta/test_torta.png" in resultado
    mock_savefig.assert_called_once()
    mock_makedirs.assert_called_once()
    mock_close.assert_called_once()

from modules.graficos import GraficadoraHistograma

@patch("matplotlib.pyplot.savefig")
@patch("os.makedirs")
@patch("matplotlib.pyplot.close")
def test_graficadora_histograma(mock_close, mock_makedirs, mock_savefig):
    graficadora = GraficadoraHistograma()
    datos = [1, 2, 3, 4, 5]
    resultado = graficadora.graficar(datos, "Título", "X", "Y", "test_hist.png", "sub")
    
    assert "graficos/sub/test_hist.png" in resultado
    from modules.graficos import GraficadoraHistograma

@patch("matplotlib.pyplot.savefig")
@patch("os.makedirs")
@patch("matplotlib.pyplot.close")
def test_graficadora_histograma(mock_close, mock_makedirs, mock_savefig):
    graficadora = GraficadoraHistograma()
    datos = [1, 2, 3, 4, 5]
    resultado = graficadora.graficar(datos, "Título", "X", "Y", "test_hist.png", "sub")
    
    assert "graficos/sub/test_hist.png" in resultado
    mock_savefig.assert_called_once()
    mock_savefig.assert_called_once()
    
def test_graficadora_histograma_sin_datos():
    graficadora = GraficadoraHistograma()
    resultado = graficadora.graficar([], "Título", "X", "Y")
    assert resultado is None

from modules.graficos import GraficadoraNubePalabras
from unittest.mock import patch, MagicMock

@patch("os.makedirs")
@patch("wordcloud.WordCloud.to_file")
def test_graficadora_nube_palabras(mock_to_file, mock_makedirs):
    reclamos = [MagicMock(contenido="soporte técnico urgente urgente impresora")]
    graficadora = GraficadoraNubePalabras()
    resultado = graficadora.generar_nube_palabras(reclamos, "nube_test.png", "nube_test")
    
    assert "graficos/nube_test/nube_test.png" in resultado
    mock_to_file.assert_called_once()

if __name__ == "__main__":
    unittest.main()