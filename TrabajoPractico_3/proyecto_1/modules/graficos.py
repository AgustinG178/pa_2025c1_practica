from modules.reportes import GeneradorReportes
from wordcloud import WordCloud
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
        
        
class GraficadoraNubePalabras:
    def generar_nube_palabras(self, reclamos, nombre_archivo="nube_palabras.png", subcarpeta="nubes"):
        """
        Genera una nube de palabras a partir de los contenidos de los reclamos.
        
        :param reclamos: Lista de objetos Reclamo o strings con los contenidos de los reclamos.
        :param nombre_archivo: Nombre del archivo de salida para la nube de palabras.
        :param subcarpeta: Subcarpeta donde se guardará la imagen.
        """
        # Concatenar todos los contenidos de los reclamos en un solo texto
        texto = " ".join([reclamo.contenido for reclamo in reclamos if reclamo.contenido])

        # Generar la nube de palabras
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color="white",
            colormap="viridis",
            max_words=100
        ).generate(texto)

        # Crear la carpeta de salida si no existe
        ruta_carpeta = os.path.join("static", "graficos", subcarpeta)
        os.makedirs(ruta_carpeta, exist_ok=True)

        # Guardar la imagen de la nube de palabras
        ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
        wordcloud.to_file(ruta_archivo)

        # Mostrar la nube de palabras
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title("Nube de Palabras - Reclamos")
        plt.tight_layout()
        
        ruta_carpeta = os.path.join('static', 'graficos', subcarpeta)
        os.makedirs(ruta_carpeta, exist_ok=True)

        ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
        plt.savefig(ruta_archivo)
        plt.close()

        return f"graficos/{subcarpeta}/{nombre_archivo}"

class Graficadora:
    """
    Clase generado de graficos, encargada de generar gráficos de torta y histogramas, emplea las clases GraficadoraTorta y GraficadoraHistograma.
    """
    def __init__(self, generador_reportes:GeneradorReportes, graficadora_torta:GraficadoraTorta, graficadora_histograma:GraficadoraHistograma, graficadora_nube:GraficadoraNubePalabras):
        self.generador_reportes = generador_reportes
        self.graficadora_torta = graficadora_torta
        self.graficadora_histograma = graficadora_histograma
        self.graficadora_nube = graficadora_nube

    def graficar_todo(self, reclamos, clasificacion=None, es_secretario_tecnico=False):
        rutas = {}

        if es_secretario_tecnico:
            subcarpeta = 'secretario_tecnico'
            datos_estado = self.generador_reportes.cantidad_reclamos_por_estado()
            rutas["torta"] = self.graficadora_torta.graficar(
                datos_estado, "torta_estado_general.png", subcarpeta
            )
            # SOLO usar reclamos que vienen como parámetro
        else:
            subcarpeta = clasificacion.replace(" ", "_")
            datos_estado = self.generador_reportes.cantidad_reclamos_por_estado_filtrado(clasificacion)
            rutas["torta"] = self.graficadora_torta.graficar(
                datos_estado, f"torta_estado_{subcarpeta}.png", subcarpeta
            )
            # SOLO usar reclamos que vienen como parámetro

        # Asegurarse que reclamos no esté vacío
        if not reclamos:
            print("[!] No hay reclamos para generar gráficos.")
            return rutas

        # Histograma
        datos_por_clasificacion = {}
        for reclamo in reclamos:
            if reclamo.cantidad_adherentes is not None:
                clave = reclamo.clasificacion or "Sin Clasificar"
                datos_por_clasificacion.setdefault(clave, []).append(reclamo.cantidad_adherentes)

        nombre_histograma = "histograma_adherentes.png" if es_secretario_tecnico else f"histograma_{subcarpeta}.png"
        rutas["histograma"] = self.graficadora_histograma.graficar(
            datos=[v for sublist in datos_por_clasificacion.values() for v in sublist],
            titulo="Distribución de Adherentes",
            xlabel="Cantidad de Adherentes",
            ylabel="Frecuencia",
            nombre_archivo=nombre_histograma,
            subcarpeta=subcarpeta
        )

        # Nube de palabras
        ruta_nube = self.graficadora_nube.generar_nube_palabras(
            reclamos, nombre_archivo=f"nube_palabras_{subcarpeta}.png", subcarpeta=subcarpeta
        )
        if ruta_nube:
            rutas["nube_palabras"] = ruta_nube

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
        
    def graficar_nube_palabras_por_rol(self, reclamos, nombre_archivo="nube_palabras.png", subcarpeta="nubes"):
        """
        Genera una nube de palabras a partir de los contenidos de los reclamos.
        
        :param reclamos: Lista de objetos Reclamo o strings con los contenidos de los reclamos.
        :param nombre_archivo: Nombre del archivo de salida para la nube de palabras.
        :param subcarpeta: Subcarpeta donde se guardará la imagen.
        """
        graficadora_nube = GraficadoraNubePalabras()
        graficadora_nube.generar_nube_palabras(reclamos, nombre_archivo, subcarpeta)
        
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

    # Obtener todos los reclamos
    reclamos = repositorio.obtener_todos_los_registros(usuario_id=2)

    # Crear una instancia de la graficadora
    graficadora_nube = GraficadoraNubePalabras()

    # Generar la nube de palabras
    ruta_nube = graficadora_nube.generar_nube_palabras(reclamos)
    print(f"Nube de palabras generada en: {ruta_nube}")



