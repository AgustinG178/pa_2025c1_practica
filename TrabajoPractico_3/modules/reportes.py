class Graficadora:
    def generar_grafico(self, datos, tipo):
        # Lógica para graficar
        pass

class ReporteHTML(IReporte):
    def __init__(self, graficadora=None):
        self.graficadora = graficadora

    def generarHTML(self, datos):
        if self.graficadora:
            grafico = self.graficadora.generar_grafico(datos, tipo="barras")
        # Lógica para generar HTML
        pass

class ReportePDF(IReporte):
    def __init__(self, graficadora=None):
        self.graficadora = graficadora

    def generarPDF(self, datos):
        if self.graficadora:
            grafico = self.graficadora.generar_grafico(datos, tipo="pie")
        # Lógica para generar PDF
        pass