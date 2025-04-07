import random
from copy import deepcopy
import matplotlib.pyplot as plt

# Constants
STATIC_GRAPH_PATH = "static/grafico_torta.png"


nombre_archivo = "frases_de_peliculas.txt"

def leer_frases_de_peliculas(nombre_archivo):
    '''
    Carga las frases desde un archivo a una lista
    '''


def leer_frases_de_peliculas(nombre_archivo):
    
    frases = []
    with open("data/frases_de_peliculas.txt", 'r', encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if ';' in linea:  
                frases.append(linea.split(';'))
    return frases      

def opciones_pelis (frases_pelis,lista_peliculas):
    while len(lista_peliculas) < 3: 
        opcion_ronda =random.choice(frases_pelis)
        pelicula = opcion_ronda[1].title()    
    #La función asegura que por ronda no haya repeticiones en las opciones de películas, ya que cada película tiene varias frases
        if pelicula not in lista_peliculas: 
            lista_peliculas.append(pelicula)
            frases_pelis.remove(opcion_ronda)

    return lista_peliculas, frases_pelis

                
   



def juego_opciones(frases, intentos):
    frases_0 = deepcopy(frases) #copiamos la lista original, de esta manera cada vez que se llame a la funcion juego_opciones, siempre se podrá jugar
                           #deepcopy() crea una nueva lista con dirección de memoria diferente 
    
    juego = [] #[[[opcion_correcta],[peliculas]]] opcion correcta es una lista, en el indice 0 se ubica la frase correcta y en el 1 la pelicula que le corresponde
    #peliculas es una lista que incluirá 3 peliculas, una justamentes es la que le corresponde a la frase.
    
    for _ in range (intentos):

        #definimos las variables que incluirán a la ronda
        opcion_correcta = []
        pelis=[]
        ronda =[] 

        sublista_random = random.choice(frases_0)
        frases_0.remove(sublista_random)
        
        opcion_correcta.append([sublista_random[0],sublista_random[1].title()])
        ronda.append(opcion_correcta)

        #añadimos la opcion correcta
        pelis.append(sublista_random[1].title()) 
        
        
        #creamos el total de opciones a mostrar y devolvemos la nueva lista de frases_0 con cambios
        opciones_pelis_juego,frases_0 = opciones_pelis(frases_0,pelis)[0],opciones_pelis(frases_0,pelis)[1]

              

        random.shuffle(opciones_pelis_juego)
        ronda.append(opciones_pelis_juego) #ronda interpretacion: ronda[0] = opcion correcta, ronda[1] = lista de películas a usar en la ronda
        juego.append(ronda)
        
    #juego[i] = ronda, entonces juego[i][0] = opcion correcta (lista: frase,peli) y juego[i][1] =  peliculas a mostrar
    return juego

def opcion_correcta(pelicula,pelicula_correcta):
    if pelicula == pelicula_correcta:
        return 1
    else:
        return 0
   
def escribir_resultados_archivo(usuario,resultado,intentos,fecha): #Escribimos en un txt los resultados de un usuario

    with open("data/frases_de_peliculas.txt", 'a', encoding="utf-8") as historial:
        
        historial.write(f"Usuario:{usuario} / Resultado: Acietos:{resultado}/ Rondas:{intentos} / Fecha: {fecha}\n")
        
        

def leer_archivo_resultados ():
   
    with open("TrabajoPractico_1/proyecto_1/data/resultados.txt", 'r', encoding="utf-8") as historial:
   
        juego_data = historial.read().splitlines()
   
        return juego_data

import matplotlib.pyplot as plt
import os

def graficar_intentos_vs_aciertos(file_path, output_folder):
    """
    Grafica un gráfico de torta general con los aciertos y errores totales
    de todos los usuarios combinados y guarda el gráfico en una carpeta.
    """
    aciertos_totales = 0
    intentos_totales = 0

    # Leer el archivo y calcular los totales
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

    # Crear el gráfico de torta
    labels = ['Aciertos', 'Errores']
    sizes = [aciertos_totales, intentos_totales - aciertos_totales]
    colors = ['skyblue', 'lightcoral']
    explode = (0.1, 0)  # Resaltar la porción de aciertos

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, explode=explode)
    plt.title('Resultados Generales')
    plt.axis('equal')  # Asegurar que el gráfico sea un círculo

    # Crear la carpeta si no existe
    os.makedirs(output_folder, exist_ok=True)

    # Guardar el gráfico en la carpeta
    output_path = os.path.join(output_folder, "grafico_torta_general.png")
    plt.savefig(output_path)
    plt.close()  # Cerrar el gráfico para liberar memoria

    print(f"Gráfico guardado en: {output_path}")

# Ejemplo de uso


if __name__ == "__main__":

    # print(juego_opciones(frases,7))
    
    # Ejemplo de uso
    file_path = "data/resultados.txt"
    folder = "static/graficos"
    graficar_intentos_vs_aciertos(file_path, folder)
    

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

    

    
    
  

