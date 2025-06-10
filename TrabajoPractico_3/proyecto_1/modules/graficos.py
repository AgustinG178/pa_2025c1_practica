from modules.reportes import GeneradorReportes
import matplotlib.pyplot as plt
import os

class GraficadoraTorta:
    def graficar(self, datos: dict, nombre_archivo:str, subcarpeta:str):
        """
        Genera un grafico de torta apareciendo los datos proporcionados, reclamos por ejemplo.
        """
        etiquetas = list(datos.keys())
        valores = list(datos.values())

        plt.figure(figsize=(6, 6))
        plt.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=140)
        plt.title('Distribución de Reclamos por Estado')
        plt.axis('equal')

        ruta_carpeta = os.path.join('static', 'graficos', subcarpeta)
        os.makedirs(ruta_carpeta, exist_ok=True)  # Esto crea la carpeta si no existe

        ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
        plt.savefig(ruta_archivo)
        plt.close()

        return f'graficos/{subcarpeta}/{nombre_archivo}'

class GraficadoraHistograma:
    def graficar(self, datos: list, titulo: str, xlabel: str, ylabel: str, nombre_archivo:str, subcarpeta:str):

        """
        Genera un histograma a partir de los datos proporcionados, reclamos por ejemplo
        """
        if not datos:
            print(f"[!] No hay datos para graficar: {titulo}")
            return

        plt.figure(figsize=(10, 6))
        plt.hist(datos, bins=10, color='salmon', edgecolor='black')
        plt.title(titulo)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()

        ruta_carpeta = os.path.join('static', 'graficos', subcarpeta)
        os.makedirs(ruta_carpeta, exist_ok=True)

        ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
        plt.savefig(ruta_archivo)
        plt.close()

        return f'graficos/{subcarpeta}/{nombre_archivo}'


    def graficar_por_clasificacion(self, datos_por_clasificacion: dict, titulo: str, xlabel: str, ylabel: str):
        """
        Se genera un histograma por clasificación de reclamos
        """
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
    """
    Clase generado de graficos, encargada de generar gráficos de torta y histogramas, emplea las clases GraficadoraTorta y GraficadoraHistograma.
    """
    def __init__(self, generador_reportes:GeneradorReportes, graficadora_torta:GraficadoraTorta, graficadora_histograma:GraficadoraHistograma):
        self.generador_reportes = generador_reportes
        self.graficadora_torta = graficadora_torta
        self.graficadora_histograma = graficadora_histograma

    def graficar_todo(self, clasificacion=None, es_secretario_tecnico=False):
        rutas = {}

        if es_secretario_tecnico:
            # Carpeta para secretario técnico
            subcarpeta = 'secretario_tecnico'

            # Torta general de estados (todos los reclamos)
            datos_estado = self.generador_reportes.cantidad_reclamos_por_estado()
            rutas["torta"] = self.graficadora_torta.graficar(
                datos_estado,
                nombre_archivo="torta_estado_general.png",
                subcarpeta=subcarpeta
            )

            # Reclamos recientes sin filtro
            reclamos = self.generador_reportes.reclamos_recientes(365)

        else:
            # Carpeta según clasificación (soporte_informatico, secretario_tecnico, maestranza)
            subcarpeta = clasificacion.replace(" ", "_")

            datos_estado = self.generador_reportes.cantidad_reclamos_por_estado_filtrado(clasificacion)
            rutas["torta"] = self.graficadora_torta.graficar(
                datos_estado,
                nombre_archivo=f"torta_estado_{subcarpeta}.png",
                subcarpeta=subcarpeta
            )

            reclamos = self.generador_reportes.reclamos_recientes_filtrado(clasificacion, 365)

        datos_por_clasificacion = {}
        for reclamo in reclamos:
            if reclamo.cantidad_adherentes is not None:
                clave = reclamo.clasificacion or "Sin Clasificar"
                datos_por_clasificacion.setdefault(clave, []).append(reclamo.cantidad_adherentes)

        nombre_histograma = "histograma_adherentes.png" if es_secretario_tecnico else f"histograma_{subcarpeta}.png"
        rutas["histograma"] = self.graficadora_histograma.graficar(
            datos=[adherentes for adherentes_list in datos_por_clasificacion.values() for adherentes in adherentes_list],
            titulo="Distribución de Adherentes",
            xlabel="Cantidad de Adherentes",
            ylabel="Frecuencia",
            nombre_archivo=nombre_histograma,
            subcarpeta=subcarpeta
        )

        return rutas
    
    def graficar_torta_por_rol(self, rol, nombre_archivo, subcarpeta):

        """
        Se genera un grafico de torta para un rol específico, por ejemplo, soporte informático o un jefe de departamento.
        """
        datos = self.generador_reportes.obtener_datos_para_torta(rol)
        self.graficadora_torta.graficar(datos, nombre_archivo, subcarpeta)
        
    def graficar_histograma_por_rol(self, rol, nombre_archivo, subcarpeta):

        """
        Se genera un histograma para un rol específico, por ejemplo, soporte informático o un jefe de departamento.
        """
        datos = self.generador_reportes.obtener_datos_para_histograma(rol)

        self.graficadora_histograma.graficar(
        datos=datos,
        titulo="Distribución de reclamos",
        xlabel="Cantidad",
        ylabel="Frecuencia",
        nombre_archivo=nombre_archivo,
        subcarpeta=subcarpeta
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

    # Roles por los que queremos generar gráficos
    roles = {
        '2': 'soporte_informatico',
        '3': 'secretario_tecnico',
        '4': 'maestranza'
    }

    for rol, nombre_directorio in roles.items():
        print(f"Generando gráficos para rol {rol} ({nombre_directorio})...")
        graficadora.graficar_torta_por_rol(rol, nombre_directorio, 'tortas')
        graficadora.graficar_histograma_por_rol(rol, nombre_directorio, 'histogramas')

    print("Todos los gráficos fueron generados exitosamente.")



