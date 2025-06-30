from datetime import datetime, timedelta
from modules.modelos import ModeloReclamo
from sqlalchemy import func
from modules.config import crear_engine
from modules.repositorio import RepositorioReclamosSQLAlchemy
from collections import Counter
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
import os
from abc import ABC, abstractmethod
from reportlab.platypus import HRFlowable

engine, Session = crear_engine()

session = Session()

"""func es un objeto que provee SQLAlchemy para usar funciones SQL como COUNT(), AVG(), SUM(), MAX(), etc., dentro de consultas ORM."""

class GeneradorReportes:
    """Genera estadísticas y datos para reportes de reclamos."""

    def __init__(self, repositorio_reclamos):
        """Inicializa el generador con un repositorio de reclamos."""
        self.repositorio_reclamos = repositorio_reclamos

    def cantidad_total_reclamos(self):
        """Devuelve el total de reclamos en la base de datos."""
        return self.repositorio_reclamos.session.query(ModeloReclamo).count()

    def cantidad_reclamos_por_estado(self):
        """Devuelve un diccionario con la cantidad de reclamos por estado."""
        query = self.repositorio_reclamos.session.query(
            ModeloReclamo.estado, 
            func.count(ModeloReclamo.id)
        ).group_by(ModeloReclamo.estado).all()
        return dict(query)

    def cantidad_reclamos_por_clasificacion(self):
        """Devuelve un diccionario con la cantidad de reclamos por clasificación."""
        query = self.repositorio_reclamos.session.query(
            ModeloReclamo.clasificacion,
            func.count(ModeloReclamo.id)
        ).group_by(ModeloReclamo.clasificacion).all()
        return dict(query)

    def cantidad_promedio_adherentes(self):
        """Devuelve el promedio de adherentes por reclamo, o 0 si no hay reclamos."""
        query = self.repositorio_reclamos.session.query(
            func.avg(ModeloReclamo.cantidad_adherentes)
        ).scalar()
        return query or 0

    def reclamos_recientes(self, dias=7):
        """Devuelve una lista de reclamos creados en los últimos `dias` días."""
        fecha_limite = datetime.utcnow() - timedelta(days=dias)
        reclamos = self.repositorio_reclamos.session.query(ModeloReclamo).filter(
            ModeloReclamo.fecha_hora >= fecha_limite
        ).all()
        return reclamos

    def reclamos_por_usuario(self, usuario_id):
        """Devuelve una lista de reclamos creados por un usuario específico."""
        reclamos = self.repositorio_reclamos.session.query(ModeloReclamo).filter_by(
            usuario_id=usuario_id
        ).all()
        return reclamos
    
    def cantidad_reclamos_por_estado_filtrado(self, clasificacion):   
        """Devuelve un dict con la cantidad de reclamos por estado, filtrados por clasificación."""
        query = self.repositorio_reclamos.session.query(
            ModeloReclamo.estado,
            func.count(ModeloReclamo.id)
        ).filter_by(clasificacion=clasificacion).group_by(ModeloReclamo.estado).all()
        return dict(query)

    def reclamos_recientes_filtrado(self, clasificacion, dias=7):
        """Devuelve una lista de reclamos recientes filtrados por clasificación."""
        fecha_limite = datetime.utcnow() - timedelta(days=dias)
        return self.repositorio_reclamos.session.query(ModeloReclamo).filter(
            ModeloReclamo.fecha_hora >= fecha_limite,
            ModeloReclamo.clasificacion == clasificacion
        ).all()
        
    def listar_clasificaciones_unicas(self):
        """Devuelve una lista de clasificaciones únicas de reclamos."""
        clasificaciones = self.repositorio_reclamos.session.query(
            ModeloReclamo.clasificacion
        ).distinct().all()
        return [c[0] for c in clasificaciones]

    def clasificacion_por_rol(self, rol):
        """Devuelve la clasificación asociada a un rol específico."""
        try:
            rol = str(rol) 
        except ValueError:
            return None

        mapa_roles = {
            '1': 'soporte informático',
            '2': 'secretaría técnica',
            '3': 'maestranza'
        }
        return mapa_roles.get(rol)

    
    def obtener_datos_para_torta(self, rol):
        """Obtiene los datos necesarios para un gráfico de torta, filtrados por rol."""
        clasificacion = self.clasificacion_por_rol(rol)
        if clasificacion is None:
            return {}

        query = self.repositorio_reclamos.session.query(
            ModeloReclamo.estado,
            func.count(ModeloReclamo.id)
        ).filter(func.lower(ModeloReclamo.clasificacion) == clasificacion.lower()).group_by(ModeloReclamo.estado).all()

        return dict(query)

    def obtener_datos_para_histograma(self, rol):
        """Obtiene los datos necesarios para un histograma, filtrados por rol."""
        clasificacion = self.clasificacion_por_rol(rol)
        if clasificacion is None:
            return {}

        reclamos = self.repositorio_reclamos.session.query(ModeloReclamo).filter(
            func.lower(ModeloReclamo.clasificacion) == clasificacion.lower()
        ).all()

        agrupados_por_mes = Counter([r.fecha_hora.month for r in reclamos if r.fecha_hora])
        return dict(agrupados_por_mes)
    
    def obtener_cantidades_adherentes(self, dias=365, clasificacion=None):
        """Obtiene las cantidades de adherentes de reclamos recientes, opcionalmente filtrados por clasificación."""
        fecha_limite = datetime.utcnow() - timedelta(days=dias)
        query = self.repositorio_reclamos.session.query(ModeloReclamo).filter(
            ModeloReclamo.fecha_hora >= fecha_limite
        )
        if clasificacion:
            query = query.filter(ModeloReclamo.clasificacion == clasificacion)
        reclamos = query.all()
        return [r.cantidad_adherentes for r in reclamos if r.cantidad_adherentes is not None]
        
    def mediana_tiempo_resolucion(self, clasificacion=None):
        """Calcula la mediana del tiempo de resolución de reclamos resueltos, opcionalmente filtrados."""
        from modules.monticulos import MonticuloMediana  # Import aquí para evitar import circular

        # Filtrar reclamos resueltos
        query = self.repositorio_reclamos.session.query(ModeloReclamo.resuelto_en).filter(
            ModeloReclamo.estado == 'resuelto'
        )
        if clasificacion:
            query = query.filter(ModeloReclamo.clasificacion == clasificacion)

        resultados = query.all()
        print("Resultados de la consulta:", resultados)

        tiempos_resueltos = [reclamo.resuelto_en for reclamo in query if reclamo.resuelto_en is not None]

        # Verificar si hay datos
        if not tiempos_resueltos:
            return None

        # Calcular la mediana usando MonticuloMediana
        monticulo = MonticuloMediana(tiempos_resueltos)
        return monticulo.obtener_mediana()

    def calcular_mediana(self, atributo, clasificacion=None):
        """Calcula la mediana de un atributo de los reclamos, opcionalmente filtrados."""
        from modules.monticulos import MonticuloMediana  # Import aquí para evitar import circular

        # Filtrar reclamos
        query = self.repositorio_reclamos.session.query(getattr(ModeloReclamo, atributo))
        if clasificacion:
            query = query.filter(ModeloReclamo.clasificacion == clasificacion)

        # Obtener valores válidos del atributo
        valores = [r[0] for r in query.all() if r[0] is not None]

        # Verificar si hay datos
        if not valores:
            return None

        # Calcular la mediana usando MonticuloMediana
        monticulo = MonticuloMediana(valores)
        return monticulo.obtener_mediana()

    def calcular_medianas_atributos(self, clasificacion=None):
        """Calcula la mediana de atributos relevantes de los reclamos."""
        atributos_relevantes = ['cantidad_adherentes', 'tiempo_estimado', 'resuelto_en']
        medianas = {}

        for atributo in atributos_relevantes:
            medianas[atributo] = self.calcular_mediana(atributo, clasificacion)

        return medianas

class Reportes(ABC):
    """Clase abstracta para reportes de reclamos."""
    
    @abstractmethod
    def generar(self, ruta_salida, clasificacion_usuario):
        """Genera un reporte y lo guarda en la ruta especificada."""
        pass

class ReportePDF(Reportes):
    """Genera reportes de reclamos en formato PDF."""

    def __init__(self, generador: GeneradorReportes):
        """Inicializa el reporte PDF con un generador de reportes."""
        self.generador = generador

    def generar(self, ruta_salida, clasificacion_usuario):
        """Genera y guarda un reporte PDF de reclamos filtrados por clasificación."""
        carpeta = os.path.dirname(ruta_salida)
        if carpeta:
            os.makedirs(carpeta, exist_ok=True)

        doc = SimpleDocTemplate(
            ruta_salida, pagesize=A4,
            leftMargin=2 * cm, rightMargin=2 * cm,
            topMargin=2 * cm, bottomMargin=2 * cm
        )

        estilos = getSampleStyleSheet()
        estilo_normal = estilos["BodyText"]
        estilo_titulo = ParagraphStyle(
            'Titulo',
            parent=estilos["Heading1"],
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=colors.HexColor("#003366"),
            alignment=1,
            spaceAfter=12
        )
        estilo_subtitulo = ParagraphStyle(
            'Subtitulo',
            parent=estilos["Heading2"],
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=colors.HexColor("#003366"),
            spaceAfter=6
        )

        elementos = []

        # Título principal
        elementos.append(Paragraph(f"Reporte de Reclamos - {clasificacion_usuario.capitalize()}", estilo_titulo))
        elementos.append(Spacer(1, 0.25 * cm))

        # Línea azul decorativa
        elementos.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#00509e")))
        elementos.append(Spacer(1, 0.5 * cm))

        # Estadísticas con medianas
        mediana = self.generador.calcular_medianas_atributos(clasificacion=clasificacion_usuario)
        elementos.append(Paragraph(f"Estadísticas del Departamento: {clasificacion_usuario.capitalize()}", estilo_subtitulo))
        elementos.append(Spacer(1, 0.3 * cm))

        for atributo, mediana in mediana.items():
            texto = f"Mediana de {atributo.replace('_', ' ').capitalize()}: {mediana if mediana is not None else 'No disponible'}"
            elementos.append(Paragraph(texto, estilo_normal))

        elementos.append(Spacer(1, 1 * cm))

        # Listado de reclamos
        reclamos = self.generador.repositorio_reclamos.obtener_registros_por_filtro(
            filtro="clasificacion", valor=clasificacion_usuario
        )

        if not reclamos:
            elementos.append(Paragraph("No hay reclamos para esta clasificación.", estilo_normal))
        else:
            elementos.append(Paragraph("Listado de Reclamos:", estilo_subtitulo))
            elementos.append(Spacer(1, 0.3 * cm))

            # Datos de la tabla
            datos_tabla = [["ID", "Contenido", "Estado", "Fecha", "Adherentes", "Resuelto", "plazo"]]
            for reclamo in reclamos:
                datos_tabla.append([
                    str(reclamo.id),
                    Paragraph(reclamo.contenido, estilo_normal),
                    reclamo.estado,
                    reclamo.fecha_hora.strftime("%Y-%m-%d %H:%M:%S"),
                    str(reclamo.cantidad_adherentes or ""),
                    str(reclamo.resuelto_en if reclamo.resuelto_en else "No"),
                    str(reclamo.tiempo_estimado if reclamo.tiempo_estimado else "---")
                ])

            tabla = Table(datos_tabla, colWidths=[2 * cm, 5 * cm, 3 * cm, 4 * cm, 2.5 * cm, 2 * cm, 1.5 * cm])
            tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#00509e")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f9f9f9")),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#00509e")),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ]))
            elementos.append(tabla)
            elementos.append(Spacer(1, 0.5 * cm))
            
            estilo_glosario = ParagraphStyle(name="Grosario",fontName="Helvetica",fontSize=9,textColor=colors.grey,leading=11,spaceAfter=6)
            
            elementos.append(Paragraph("*Plazo: Tiempo estimado para resolver el reclamo.", estilo_glosario))

        doc.build(elementos)
        print(f"Reporte PDF generado en: {ruta_salida}")

class ReporteHTML(Reportes):
    """Genera reportes de reclamos en formato HTML."""

    def __init__(self, generador: GeneradorReportes):
        """Inicializa el reporte HTML con un generador de reportes."""
        self.generador = generador

    def generar(self, ruta_salida, clasificacion_usuario):
        """Genera y guarda un reporte HTML de reclamos filtrados por clasificación."""
        import os

        carpeta = os.path.dirname(ruta_salida)
        if carpeta:
            os.makedirs(carpeta, exist_ok=True)

        medianas = self.generador.calcular_medianas_atributos(clasificacion=clasificacion_usuario)

        reclamos = self.generador.repositorio_reclamos.obtener_registros_por_filtro(
            filtro="clasificacion", valor=clasificacion_usuario
        )

        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reporte de Reclamos - {clasificacion_usuario.capitalize()}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    padding: 0;
                }}
                h1 {{
                    color: #003366;
                    text-align: center;
                }}
                h2 {{
                    color: #00509e;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th, td {{
                    border: 1px solid #00509e;
                    padding: 8px;
                    text-align: center;
                }}
                th {{
                    background-color: #00509e;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <h1>Reporte de Reclamos - {clasificacion_usuario.capitalize()}</h1>
            <h2>Estadísticas del Departamento</h2>
            <ul>
        """

        for atributo, mediana in medianas.items():
            html += f"<li>Mediana de {atributo.replace('_', ' ').capitalize()}: {mediana if mediana is not None else 'No disponible'}</li>"

        html += "</ul>"

        html += """
            <h2>Listado de Reclamos</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Contenido</th>
                        <th>Estado</th>
                        <th>Fecha</th>
                        <th>Adherentes</th>
                        <th>Resuelto en</th>
                        <th>Tiempo estimado</th>
                    </tr>
                </thead>
                <tbody>
        """

        if not reclamos:
            html += "<tr><td colspan='5'>No hay reclamos para esta clasificación.</td></tr>"
        else:
            for reclamo in reclamos:
                html += f"""
                    <tr>
                        <td>{reclamo.id}</td>
                        <td>{reclamo.contenido}</td>
                        <td>
                            {('<strong style="color: #003366;">{}</strong>'.format(reclamo.estado) if reclamo.estado == "resuelto" else "pendiente")}
                        </td>
                        <td>{reclamo.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}</td>
                        <td>{reclamo.cantidad_adherentes}</td>
                        <td>{reclamo.resuelto_en if reclamo.resuelto_en else 'No resuelto'}</td>
                        <td>{reclamo.tiempo_estimado if reclamo.tiempo_estimado else 'No disponible'}</td>
                    </tr>
                """

        html += """
                </tbody>
            </table>
        </body>
        </html>
        """

        with open(ruta_salida, "w", encoding="utf-8") as archivo:
            archivo.write(html)

        print(f"Reporte HTML generado en: {ruta_salida}")


if __name__ == '__main__':  # pragma: no cover
    repo_reclamos = RepositorioReclamosSQLAlchemy(session)
    generador = GeneradorReportes(repo_reclamos)

    # Mediana para todos los reclamos resueltos
    mediana_general = generador.mediana_tiempo_resolucion()
    print("Mediana general del tiempo de resolución:", mediana_general)

    # Mediana para una clasificación específica
    mediana_maestranza = generador.mediana_tiempo_resolucion(clasificacion="maestranza")
    print("Mediana del tiempo de resolución para maestranza:", mediana_maestranza)
   # print("Cantidad total de reclamos:", generador.cant_reclamos())

    # Reporte en PDF
    reporte_pdf = ReportePDF(generador)
    reporte_pdf.generar("data/salida_reporte.pdf", "maestranza")


