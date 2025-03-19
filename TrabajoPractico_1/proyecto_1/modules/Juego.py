from modules.modulos import leer_frases_de_peliculas, seleccionar_peli
import random
from flask import render_template


frases_usadas = []

nombre_archivo = "frases_de_peliculas.txt"

frases = leer_frases_de_peliculas(nombre_archivo)

frase, pelicula, frases_usadas = seleccionar_peli(frases) 

#podriamos meter esta funcion en un for de 3 ciclos cada vez que se seleccione o una dificultad o una respuesta 
#asi se seleccionan 3 películas constantemente

"""juego principal"""

frases = leer_frases_de_peliculas(nombre_archivo)
frase = random.choice(frases)
opciones=[]
for i in range(2):
    peli_random = [random.choice(frases)[1]] 

def dif_dificil():

    for i in range(3): 
        try:
            opciones.append(seleccionar_peli(peli_random)[0])
            opciones.append(seleccionar_peli(peli_random)[1])
            opciones.append(seleccionar_peli(peli_random)[2]) 
        except TypeError:
            return render_template("Inicio.html")
        
dif_dificil()

print(opciones)
    


