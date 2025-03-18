from modules.modulo1 import leer_frases_de_peliculas, seleccionar_frase

frases = []

nombre_archivo = "frases_de_peliculas.txt"

frases = leer_frases_de_peliculas(nombre_archivo)

frase, pelicula = seleccionar_frase(frases)

print(f"Frase seleccionada: {frase}")

print(f"Película: {pelicula}")