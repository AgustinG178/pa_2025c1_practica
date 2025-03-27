import modulos
from random import shuffle

nombre_archivo = "frases_de_peliculas.txt"

frases = modulos.leer_frases_de_peliculas(nombre_archivo)

frase, dic = modulos.seleccionar_peli(frases, 1)

#for _ in range(10):
#    print (frase)
#    print (listaop[0])
#    print (listaop[2])

print(dic)

