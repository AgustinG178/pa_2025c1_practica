import random
from copy import deepcopy
import os


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
    file_path = "data/frases_de_peliculas.txt"
    
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


if __name__ == "__main__":

    # print(juego_opciones(frases,7))
    # Ejemplo de uso
    
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







