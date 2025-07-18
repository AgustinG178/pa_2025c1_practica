import unittest
from unittest.mock import MagicMock, patch
from modules.reportes import ReportePDF, GeneradorReportes
from modules.modelos import ModeloReclamo
from datetime import datetime, timedelta

class DummyRepo:
    def __init__(self):
        self.session = MagicMock()

    def obtener_registros_por_filtro(self, filtro, valor):
        return []

class TestGeneradorReportes(unittest.TestCase):
    def setUp(self):
        # Arrange: Configura el repo y generador para cada test
        self.repo = DummyRepo()
        self.generador = GeneradorReportes(self.repo)
        self.reporte_pdf = ReportePDF(self.generador)

    def test_cantidad_total_reclamos(self):
        # Arrange
        self.repo.session.query.return_value.count.return_value = 5
        # Act
        resultado = self.generador.cantidad_total_reclamos()
        # Assert
        self.assertEqual(resultado, 5)

    def test_cantidad_reclamos_por_estado(self):
        # Arrange
        self.repo.session.query.return_value.group_by.return_value.all.return_value = [
            ("pendiente", 3), ("resuelto", 2)
        ]
        # Act
        resultado = self.generador.cantidad_reclamos_por_estado()
        # Assert
        self.assertEqual(resultado, {"pendiente": 3, "resuelto": 2})

    def test_cantidad_reclamos_por_clasificacion(self):
        # Arrange
        self.repo.session.query.return_value.group_by.return_value.all.return_value = [("soporte", 3)]
        # Act
        resultado = self.generador.cantidad_reclamos_por_clasificacion()
        # Assert
        self.assertEqual(resultado, {"soporte": 3})

    def test_reclamos_por_usuario(self):
        # Arrange
        dummy = MagicMock()
        self.repo.session.query.return_value.filter_by.return_value.all.return_value = [dummy]
        # Act
        resultado = self.generador.reclamos_por_usuario(1)
        # Assert
        self.assertEqual(resultado, [dummy])

    def test_cantidad_reclamos_por_estado_filtrado(self):
        # Arrange
        self.repo.session.query.return_value.filter_by.return_value.group_by.return_value.all.return_value = [
            ("pendiente", 1)
        ]
        # Act
        resultado = self.generador.cantidad_reclamos_por_estado_filtrado("soporte")
        # Assert
        self.assertEqual(resultado, {"pendiente": 1})

    def test_clasificacion_por_rol(self):
        # Act & Assert
        self.assertEqual(self.generador.clasificacion_por_rol("1"), "soporte informático")
        self.assertEqual(self.generador.clasificacion_por_rol("2"), "secretaría técnica")
        self.assertEqual(self.generador.clasificacion_por_rol("3"), "maestranza")
        self.assertIsNone(self.generador.clasificacion_por_rol("4"))

    def test_obtener_datos_para_histograma(self):
        # Arrange
        reclamo1 = MagicMock(fecha_hora=datetime(2025, 6, 1))
        reclamo2 = MagicMock(fecha_hora=datetime(2025, 6, 15))
        self.repo.session.query.return_value.filter.return_value.all.return_value = [reclamo1, reclamo2]
        # Act
        datos = self.generador.obtener_datos_para_histograma("1")
        # Assert
        self.assertEqual(datos, {6: 2})

    def test_mediana_tiempo_resolucion(self):
        # Arrange
        dummy = MagicMock(resuelto_en=10)
        self.repo.session.query.return_value.filter.return_value.__iter__.return_value = [dummy]
        self.repo.session.query.return_value.filter.return_value.all.return_value = [(10,)]
        # Act
        resultado = self.generador.mediana_tiempo_resolucion()
        # Assert
        self.assertEqual(resultado, 10)

    @patch("modules.reportes.SimpleDocTemplate")
    @patch("modules.reportes.Paragraph")
    @patch("modules.reportes.Table")
    @patch("modules.reportes.os.makedirs")
    def test_generarPDF(self, mock_makedirs, mock_table, mock_paragraph, mock_doc_template):
        # Arrange
        reclamos_mock = [
            ModeloReclamo(
                id=1,
                estado="pendiente",
                fecha_hora=datetime(2025, 6, 15, 12, 0, 0),
                contenido="Reclamo de prueba 1",
                clasificacion="maestranza",
                cantidad_adherentes=3,
            )
        ]
        self.generador.repositorio_reclamos.obtener_registros_por_filtro = MagicMock(return_value=reclamos_mock)
        self.generador.calcular_medianas_atributos = MagicMock(return_value={
            "cantidad_adherentes": 3,
            "tiempo_estimado": 5,
            "resuelto_en": 2
        })
        doc_mock = MagicMock()
        mock_doc_template.return_value = doc_mock

        # Act
        self.reporte_pdf.generar("test_output/reporte.pdf", "maestranza")

        # Assert
        doc_mock.build.assert_called_once()
        mock_makedirs.assert_called_once()
        self.assertTrue(mock_paragraph.called)
        self.assertTrue(mock_table.called)

if __name__ == "__main__":
    unittest.main()

