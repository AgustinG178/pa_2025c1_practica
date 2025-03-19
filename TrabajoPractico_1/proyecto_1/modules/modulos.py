import random
frases_usadas = []

def leer_frases_de_peliculas(nombre_archivo):

    frases = []
    with open("data/frases_de_peliculas.txt", 'r', encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if ';' in linea:  
                frases.append(linea.split(';'))
    return frases

def seleccionar_peli(frases):
    while len(frases_usadas)<len(frases):
        sublista_random = random.choice(frases[1])
        if sublista_random not in frases_usadas:
            frase = sublista_random[0]
                
            pelicula = sublista_random[1]

            frases_usadas.append(sublista_random)
            
            return frase, pelicula, frases_usadas
        else:
            return seleccionar_peli(frases)
        
def procesar_respuesta(respuesta):
    return "Respuesta correcta" if respuesta == "la correcta" else "Respuesta incorrecta"