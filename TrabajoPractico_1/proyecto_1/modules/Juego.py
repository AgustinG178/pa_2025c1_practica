import modulos

nombre_archivo = "frases_de_peliculas.txt"

frases = modulos.leer_frases_de_peliculas(nombre_archivo)

frase, peli_i, peli_c = modulos.seleccionar_peli(frases, 10)

for _ in range(10):
    print (frase)
    print (peli_c)
    print (peli_i)
    


