import random
from copy import deepcopy
import matplotlib
matplotlib.use('Agg')  # Configura un backend no interactivo
import matplotlib.pyplot as plt
import os
from collections import defaultdict

def leer_frases_de_peliculas(nombre_archivo):
    """
    Lee las frases y películas desde un archivo y las devuelve en una lista.
    Args:
        nombre_archivo (str): Ruta al archivo que contiene las frases y películas.
    Returns:
        list: Lista de frases y sus respectivas películas.
    """
    frases = []
    with open("data/frases_de_peliculas.txt", 'r', encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if ';' in linea:
                frases.append(linea.split(';'))
    return frases

def opciones_pelis(frases_pelis, lista_peliculas):
    """
    Genera una lista de tres opciones de películas únicas para una ronda.
    Args:
        frases_pelis (list): Lista de frases y películas disponibles.
        lista_peliculas (list): Lista de películas ya seleccionadas.
    Returns:
        tuple: Lista de películas únicas y la lista de frases actualizada.
    """
    while len(lista_peliculas) < 3:
        opcion_ronda = random.choice(frases_pelis)
        pelicula = opcion_ronda[1].title()
        if pelicula not in lista_peliculas:
            lista_peliculas.append(pelicula)
            frases_pelis.remove(opcion_ronda)
    return lista_peliculas, frases_pelis

def listar_peliculas(file_path):
    """
    Lee el archivo frases_de_peliculas.txt, extrae las películas, elimina duplicados y las ordena alfabéticamente.
    
    Args:
        file_path (str): Ruta al archivo frases_de_peliculas.txt.
    
    Returns:
        list: Lista de películas únicas ordenadas alfabéticamente.
        
    ¿porque file_path y no la ruta directamente?, Si la ruta del archivo cambia en el futuro, solo necesitas actualizar la variable que contiene la ruta en un único lugar, en lugar de buscar y reemplazar todas las instancias de la ruta en el código.
    """
    peliculas = set()
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            if line.strip() and ';' in line:
                try:
                    pelicula = line.split(';')[1].strip()
                    peliculas.add(pelicula)
                except IndexError:
                    print(f"Línea con formato incorrecto: {line.strip()}")
                    continue
    return sorted(peliculas)

def juego_opciones(frases, intentos):
    """
    Genera las rondas del juego con frases y opciones de películas.
    Args:
        frases (list): Lista de frases y películas.
        intentos (int): Número de rondas a generar.
    Returns:
        list: Lista de rondas con frases y opciones de películas.
    """
    frases_0 = deepcopy(frases)
    juego = []
    for _ in range(intentos):
        opcion_correcta = []
        pelis = []
        ronda = []
        sublista_random = random.choice(frases_0)
        frases_0.remove(sublista_random)
        opcion_correcta.append([sublista_random[0], sublista_random[1].title()])
        ronda.append(opcion_correcta)
        pelis.append(sublista_random[1].title())
        opciones_pelis_juego, frases_0 = opciones_pelis(frases_0, pelis)
        random.shuffle(opciones_pelis_juego)
        ronda.append(opciones_pelis_juego)
        juego.append(ronda)
    return juego

def opcion_correcta(pelicula, pelicula_correcta):
    """
    Verifica si la opción seleccionada por el usuario es correcta.
    Args:
        pelicula (str): Película seleccionada por el usuario.
        pelicula_correcta (str): Película correcta.
    Returns:
        int: 1 si es correcta, 0 si es incorrecta.
    """
    return 1 if pelicula == pelicula_correcta else 0

def escribir_resultados_archivo(usuario, resultado, intentos, fecha):
    """
    Escribe los resultados de una partida en el archivo de resultados.
    Args:
        usuario (str): Nombre del usuario.
        resultado (int): Número de aciertos.
        intentos (int): Número total de intentos.
        fecha (str): Fecha de la partida.
    """
    os.makedirs("data", exist_ok=True)
    with open("data/resultados.txt", 'a', encoding="utf-8") as historial:
        historial.write(f"Usuario:{usuario} / Resultado: {resultado}/{intentos} / Fecha: {fecha}\n")

def leer_archivo_resultados():
    """
    Lee el archivo de resultados y devuelve los datos como una lista de líneas.
    Returns:
        list: Lista de resultados de las partidas.
    """
    with open("data/resultados.txt", 'r', encoding="utf-8") as historial:
        return historial.read().splitlines()

def graficar_intentos_vs_aciertos(file_path, output_folder):
    """
    Genera un gráfico de torta con los aciertos y errores totales.
    Args:
        file_path (str): Ruta al archivo de resultados.
        output_folder (str): Carpeta donde se guardará el gráfico.
    """
    aciertos_totales = 0
    intentos_totales = 0
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() and "Usuario:" in line and "Resultado:" in line:
                parts = line.strip().split(" / ")
                try:
                    resultado = parts[1].split(":")[1]
                    correctos, total = map(int, resultado.split("/"))
                    aciertos_totales += correctos
                    intentos_totales += total
                except (IndexError, ValueError):
                    print(f"Línea con formato incorrecto: {line.strip()}")
                    continue
    labels = ['Aciertos', 'Errores']
    sizes = [aciertos_totales, intentos_totales - aciertos_totales]
    colors = ['skyblue', 'lightcoral']
    explode = (0.1, 0)
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, explode=explode)
    plt.title('Resultados Generales')
    plt.axis('equal')
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "grafico_torta_general.png")
    plt.savefig(output_path)
    plt.close()

def graficar_aciertos_vs_desaciertos_por_fecha(file_path, output_folder):
    """
    Genera un gráfico con dos curvas: una para los aciertos y otra para los desaciertos,
    en función de las fechas de juego para todos los usuarios.
    Args:
        file_path (str): Ruta al archivo de resultados.
        output_folder (str): Carpeta donde se guardará el gráfico.
    """
    fechas = defaultdict(lambda: {"aciertos": 0, "desaciertos": 0})
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            if line.strip() and "Usuario:" in line and "Resultado:" in line:
                parts = line.strip().split(" / ")
                try:
                    fecha = parts[2].split(":")[1].strip()
                    resultado = parts[1].split(":")[1]
                    aciertos, total = map(int, resultado.split("/"))
                    desaciertos = total - aciertos
                    fechas[fecha]["aciertos"] += aciertos
                    fechas[fecha]["desaciertos"] += desaciertos
                except (IndexError, ValueError):
                    print(f"Línea con formato incorrecto: {line.strip()}")
                    continue
    fechas_ordenadas = sorted(fechas.items())
    fechas_labels = [fecha for fecha, _ in fechas_ordenadas]
    aciertos_totales = [data["aciertos"] for _, data in fechas_ordenadas]
    desaciertos_totales = [data["desaciertos"] for _, data in fechas_ordenadas]
    plt.figure(figsize=(10, 6))
    plt.plot(fechas_labels, aciertos_totales, label="Aciertos", marker="o", color="green")
    plt.plot(fechas_labels, desaciertos_totales, label="Desaciertos", marker="o", color="red")
    plt.xlabel("Fechas")
    plt.ylabel("Cantidad")
    plt.title("Aciertos vs Desaciertos por Fecha")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "grafico_curvas_aciertos_desaciertos.png")
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":

    # print(juego_opciones(frases,7))
    # Ejemplo de uso
    file_path = "data/resultados.txt"
    folder = "static/graficos"
    graficar_intentos_vs_aciertos(file_path, folder)
    graficar_aciertos_vs_desaciertos_por_fecha(file_path, folder)
    
    """
    frases_prueba = deepcopy(frases)
    lista_aletoria = random.choice(frases_prueba)
    frases_prueba.remove(lista_aletoria)
    
    if lista_aletoria not in frases_prueba:
        print("El elemento fue removido correctamente")
    else:
        print("El elemento no fue removido")
    #for ronda_0 in juego_opciones(frases,4):
        #print(f"Frase: {ronda_0[0][0][0]}")
        #print(f"Opciones: {ronda_0[1]}")  
    """







