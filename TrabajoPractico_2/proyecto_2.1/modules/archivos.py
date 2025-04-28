# Se definirán funciones para leer archivos .txt
def leer_archivo_txt(ruta_archivo: str):
    """
    Se lee el archivo y se devuelve como una lista
    """
    try:
  
        informacion = []
  
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
  
            for linea in archivo:
  
                dato = linea.strip().split("/")
  
                nombre, dni = dato[0], dato[1]
  
                informacion.append([nombre, dni])
  
    except FileNotFoundError:
  
        print("El archivo no se ha encontrado")
  
        informacion = []  # Retorna una lista vacía si no se encuentra el archivo
  
    return informacion

if __name__ == "__main__":
    # Prueba de la función leer_archivo_txt
    ruta_archivo = "data/profesores.txt"  # Cambia esto a la ruta de tu archivo
    datos = leer_archivo_txt(ruta_archivo)
    if datos:
        print("Profesores:")
        for registro in datos:
            print(f"Nombre: {registro[0]}, DNI: {registro[1]}")
    else:
        print("No se pudo leer el archivo o está vacío.")
        
    ruta_archivo = "data/estudiantes.txt"  # Cambia esto a la ruta de tu archivo
    datos = leer_archivo_txt(ruta_archivo)
    if datos:
        print("Estudiantes:")
        for registro in datos:
            print(f"Nombre: {registro[0]}, DNI: {registro[1]}")
    else:
        print("No se pudo leer el archivo o está vacío.")