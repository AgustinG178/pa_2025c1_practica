import random
frases_usadas = []

def leer_frases_de_peliculas(nombre_archivo):

    frases = []
    with open("proyecto_1/data/frases_de_peliculas.txt", 'r') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if ';' in linea:  
                frases.append(linea.split(';'))
    return frases

def seleccionar_frase(frases):
    while len(frases_usadas)<len(frases):
        sublista_random = random.choice(frases)
        if sublista_random not in frases_usadas:
            frase = sublista_random[0]
                
            pelicula = sublista_random[1]

            frases_usadas.append(sublista_random)
            
            return frase, pelicula, frases_usadas
        else:
            return seleccionar_frase(frases)