from modules.modulo1 import leer_frases_de_peliculas, seleccionar_frase

frases_usadas = []

nombre_archivo = "frases_de_peliculas.txt"

frases = leer_frases_de_peliculas(nombre_archivo)

frase, pelicula = seleccionar_frase(frases) #podriamos meter esta funcion en un for de 3 ciclos cada vez que se seleccione o una dificultad o una respuesta 
                                            #asi se seleccionan 3 películas constantemente

print(f"Frase seleccionada: {frase}")

print(f"Película: {pelicula}")