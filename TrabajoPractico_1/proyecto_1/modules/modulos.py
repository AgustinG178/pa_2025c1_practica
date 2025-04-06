import random

nombre_archivo = "frases_de_peliculas.txt"

def leer_frases_de_peliculas(nombre_archivo):

    frases = []
    with open("TrabajoPractico_1/proyecto_1/data/frases_de_peliculas.txt", 'r', encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if ';' in linea:  
                frases.append(linea.split(';'))
    return frases      

frases = leer_frases_de_peliculas(nombre_archivo)      

def opciones_pelis (frases_pelis,lista_peliculas):
    while len(lista_peliculas) < 3: 
        opcion_ronda =random.choice(frases_pelis)
        pelicula = opcion_ronda[1].title()    
    #La función asegura que por ronda no haya repeticiones en las opciones de películas, ya que cada película tiene varias frases
        if pelicula not in lista_peliculas: 
            lista_peliculas.append(pelicula)
            frases_pelis.remove(opcion_ronda)
    
    return lista_peliculas, frases_pelis

                
   

def juego_opciones(frases, intentos):
    frases_0 = frases.copy() #copiamos la lista original, de esta manera cada vez que se llame a la funcion juego_opciones, siempre se podrá jugar
                           #frases.copy() crea una nueva lista con dirección de memoria diferente 
    
    juego = [] #[[[opcion_correcta],[peliculas]]] opcion correcta es una lista, en el indice 0 se ubica la frase correcta y en el 1 la pelicula que le corresponde
               #peliculas es una lista que incluirá 3 peliculas, una justamentes es la que le corresponde a la frase.
    
    for _ in range (intentos):

        opcion_correcta = []
        pelis=[]
        ronda =[] 

        sublista_random = random.choice(frases_0)
        opcion_correcta.append([sublista_random[0],sublista_random[1].title()])
        ronda.append(opcion_correcta)

        #añadimos la opcion correcta
        pelis.append(sublista_random[1].title()) 
        frases_0.remove(sublista_random)
        
        #creamos el total de opciones a mostrar
        opciones_pelis_juego,frases_0 = opciones_pelis(frases_0,pelis)[0],opciones_pelis(frases_0,pelis)[1]

              

        random.shuffle(opciones_pelis_juego)
        ronda.append(opciones_pelis_juego) #ronda interpretacion: ronda[0] = opcion correcta, ronda[1] = lista de películas a usar en la ronda
        juego.append(ronda)
        
        #juego[i] = ronda, entonces juego[i][0] = opcion correcta (lista: frase,peli) y juego[i][1] =  peliculas a mostrar

    return juego
    #devolvemos la opcion correcta junto con una lista juego, que será lo que se mostrará
    #cada ronda

def opcion_correcta(pelicula,pelicula_correcta):
    if pelicula == pelicula_correcta:
        return 1
    else:
        return 0
   
def escribir_resultados_archivo(usuario,resultado,intentos,fecha): #Escribimos en un txt los resultados de un usuario
    with open("TrabajoPractico_1/proyecto_1/data/resultados.txt", 'a', encoding="utf-8") as historial:
        historial.write(f"Usuario:{usuario} / Resultado: {resultado}/{intentos} / Fecha: {fecha}\n")


def leer_archivo_resultados ():
    with open("TrabajoPractico_1/proyecto_1/data/resultados.txt", 'r', encoding="utf-8") as historial:
        juego_data = historial.read().splitlines()
        return juego_data



        
if __name__ == "__main__":
    print(juego_opciones(frases,7))
    #for ronda_0 in juego_opciones(frases,4):
        #print(f"Frase: {ronda_0[0][0][0]}")
        #print(f"Opciones: {ronda_0[1]}")
        #print(len(frases))  
        
    #print(opciones_pelis(frases,["El Padrino"]))
     
"""
    print(leer_archivo_resultados())
    for i in leer_archivo_resultados():
         print(i)
"""
    
    
  

