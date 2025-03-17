# módulo para organizar funciones o clases utilizadas en nuestro proyecto
# Crear tantos módulos como sea necesario para organizar el código

def leer_frases_de_peliculas(nombre_archivo):

    lista_de_frases = []
    
    with open("data/frases_de_peliculas.txt", 'r', encoding='utf-8') as archivo:
        
        for linea in archivo:
               
            linea_limpia = linea.strip().split(";")
    
            lista_de_frases.append([linea_limpia])
    
    return lista_de_frases