from modules.modulo1 import leer_frases_de_peliculas, seleccionar_frase
import random
from flask import render_template, app


frases_usadas = []

nombre_archivo = "frases_de_peliculas.txt"

frases = leer_frases_de_peliculas(nombre_archivo)

frase, pelicula, frases_usadas = seleccionar_frase(frases) #podriamos meter esta funcion en un for de 3 ciclos cada vez que se seleccione o una dificultad o una respuesta 
                                            #asi se seleccionan 3 películas constantemente
                                            
"""dificil"""

frases = leer_frases_de_peliculas(nombre_archivo)
opciones=[]
frase_random = random.choice(frases)[1] 

def dif_dificil():

    for i in range(3): 
        try:
            opciones.append([seleccionar_frase(frases)[0],seleccionar_frase(frases)[1]]) 
        except TypeError:
            return render_template("Inicio.html")
        
    


