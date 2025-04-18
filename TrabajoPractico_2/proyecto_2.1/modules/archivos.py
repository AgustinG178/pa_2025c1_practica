#Se definirán funciones para leer archivos .txt
from modules.comunidad_academica import Estudiante,Profesor
def leer_archivo_txt(ruta_archivo:str):

    with open (ruta_archivo,"r") as archivo:

        """
        Se lee el archivo y se devuelve como una lista
        """
        return archivo.splitlines()
    
def escribir_datos_en_archivo(dato:object):

    """
    Se escribirán los datos dependiendo el objeto ingresado, en un archvivo u otro.
    """

    if isinstance(dato, Estudiante):

        with open ("TrabajoPractico_2/proyecto_2.1/data/Estudiantes.txt", "a") as archivo:

            archivo.write(dato.mostrar_informacion)
    
    if isinstance(dato,Profesor):

        with open ("TrabajoPractico_2/proyecto_2.1/data/Profesores.txt", "a") as archivo:

            archivo.write(dato.mostrar_informacion)


        