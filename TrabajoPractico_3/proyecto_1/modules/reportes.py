from datetime import datetime, timedelta
from modules.modelos import ModeloReclamo
from sqlalchemy import func
from modules.config import crear_engine
from modules.repositorio import RepositorioReclamosSQLAlchemy
from collections import Counter
from modules.login import FlaskLoginUser
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

engine, Session = crear_engine()

session = Session()

"""func es un objeto que provee SQLAlchemy para usar funciones SQL como COUNT(), AVG(), SUM(), MAX(), etc., dentro de tus consultas ORM."""

class GeneradorReportes:
    def __init__(self, repositorio_reclamos):
        self.repositorio_reclamos = repositorio_reclamos

    def cantidad_total_reclamos(self):
        """
        Devuelve el total de reclamos en la base de datos.
        """
        return self.repositorio_reclamos.session.query(ModeloReclamo).count()

    def cantidad_reclamos_por_estado(self):
        """
        Devuelve un diccionario con la cantidad de reclamos agrupados por estado.
        """
        query = self.repositorio_reclamos.session.query(
            ModeloReclamo.estado, 
            func.count(ModeloReclamo.id)
        ).group_by(ModeloReclamo.estado).all()
        return dict(query)

    def cantidad_reclamos_por_clasificacion(self):
        """
        Devuelve un diccionario con la cantidad de reclamos agrupados por clasificación.
        """
        query = self.repositorio_reclamos.session.query(
            ModeloReclamo.clasificacion,
            func.count(ModeloReclamo.id)
        ).group_by(ModeloReclamo.clasificacion).all()
        return dict(query)

    def cantidad_promedio_adherentes(self):
        """
        Devuelve el promedio de adherentes por reclamo. En caso de que no haya reclamos se devuelve 0.
        """
        query = self.repositorio_reclamos.session.query(
            func.avg(ModeloReclamo.cantidad_adherentes)
        ).scalar()
        return query or 0

    def reclamos_recientes(self, dias=7):
        """
        Devuelve una lista de los reclamos creados en los últimos `dias` días.
        """
        fecha_limite = datetime.utcnow() - timedelta(days=dias)
        reclamos = self.repositorio_reclamos.session.query(ModeloReclamo).filter(
            ModeloReclamo.fecha_hora >= fecha_limite
        ).all()
        return reclamos

    def reclamos_por_usuario(self, usuario_id):
        """
        Devuelve una lista de reclamos creados por un usuario específico.
        """
        reclamos = self.repositorio_reclamos.session.query(ModeloReclamo).filter_by(
            usuario_id=usuario_id
        ).all()
        return reclamos
    
    def cantidad_reclamos_por_estado_filtrado(self, clasificacion):   
        """
        Devuelve un diccionario con la cantidad de reclamos agrupados por estado, filtrados por clasificación.
        """ 
        query = self.repositorio_reclamos.session.query(
            ModeloReclamo.estado,
            func.count(ModeloReclamo.id)
        ).filter_by(clasificacion=clasificacion).group_by(ModeloReclamo.estado).all()
        return dict(query)

    def reclamos_recientes_filtrado(self, clasificacion, dias=7):
        """
        Devuelve una lista de reclamos recientes filtrados por clasificación.
        """
        fecha_limite = datetime.utcnow() - timedelta(days=dias)
        return self.repositorio_reclamos.session.query(ModeloReclamo).filter(
            ModeloReclamo.fecha_hora >= fecha_limite,
            ModeloReclamo.clasificacion == clasificacion
        ).all()
        
    def listar_clasificaciones_unicas(self):
        """
        Devuelve una lista de clasificaciones únicas de reclamos en la base de datos.
        """
        clasificaciones = self.repositorio_reclamos.session.query(
            ModeloReclamo.clasificacion
        ).distinct().all()
        return [c[0] for c in clasificaciones]

    def clasificacion_por_rol(self, rol):
        """
        Devuelve la clasificación asociada a un rol específico.
        """
        try:
            rol_int = int(rol)
        except ValueError:
            return None

        mapa_roles = {
            1: 'soporte informático',
            2: 'secretaría técnica',
            3: 'maestranza'
        }
        return mapa_roles.get(rol_int)
    
    def obtener_datos_para_torta(self, rol):
        """
        Obtiene los datos necesarios para generar un gráfico de torta, filtrados por rol.
        """
        clasificacion = self.clasificacion_por_rol(rol)
        if clasificacion is None:
            return {}

        query = self.repositorio_reclamos.session.query(
            ModeloReclamo.estado,
            func.count(ModeloReclamo.id)
        ).filter(func.lower(ModeloReclamo.clasificacion) == clasificacion.lower()).group_by(ModeloReclamo.estado).all()

        return dict(query)

    def obtener_datos_para_histograma(self, rol):
        """
        Obtiene los datos necesarios para generar un histograma, filtrados por rol.
        """
        clasificacion = self.clasificacion_por_rol(rol)
        if clasificacion is None:
            return {}

        reclamos = self.repositorio_reclamos.session.query(ModeloReclamo).filter(
            func.lower(ModeloReclamo.clasificacion) == clasificacion.lower()
        ).all()

        agrupados_por_mes = Counter([r.fecha_hora.month for r in reclamos if r.fecha_hora])
        return dict(agrupados_por_mes)
    
    def obtener_cantidades_adherentes(self, dias=365, clasificacion=None):
        """
        Obtiene las cantidades de adherentes de los reclamos creados en los últimos `dias` días.
        Si se especifica una clasificación, se filtran los reclamos por esa clasificación.
        """
        fecha_limite = datetime.utcnow() - timedelta(days=dias)
        query = self.repositorio_reclamos.session.query(ModeloReclamo).filter(
            ModeloReclamo.fecha_hora >= fecha_limite
        )
        if clasificacion:
            query = query.filter(ModeloReclamo.clasificacion == clasificacion)
        reclamos = query.all()
        return [r.cantidad_adherentes for r in reclamos if r.cantidad_adherentes is not None]
        
class ReportePDF:
    def __init__(self, generador:GeneradorReportes):
        self.generador = generador
        
    def generarPDF(self, ruta_salida='.data/reporte.pdf'):
        from reportlab.lib import colors

        c = canvas.Canvas(ruta_salida, pagesize=A4)
        ancho, alto = A4
        x = 2 * cm
        y = alto - 2 * cm
        salto = 1 * cm

        def salto_de_pagina():
            nonlocal y
            if y < 2.5 * cm:
                c.showPage()
                y = alto - 2 * cm
                c.setFont("Helvetica-Bold", 14)
                c.setFillColor(colors.darkblue)
                c.drawString(x, y, "Reporte de Reclamos (continuación)")
                c.setFillColor(colors.black)
                y -= salto

        # Título
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(colors.darkblue)
        c.drawCentredString(ancho / 2, y, "Reporte de Reclamos")
        c.setFillColor(colors.black)
        y -= 2 * salto

        # Total y promedio
        c.setFont("Helvetica", 12)
        c.drawString(x, y, f"Total de reclamos: {self.generador.cantidad_total_reclamos()}")
        y -= salto
        salto_de_pagina()

        c.drawString(x, y, f"Promedio de adherentes por reclamo: {self.generador.cantidad_promedio_adherentes():.2f}")
        y -= 2 * salto
        salto_de_pagina()

        def seccion(titulo):
            nonlocal y
            c.setFillColorRGB(0.9, 0.9, 0.9)
            c.rect(x - 0.2*cm, y - 0.3*cm, ancho - 4*cm, salto + 0.2*cm, fill=True, stroke=False)
            c.setFillColor(colors.black)
            c.setFont("Helvetica-Bold", 14)
            c.drawString(x, y, titulo)
            y -= salto
            salto_de_pagina()
            c.setFont("Helvetica", 11)

        # Por estado
        seccion("Cantidad de reclamos por estado:")
        for estado, cantidad in self.generador.cantidad_reclamos_por_estado().items():
            c.drawString(x + 0.5 * cm, y, f"• {estado}: {cantidad}")
            y -= salto
            salto_de_pagina()

        # Por clasificación
        seccion("Cantidad de reclamos por clasificación:")
        for clasificacion, cantidad in self.generador.cantidad_reclamos_por_clasificacion().items():
            c.drawString(x + 0.5 * cm, y, f"• {clasificacion}: {cantidad}")
            y -= salto
            salto_de_pagina()

        # Reclamos recientes
        seccion("Reclamos recientes (últimos 7 días):")
        recientes = self.generador.reclamos_recientes()
        c.setFont("Helvetica-Oblique", 10)
        for reclamo in recientes:
            texto = f"• ID {reclamo.id} - {reclamo.contenido or 'Sin título'} ({reclamo.estado or 'Sin estado'})"
            c.drawString(x + 0.5 * cm, y, texto)
            y -= salto
            salto_de_pagina()

        c.save()
        print(f"Reporte PDF generado en: {ruta_salida}")

from jinja2 import Environment, FileSystemLoader

class ReporteHTML:
    def __init__(self, generador_reportes):
        self.generador = generador_reportes

    def obtener_datos_reporte(self):
        return {
            "total": self.generador.cantidad_total_reclamos(),
            "promedio": f"{self.generador.cantidad_promedio_adherentes():.2f}",
            "reclamos_por_estado": self.generador.cantidad_reclamos_por_estado(),
            "reclamos_por_clasificacion": self.generador.cantidad_reclamos_por_clasificacion(),
            "reclamos_recientes": self.generador.reclamos_recientes(),
        }

    def exportar_html(self, nombre_archivo="reporte.html"):
        datos = self.obtener_datos_reporte()

        # Cargar el entorno de plantillas desde la carpeta templates/
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("reporte.html")

        # Renderizar el HTML con los datos
        html = template.render(**datos)

        # Guardar el resultado en un archivo
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(html)
        
        import webbrowser
        import os

        ruta_absoluta = os.path.abspath(nombre_archivo)
        webbrowser.open(f"file://{ruta_absoluta}")


if __name__ == '__main__':  # pragma: no cover
    repo_reclamos = RepositorioReclamosSQLAlchemy(session)
    generador = GeneradorReportes(repo_reclamos)
    print("Cantidad total de reclamos:", generador.cantidad_total_reclamos())

    # Reporte en PDF
    reporte_pdf = ReportePDF(generador)
    reporte_pdf.generarPDF("data/salida_reporte.pdf")
    
    reporte_html = ReporteHTML(generador)

    # Exportar el reporte HTML a archivo y abrirlo en navegador
    reporte_html.exportar_html("templates/reporte.html")

    # Obtener datos para testeo e imprimir en consola
    datos = reporte_html.obtener_datos_reporte()
    import pprint
    pprint.pprint(datos)
    
    for reclamo in datos["reclamos_recientes"]:
        print(f"ID {reclamo.id} - {reclamo.contenido or 'Sin título'} - Estado: {reclamo.estado or 'Sin estado'}")


