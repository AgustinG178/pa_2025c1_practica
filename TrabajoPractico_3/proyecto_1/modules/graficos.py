from modules.reportes import GeneradorReportes
from wordcloud import WordCloud, STOPWORDS
from collections import Counter
import os
import matplotlib.pyplot as plt
import matplotlib
from stop_words import get_stop_words

matplotlib.use('Agg')

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
    def graficar(self, datos, titulo, xlabel, ylabel, nombre_archivo="histograma.png", subcarpeta="histogramas"):
        """
        Genera un histograma a partir de los datos proporcionados.

        :param datos: Lista de valores numéricos para el histograma.
        :param titulo: Título del gráfico.
        :param xlabel: Etiqueta del eje X.
        :param ylabel: Etiqueta del eje Y.
        :param nombre_archivo: Nombre del archivo de salida para el histograma.
        :param subcarpeta: Subcarpeta donde se guardará la imagen.
        """
        # Verificar si hay datos
        if not datos:
            print("[!] No hay datos para generar el histograma.")
            return None

        # Crear el histograma
        plt.figure(figsize=(10, 6))
        plt.hist(datos, bins=10, color="#00509e", edgecolor="black", alpha=0.7)
        plt.title(titulo)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        # Crear la carpeta de salida si no existe
        ruta_carpeta = os.path.join("static", "graficos", subcarpeta)
        os.makedirs(ruta_carpeta, exist_ok=True)

        # Guardar el histograma
        ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
        plt.savefig(ruta_archivo)
        plt.close()

        return f"graficos/{subcarpeta}/{nombre_archivo}"


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

        """
        # Concatenar todos los contenidos de los reclamos en un solo texto
        texto = " ".join([reclamo.contenido for reclamo in reclamos if reclamo.contenido])

        # Verificar si el texto está vacío
        if not texto.strip():
            print("[!] No hay palabras para generar la nube de palabras.")
            return None

        ruta_stopwords = "data/stopwords.txt"
        
        with open(ruta_stopwords, encoding="utf-8") as f:
            stopwords_personalizadas = {line.strip() for line in f if line.strip()}


        # Filtrar palabras vacías (stopwords) y caracteres no deseados del modulo stop-words
        stopwords_libreria = set(get_stop_words('spanish'))
        stopwords = set(STOPWORDS)
        stopwords.update(stopwords_libreria)
        palabras = texto.lower().split()
        palabras_filtradas = [
            palabra.strip(".,!?()[]{}\"'") for palabra in palabras if palabra not in stopwords and len(palabra) > 2
        ]
        # Agregar stopwords propias 
        ruta_stopwords = "data/stopwords.txt"
        if os.path.exists(ruta_stopwords):
            with open(ruta_stopwords, encoding="utf-8") as f:
                stopwords_personalizadas = {line.strip() for line in f if line.strip()}
            stopwords.update(stopwords_personalizadas)

        palabras = texto.lower().split()
        palabras_filtradas = [
            palabra.strip(".,!?()[]{}\"'") for palabra in palabras if palabra not in stopwords and len(palabra) > 2
        ]
        contador = Counter(palabras_filtradas)
        palabras_frecuentes = dict(contador.most_common(15))
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color="white",
            colormap="viridis",
            max_words=15
        ).generate_from_frequencies(palabras_frecuentes)
        ruta_carpeta = os.path.join("static", "graficos", subcarpeta)
        os.makedirs(ruta_carpeta, exist_ok=True)
        ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
        wordcloud.to_file(ruta_archivo)

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
        return self.graficadora_torta.graficar(datos, nombre_archivo, subcarpeta)
        
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
        
    def clasificacion_por_rol(self, rol):
        """
        Devuelve la clasificación correspondiente a un rol.
        """
        clasificaciones = {
            "2": "secretaría técnica",
            "3": "soporte informático",
            "4": "maestranza"
        }
        return clasificaciones.get(rol)
        
if __name__ == "__main__":
    from modules.config import crear_engine
    from repositorio import RepositorioReclamosSQLAlchemy
    from reportes import GeneradorReportes

    engine, Session = crear_engine()
    session = Session()

    graficadora_torta = GraficadoraTorta()
    graficadora_histograma = GraficadoraHistograma()
    graficadora_nube = GraficadoraNubePalabras()

    repositorio = RepositorioReclamosSQLAlchemy(session)
    generador = GeneradorReportes(repositorio)
    graficadora = Graficadora(generador, graficadora_torta, graficadora_histograma, graficadora_nube)

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

    reclamos = repositorio.obtener_todos_los_registros(usuario_id=2)
    if reclamos:
        graficadora_nube = GraficadoraNubePalabras()
        ruta_nube = graficadora_nube.generar_nube_palabras(reclamos)
        if ruta_nube:
            print(f"Nube de palabras generada en: {ruta_nube}")
    else:
        print("[!] No se encontraron reclamos para el usuario_id=2. No se generó nube de palabras.")
