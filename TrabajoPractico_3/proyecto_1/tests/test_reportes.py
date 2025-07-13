import unittest
from unittest.mock import MagicMock, patch
from modules.reportes import ReportePDF, GeneradorReportes
from modules.modelos import ModeloReclamo
from datetime import datetime

class DummyRepo:
    def __init__(self):
        self.session = MagicMock()

    def obtener_reclamos_por_filtro(self, filtro, valor):
        return []
class DummyReclamo:
    def __init__(self, cantidad_adherentes):
        self.cantidad_adherentes = cantidad_adherentes

class TestGeneradorReportes(unittest.TestCase):
    def setUp(self):
        self.repo = DummyRepo()
        self.generador = GeneradorReportes(self.repo)
        self.reporte_pdf = ReportePDF(self.generador)

    def test_cantidad_total_reclamos(self):
        self.repo.session.query.return_value.count.return_value = 5
        self.assertEqual(self.generador.cantidad_total_reclamos(), 5)

    def test_cantidad_reclamos_por_estado(self):
        self.repo.session.query.return_value.group_by.return_value.all.return_value = [
            ("pendiente", 3), ("resuelto", 2)
        ]
        resultado = self.generador.cantidad_reclamos_por_estado()
        self.assertEqual(resultado, {"pendiente": 3, "resuelto": 2})

    def test_cantidad_reclamos_por_clasificacion(self):
        self.repo.session.query.return_value.group_by.return_value.all.return_value = [("soporte", 3)]
        self.assertEqual(self.generador.cantidad_reclamos_por_clasificacion(), {"soporte": 3})

    def test_cantidad_promedio_adherentes(self):
        self.repo.session.query.return_value.scalar.return_value = 2.5
        self.assertEqual(self.generador.cantidad_promedio_adherentes(), 2.5)
        self.repo.session.query.return_value.scalar.return_value = None
        self.assertEqual(self.generador.cantidad_promedio_adherentes(), 0)

    def test_reclamos_por_usuario(self):
        dummy = MagicMock()
        self.repo.session.query.return_value.filter_by.return_value.all.return_value = [dummy]
        self.assertEqual(self.generador.reclamos_por_usuario(1), [dummy])

    def test_cantidad_reclamos_por_estado_filtrado(self):
        self.repo.session.query.return_value.filter_by.return_value.group_by.return_value.all.return_value = [
            ("pendiente", 1)
        ]
        self.assertEqual(self.generador.cantidad_reclamos_por_estado_filtrado("soporte"), {"pendiente": 1})

    def test_listar_clasificaciones_unicas(self):
        self.repo.session.query.return_value.distinct.return_value.all.return_value = [("soporte",), ("tecnica",)]
        self.assertEqual(self.generador.listar_clasificaciones_unicas(), ["soporte", "tecnica"])

    def test_clasificacion_por_rol(self):
        self.assertEqual(self.generador.clasificacion_por_rol("2"), "soporte informático")
        self.assertEqual(self.generador.clasificacion_por_rol("3"), "secretaría técnica")
        self.assertEqual(self.generador.clasificacion_por_rol("4"), "maestranza")
        self.assertIsNone(self.generador.clasificacion_por_rol("1"))

    def test_obtener_datos_para_histograma(self):

        reclamos_simulados = [DummyReclamo(6), DummyReclamo(2), DummyReclamo(None)]

        self.repo.session.query.return_value.filter.return_value.all.return_value = reclamos_simulados

        datos = self.generador.obtener_datos_para_histograma("2")
        self.assertEqual(datos, [6,2])

    def test_mediana_tiempo_resolucion(self):
        dummy = MagicMock(resuelto_en=10)
        self.repo.session.query.return_value.filter.return_value.__iter__.return_value = [dummy]
        self.repo.session.query.return_value.filter.return_value.all.return_value = [(10,)]
        resultado = self.generador.mediana_tiempo_resolucion()
        self.assertEqual(resultado, 10)

    @patch("modules.reportes.SimpleDocTemplate")
    @patch("modules.reportes.Paragraph")
    @patch("modules.reportes.Table")
    @patch("modules.reportes.os.makedirs")
    def test_generarPDF(self, mock_makedirs, mock_table, mock_paragraph, mock_doc_template):
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
        self.generador._repositorio_reclamos.obtener_registros_por_filtro = MagicMock(return_value=reclamos_mock)
        self.generador.calcular_medianas_atributos = MagicMock(return_value={
            "cantidad_adherentes": 3,
            "tiempo_estimado": 5,
            "resuelto_en": 2
        })
        doc_mock = MagicMock()
        mock_doc_template.return_value = doc_mock

        self.reporte_pdf.generar("test_output/reporte.pdf", "maestranza")
        doc_mock.build.assert_called_once()
        mock_makedirs.assert_called_once()
        self.assertTrue(mock_paragraph.called)
        self.assertTrue(mock_table.called)

if __name__ == "__main__":
    unittest.main()
