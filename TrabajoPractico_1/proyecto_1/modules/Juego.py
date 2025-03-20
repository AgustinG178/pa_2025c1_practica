from modules.modulos import leer_frases_de_peliculas, seleccionar_peli, dif_dificil
import random
from flask import render_template


frases_usadas = []

nombre_archivo = "frases_de_peliculas.txt"

frases = leer_frases_de_peliculas(nombre_archivo)

frase, peliculas, frases_usadas = seleccionar_peli(frases) 

"""juego principal"""

frases = leer_frases_de_peliculas(nombre_archivo)
frase = random.choice(frases[0])
opciones=[]
peli_random = []

    
print(peliculas) 
        

    


