#Se definirán funciones para leer archivos .txt
def leer_archivo_txt(ruta_archivo:str):

    with open (ruta_archivo,"r") as archivo:

        """
        Se lee el archivo y se devuelve como una lista
        """
        
        try:
            informacion = []
            with open(ruta_archivo,"r",encoding="utf-8") as archivo:

                for linea in archivo:

                    dato = linea.strip().split("/")
                    nombre,dni = dato[0],dato[1]

                    informacion.append([nombre,dni])

        except FileNotFoundError:

            print("El archivo no se ha encontrado")

        return informacion