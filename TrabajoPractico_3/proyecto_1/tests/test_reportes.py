import unittest
from unittest.mock import MagicMock, patch
from modules.reportes import ReportePDF, GeneradorReportes
from modules.modelos import ModeloReclamo
from reportlab.platypus import SimpleDocTemplate
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
        # Simular datos en el repositorio
        self.repo.session.query.return_value.group_by.return_value.all.return_value = [
            ("pendiente", 3), ("resuelto", 2)
        ]

        resultado = self.generador.cantidad_reclamos_por_estado()
        self.assertEqual(resultado, {"pendiente": 3, "resuelto": 2})
        self.repo.session.query.assert_called_once()

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
        """Verifica que se obtienen los reclamos recientes correctamente."""
        # Crear reclamos de prueba
        reclamo1 = ModeloReclamo(
            estado="pendiente",
            fecha_hora=datetime.now() - timedelta(days=3),
            contenido="Reclamo reciente",
            clasificacion="soporte",
            cantidad_adherentes=2,
        )
        reclamo2 = ModeloReclamo(
            estado="pendiente",
            fecha_hora=datetime.now() - timedelta(days=10),
            contenido="Reclamo antiguo",
            clasificacion="soporte",
            cantidad_adherentes=1,
        )
        self.repo.session.add_all([reclamo1, reclamo2])
        self.repo.session.commit()

        # Obtener reclamos recientes
        recientes = self.generador.reclamos_recientes(dias=7)
        self.assertEqual(len(recientes), 1)
        self.assertEqual(recientes[0].contenido, "Reclamo reciente")

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

    def test_reclamos_recientes_filtrado(self):
        """Verifica que se obtienen los reclamos recientes filtrados por clasificación."""
        reclamo1 = ModeloReclamo(
            estado="pendiente",
            fecha_hora=datetime.now() - timedelta(days=3),
            contenido="Reclamo reciente",
            clasificacion="soporte",
            cantidad_adherentes=2,
        )
        reclamo2 = ModeloReclamo(
            estado="pendiente",
            fecha_hora=datetime.now() - timedelta(days=3),
            contenido="Reclamo reciente maestranza",
            clasificacion="maestranza",
            cantidad_adherentes=1,
        )
        self.session.add_all([reclamo1, reclamo2])
        self.session.commit()

        recientes = self.generador.reclamos_recientes_filtrado(clasificacion="soporte", dias=7)
        self.assertEqual(len(recientes), 1)
        self.assertEqual(recientes[0].clasificacion, "soporte")
        
    def test_listar_clasificaciones_unicas(self):
        """Verifica que se obtienen las clasificaciones únicas correctamente."""
        reclamo1 = ModeloReclamo(
            estado="pendiente",
            fecha_hora=datetime.now(),
            contenido="Reclamo 1",
            clasificacion="soporte",
            cantidad_adherentes=2,
        )
        reclamo2 = ModeloReclamo(
            estado="pendiente",
            fecha_hora=datetime.now(),
            contenido="Reclamo 2",
            clasificacion="maestranza",
            cantidad_adherentes=1,
        )
        self.session.add_all([reclamo1, reclamo2])
        self.session.commit()

        clasificaciones = self.generador.listar_clasificaciones_unicas()
        self.assertIn("soporte", clasificaciones)
        self.assertIn("maestranza", clasificaciones)    
        
    def test_clasificacion_por_rol(self):
        """Verifica que se obtiene la clasificación correcta según el rol."""
        self.assertEqual(self.generador.clasificacion_por_rol("1"), "soporte informático")
        self.assertEqual(self.generador.clasificacion_por_rol("2"), "secretaría técnica")
        self.assertEqual(self.generador.clasificacion_por_rol("3"), "maestranza")
        self.assertIsNone(self.generador.clasificacion_por_rol("4"))
        
    def test_obtener_datos_para_torta(self):
        """Verifica que se obtienen los datos para el gráfico de torta correctamente."""
        reclamo1 = ModeloReclamo(
            estado="pendiente",
            fecha_hora=datetime.now(),
            contenido="Reclamo 1",
            clasificacion="soporte informático",
            cantidad_adherentes=2,
        )
        reclamo2 = ModeloReclamo(
            estado="resuelto",
            fecha_hora=datetime.now(),
            contenido="Reclamo 2",
            clasificacion="soporte informático",
            cantidad_adherentes=1,
        )
        self.session.add_all([reclamo1, reclamo2])
        self.session.commit()

        datos_torta = self.generador.obtener_datos_para_torta(rol="1")
        self.assertEqual(datos_torta, {"pendiente": 1, "resuelto": 1})
        
    def test_obtener_datos_para_histograma(self):
        """Verifica que se obtienen los datos para el histograma correctamente."""
        reclamo1 = ModeloReclamo(
            estado="pendiente",
            fecha_hora=datetime(2025, 6, 1),
            contenido="Reclamo 1",
            clasificacion="soporte informático",
            cantidad_adherentes=2,
        )
        reclamo2 = ModeloReclamo(
            estado="pendiente",
            fecha_hora=datetime(2025, 6, 15),
            contenido="Reclamo 2",
            clasificacion="soporte informático",
            cantidad_adherentes=1,
        )
        self.session.add_all([reclamo1, reclamo2])
        self.session.commit()

        datos_histograma = self.generador.obtener_datos_para_histograma(rol="1")
        self.assertEqual(datos_histograma, {6: 2})  # Mes 6 (junio) tiene 2 reclamos
        
    def test_obtener_datos_para_histograma(self):
        """Verifica que se obtienen los datos para el histograma correctamente."""
        # Simula datos de reclamos
        self.repo.session.query.return_value.filter.return_value.group_by.return_value.all.return_value = [
            (1, 5), (2, 10), (3, 15)
        ]
        resultado = self.generador.obtener_datos_para_histograma(1)
        self.assertEqual(resultado, {1: 5, 2: 10, 3: 15})
    
    def test_calcular_medianas_atributos(self):
        """Verifica que se calculan las medianas de los atributos correctamente."""
        reclamo1 = ModeloReclamo(
            estado="resuelto",
            fecha_hora=datetime.now(),
            contenido="Reclamo 1",
            clasificacion="soporte",
            cantidad_adherentes=2,
            tiempo_estimado=5,
            resuelto_en=3,
        )
        reclamo2 = ModeloReclamo(
            estado="resuelto",
            fecha_hora=datetime.now(),
            contenido="Reclamo 2",
            clasificacion="soporte",
            cantidad_adherentes=4,
            tiempo_estimado=7,
            resuelto_en=5,
        )
        self.session.add_all([reclamo1, reclamo2])
        self.session.commit()

        medianas = self.generador.calcular_medianas_atributos(clasificacion="soporte")
        self.assertEqual(medianas["cantidad_adherentes"], 3)
        self.assertEqual(medianas["tiempo_estimado"], 6)
        self.assertEqual(medianas["resuelto_en"], 4)
        
    def test_cantidad_reclamos_por_estado_filtrado(self):
        """Verifica que retorna la cantidad de reclamos por estado filtrado."""
        self.repo.session.query.return_value.filter_by.return_value.group_by.return_value.all.return_value = [
            ("pendiente", 1), ("resuelto", 2)
        ]
        resultado = self.generador.cantidad_reclamos_por_estado_filtrado("soporte informático")
        self.assertEqual(resultado, {"pendiente": 1, "resuelto": 2})
        
    @patch("modules.reportes.SimpleDocTemplate")
    @patch("modules.reportes.Paragraph")
    @patch("modules.reportes.Table")
    @patch("modules.reportes.os.makedirs")
    def test_generarPDF(self, mock_makedirs, mock_table, mock_paragraph, mock_doc_template):
        """Test para cubrir el método generarPDF de ReportePDF."""
        # Mock de reclamos
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
        self.generador.repositorio_reclamos.obtener_registros_por_filtro.return_value = reclamos_mock

        # Mock del documento PDF
        doc_mock = MagicMock()
        mock_doc_template.return_value = doc_mock

        # Ejecutar el método
        self.reporte_pdf.generarPDF("test_output/reporte.pdf", "maestranza")

        # Verificar que se construyó el documento PDF
        doc_mock.build.assert_called_once()

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

    def test_mediana_tiempo_resolucion(self):
        # Simular datos en el repositorio
        self.repo.session.query.return_value.filter.return_value.all.return_value = [
            (5,), (10,), (15,)
        ]

        resultado = self.generador.mediana_tiempo_resolucion()
        self.assertEqual(resultado, 10)  # Mediana de [5, 10, 15]

class TestReportePDF(unittest.TestCase):
    def setUp(self):
        # Mock del generador de reportes
        self.generador_mock = MagicMock(spec=GeneradorReportes)
        self.reporte_pdf = ReportePDF(self.generador_mock)

    @patch("modules.reportes.SimpleDocTemplate")
    @patch("modules.reportes.Paragraph")
    @patch("modules.reportes.Table")
    @patch("modules.reportes.os.makedirs")
    def test_generarPDF(self, mock_makedirs, mock_table, mock_paragraph, mock_doc_template):
        """
        Test para cubrir el método generarPDF de ReportePDF.
        """
        # Mock de reclamos
        reclamos_mock = [
            ModeloReclamo(
                id=1,
                estado="pendiente",
                fecha_hora=datetime(2025, 6, 15, 12, 0, 0),
                contenido="Reclamo de prueba 1",
                clasificacion="maestranza",
                cantidad_adherentes=3,
            ),
            ModeloReclamo(
                id=2,
                estado="resuelto",
                fecha_hora=datetime(2025, 6, 14, 10, 0, 0),
                contenido="Reclamo de prueba 2",
                clasificacion="maestranza",
                cantidad_adherentes=5,
            ),
        ]

        # Mock de medianas
        medianas_mock = {
            "cantidad_adherentes": 4,
            "tiempo_estimado": 7,
            "resuelto_en": 3,
        }

        # Configurar el generador de reportes mock
        self.generador_mock.calcular_medianas_atributos.return_value = medianas_mock
        self.generador_mock.repositorio_reclamos.obtener_registros_por_filtro.return_value = reclamos_mock

        # Mock del documento PDF
        doc_mock = MagicMock(spec=SimpleDocTemplate)
        mock_doc_template.return_value = doc_mock

        # Ejecutar el método
        self.reporte_pdf.generarPDF("test_output/reporte.pdf", "maestranza")

        # Verificar que se crearon las carpetas necesarias
        mock_makedirs.assert_called_once_with("test_output", exist_ok=True)

        # Verificar que se generaron los elementos del PDF
        self.generador_mock.calcular_medianas_atributos.assert_called_once_with(clasificacion="maestranza")
        self.generador_mock.repositorio_reclamos.obtener_registros_por_filtro.assert_called_once_with(
            filtro="clasificacion", valor="maestranza"
        )

        # Verificar que se construyó el documento PDF
        doc_mock.build.assert_called_once()

        # Verificar que se generaron los elementos del contenido
        self.assertTrue(mock_paragraph.called)
        self.assertTrue(mock_table.called)


if __name__ == "__main__":
    unittest.main()