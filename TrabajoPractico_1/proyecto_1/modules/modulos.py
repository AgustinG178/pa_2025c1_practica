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

def juego_opciones(frases, intentos):
    frases_0 = frases
    opcion_correcta = []
    pelis=[]
    juego = [] #[[[opcion_correcta],[peliculas]]] opcion correcta es una lista, en el indice 0 se ubica la frase correcta y en el 1 la pelicula que le corresponde
               #peliculas es una lista que incluirá 3 peliculas, una justamentes es la que le corresponde a la frase.
    ronda =[] 
    for _ in range (intentos):
        sublista_random = random.choice(frases_0)
        opcion_correcta.append([sublista_random[0],sublista_random[1]])
        ronda.append(opcion_correcta)
        pelis.append(sublista_random[1]) #añadimos la opcion correcta
        frases_0.remove(sublista_random)
        
        for _ in range(2):

              peli_aleatoria = random.choice(frases_0)
              pelis.append(peli_aleatoria[1])
              frases_0.remove(peli_aleatoria)
        
        
        random.shuffle(pelis)
        ronda.append(pelis) #ronda interpretacion: ronda[0] = opcion correcta, ronda[1] = lista de películas a usar en la ronda
        juego.append(ronda)
        #juego[i] = ronda, entonces juego[i][0] = opcion correcta (lista: frase,peli) y juego[i][1] =  peliculas a mostrar

        return juego
    #devolvemos la opcion correcta junto con una lista juego, que será lo que se mostrará
    #cada ronda
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
    


if __name__ == "__main__":
        
    for ronda in juego_opciones(frases,1):
        print(f"Frase: {ronda[0][0][0]}")
        print(f"Opciones: {ronda[1]}")



