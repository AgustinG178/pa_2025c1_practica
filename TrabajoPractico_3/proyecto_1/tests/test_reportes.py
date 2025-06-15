import unittest
from unittest.mock import MagicMock, patch
from modules.reportes import GeneradorReportes, ReportePDF, ReporteHTML
from modules.modelos import ModeloReclamo
from datetime import datetime, timedelta

class DummyRepo:
    def __init__(self):
        self.session = MagicMock()

class TestGeneradorReportes(unittest.TestCase):
    """Tests para la clase GeneradorReportes usando mocks."""

    def setUp(self):
        self.repo = DummyRepo()
        self.generador = GeneradorReportes(self.repo)

    def test_cantidad_total_reclamos(self):
        """Verifica que retorna la cantidad total de reclamos usando un mock."""
        self.repo.session.query.return_value.count.return_value = 5
        self.assertEqual(self.generador.cantidad_total_reclamos(), 5)

    def test_cantidad_reclamos_por_estado(self):
        """Verifica que retorna la cantidad de reclamos por estado."""
        self.repo.session.query.return_value.group_by.return_value.all.return_value = [("pendiente", 2)]
        self.assertEqual(self.generador.cantidad_reclamos_por_estado(), {"pendiente": 2})

    def test_cantidad_reclamos_por_clasificacion(self):
        """Verifica que retorna la cantidad de reclamos por clasificación."""
        self.repo.session.query.return_value.group_by.return_value.all.return_value = [("soporte", 3)]
        self.assertEqual(self.generador.cantidad_reclamos_por_clasificacion(), {"soporte": 3})

    def test_cantidad_promedio_adherentes(self):
        """Verifica que retorna el promedio de adherentes usando un mock."""
        self.repo.session.query.return_value.scalar.return_value = 2.5
        self.assertEqual(self.generador.cantidad_promedio_adherentes(), 2.5)
        self.repo.session.query.return_value.scalar.return_value = None
        self.assertEqual(self.generador.cantidad_promedio_adherentes(), 0)

    def test_reclamos_recientes(self):
        """Verifica que retorna los reclamos recientes usando un mock."""
        dummy = MagicMock()
        self.repo.session.query.return_value.filter.return_value.all.return_value = [dummy]
        self.assertEqual(self.generador.reclamos_recientes(), [dummy])

    def test_reclamos_por_usuario(self):
        """Verifica que retorna los reclamos de un usuario dado."""
        dummy = MagicMock()
        self.repo.session.query.return_value.filter_by.return_value.all.return_value = [dummy]
        self.assertEqual(self.generador.reclamos_por_usuario(1), [dummy])

    def test_cantidad_reclamos_por_estado_filtrado(self):
        """Verifica que retorna la cantidad de reclamos por estado filtrado."""
        self.repo.session.query.return_value.filter_by.return_value.group_by.return_value.all.return_value = [("pendiente", 1)]
        self.assertEqual(self.generador.cantidad_reclamos_por_estado_filtrado("soporte"), {"pendiente": 1})

    def test_reclamos_recientes_filtrado(self):
        """Verifica que retorna los reclamos recientes filtrados por clasificación."""
        dummy = MagicMock()
        self.repo.session.query.return_value.filter.return_value.all.return_value = [dummy]
        self.assertEqual(self.generador.reclamos_recientes_filtrado("soporte"), [dummy])

    def test_listar_clasificaciones_unicas(self):
        """Verifica que retorna las clasificaciones únicas."""
        self.repo.session.query.return_value.distinct.return_value.all.return_value = [("soporte",), ("tecnica",)]
        self.assertEqual(self.generador.listar_clasificaciones_unicas(), ["soporte", "tecnica"])

    def test_clasificacion_por_rol(self):
        """Verifica la conversión de rol a clasificación y el manejo de errores."""
        self.assertEqual(self.generador.clasificacion_por_rol(1), "soporte informático")
        self.assertEqual(self.generador.clasificacion_por_rol("2"), "secretaría técnica")
        self.assertEqual(self.generador.clasificacion_por_rol("noesnumero"), None)
        self.assertEqual(self.generador.clasificacion_por_rol(99), None)

    def test_obtener_datos_para_torta(self):
        """Verifica que retorna los datos para graficar una torta por estado."""
        # Simula distintos estados y cantidades
        self.generador.clasificacion_por_rol = MagicMock(return_value="soporte")
        estados = ["pendiente", "en proceso", "resuelto"]
        # Simula que el query devuelve diferentes estados
        for estado in estados:
            self.repo.session.query.return_value.filter.return_value.group_by.return_value.all.return_value = [(estado, 2)]
            resultado = self.generador.obtener_datos_para_torta(1)
            self.assertIn(estado, resultado)
            self.assertEqual(resultado[estado], 2)
        # Caso de rol inválido
        self.generador.clasificacion_por_rol = MagicMock(return_value=None)
        self.assertEqual(self.generador.obtener_datos_para_torta(99), {})

class TestReportePDFHTML(unittest.TestCase):
    """Tests para las clases ReportePDF y ReporteHTML."""

    def setUp(self):
        self.generador = MagicMock()
        self.generador.cantidad_total_reclamos.return_value = 1
        self.generador.cantidad_promedio_adherentes.return_value = 2.0
        self.generador.cantidad_reclamos_por_estado.return_value = {"pendiente": 1}
        self.generador.cantidad_reclamos_por_clasificacion.return_value = {"soporte": 1}
        self.generador.reclamos_recientes.return_value = [MagicMock(id=1, contenido="Test", estado="pendiente")]
        self.reporte_pdf = ReportePDF(self.generador)
        self.reporte_html = ReporteHTML(self.generador)

    @patch("modules.reportes.canvas")
    @patch("modules.reportes.A4", (100, 200))
    @patch("modules.reportes.cm", 1)
    def test_generarPDF(self, mock_canvas):
        """Verifica que se puede generar un PDF usando mocks."""
        c = MagicMock()
        mock_canvas.Canvas.return_value = c
        self.reporte_pdf.generarPDF(".")

    @patch("modules.reportes.Environment")
    @patch("modules.reportes.FileSystemLoader")
    @patch("modules.reportes.webbrowser.open")
    def test_exportar_html(self, mock_web, mock_loader, mock_env):
        """Verifica que se puede exportar un HTML usando mocks."""
        template = MagicMock()
        template.render.return_value = "<html></html>"
        mock_env.return_value.get_template.return_value = template
        self.reporte_html.exportar_html("test_reporte.html")

    def test_obtener_datos_reporte(self):
        """Verifica que se obtienen los datos necesarios para el reporte HTML."""
        datos = self.reporte_html.obtener_datos_reporte()
        self.assertIn("total", datos)
        self.assertIn("promedio", datos)
        self.assertIn("reclamos_por_estado", datos)
        self.assertIn("reclamos_por_clasificacion", datos)
        self.assertIn("reclamos_recientes", datos)

if __name__ == "__main__":
    unittest.main()