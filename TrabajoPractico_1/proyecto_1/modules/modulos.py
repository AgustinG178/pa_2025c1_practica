import random

nombre_archivo = "frases_de_peliculas.txt"

def leer_frases_de_peliculas(nombre_archivo):

    frases = []
    with open("data/frases_de_peliculas.txt", 'r', encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if ';' in linea:  
                frases.append(linea.split(';'))
    return frases      

frases = leer_frases_de_peliculas(nombre_archivo)      

listaop = []

def seleccionar_peli(frases, intentos):
    frases_usadas = []
    peli_i = []
    peli_c = []
    frase = []
    for _ in range (intentos):
        sublista_random = random.choice(frases)
        if sublista_random not in frases_usadas:
            frase.append(sublista_random[0])
            peli_c = sublista_random[1]
            
            peli_i.append(random.choice(frases[1]))
            peli_i.append(random.choice(frases[1]))
        else:
            return seleccionar_peli
        print(peli_i)
        print(type(peli_i))

        dic = { peli_c : "correcto", 
                peli_i[0] : "incorrecto", 
                peli_i[1] : "incorrecto" }

    return frase , dic 
    
def procesar_respuesta(respuesta):
    return "Respuesta correcta" if respuesta == "la correcta" else "Respuesta incorrecta"
