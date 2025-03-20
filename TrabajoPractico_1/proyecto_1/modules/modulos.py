import random
from flask import render_template
frases_usadas = []
peli_random = []
peliculas = []

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
        sublista_random = random.choice(frases)
        if sublista_random not in frases_usadas:
            frase = sublista_random[0]
            for _ in range (3):
                sublista_random2 = random.choice(frases)
                randomizador = sublista_random2[1] 
                peliculas.append(randomizador)
            frases_usadas.append(sublista_random)
            return frase, peliculas, frases_usadas
        else:
            return seleccionar_peli(frases)

def procesar_respuesta(respuesta):
    return "Respuesta correcta" if respuesta == "la correcta" else "Respuesta incorrecta"
def dif_dificil(opciones):
        try:
            opciones.append(seleccionar_peli(peli_random)[0])
            opciones.append(seleccionar_peli(peli_random)[1])
            opciones.append(seleccionar_peli(peli_random)[2]) 
            return opciones
        except TypeError:
            return render_template("Inicio.html")