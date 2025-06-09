from modules.reportes import GeneradorReportes
import matplotlib.pyplot as plt
import os

class GraficadoraTorta:
    def graficar(self, datos: dict, nombre_archivo='torta_estado.png', ruta = "static/graficos"):
        etiquetas = list(datos.keys())
        valores = list(datos.values())

        plt.figure(figsize=(6, 6))
        plt.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=140)
        plt.title('Distribución de Reclamos por Estado')
        plt.axis('equal')

        ruta = os.path.join('static', 'graficos', nombre_archivo)
        plt.savefig(ruta)
        plt.close()

        return f'graficos/{nombre_archivo}'


class GraficadoraHistograma:
    def graficar(self, datos: list, titulo: str, xlabel: str, ylabel: str, nombre_archivo='histograma_estado.png'):
        if not datos:
            print(f"[!] No hay datos para graficar: {titulo}")
            return

        plt.figure(figsize=(10, 6))
        plt.hist(datos, bins=10, color='salmon', edgecolor='black')
        plt.title(titulo)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        
        ruta = os.path.join('static', 'graficos', nombre_archivo)
        plt.savefig(ruta)
        plt.close()
        
        return f'graficos/{nombre_archivo}'

    def graficar_por_clasificacion(self, datos_por_clasificacion: dict, titulo: str, xlabel: str, ylabel: str):
        if not datos_por_clasificacion:
            print(f"[!] No hay datos para graficar: {titulo}")
            return

        plt.figure(figsize=(10, 6))

        for clasificacion, datos in datos_por_clasificacion.items():
            if datos:
                plt.hist(datos, bins=10, alpha=0.5, label=clasificacion, edgecolor='black')

        plt.title(titulo)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.tight_layout()
        plt.show()
        
class Graficadora:
    def __init__(self, generador_reportes, graficadora_torta, graficadora_histograma):
        self.generador_reportes = generador_reportes
        self.graficadora_torta = graficadora_torta
        self.graficadora_histograma = graficadora_histograma

    def graficar_todo(self, clasificacion=None):
        if clasificacion:
            datos_estado = self.generador_reportes.cantidad_reclamos_por_estado_filtrado(clasificacion)
            reclamos = self.generador_reportes.reclamos_recientes_filtrado(clasificacion, 365)
        else:
            datos_estado = self.generador_reportes.cantidad_reclamos_por_estado()
            reclamos = self.generador_reportes.reclamos_recientes(365)

        self.graficadora_torta.graficar(datos_estado, "Distribución de Reclamos por Estado")

        datos_por_clasificacion = {}
        for reclamo in reclamos:
            if reclamo.cantidad_adherentes is not None:
                clave = reclamo.clasificacion or "Sin Clasificar"
                datos_por_clasificacion.setdefault(clave, []).append(reclamo.cantidad_adherentes)

        self.graficadora_histograma.graficar_por_clasificacion(
            datos_por_clasificacion,
            "Distribución de Adherentes por Clasificación",
            "Cantidad de Adherentes",
            "Frecuencia"
        )

        
if __name__ == "__main__":
    from modules.config import crear_engine
    from repositorio import RepositorioReclamosSQLAlchemy
    from reportes import GeneradorReportes

    engine, Session = crear_engine()
    session = Session()

    graficadora_torta = GraficadoraTorta()
    graficadora_histograma = GraficadoraHistograma()

    repositorio = RepositorioReclamosSQLAlchemy(session)
    generador = GeneradorReportes(repositorio)
    graficadora = Graficadora(generador, graficadora_torta, graficadora_histograma)

    graficadora.graficar_todo()


