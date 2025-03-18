import random
frases_usadas = []

def leer_frases_de_peliculas(nombre_archivo):

    frases = []
    with open("data/frases_de_peliculas.txt", 'r') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if ';' in linea:  
                frases.append(linea.split(';'))
    return frases

def seleccionar_frase(frases):

    sublista_random = random.choice(frases)
    if sublista_random not in frases_usadas:

        frase = sublista_random[0]
        
        pelicula = sublista_random[1]
        
        return frase, pelicula
    else:
        seleccionar_frase(frases)