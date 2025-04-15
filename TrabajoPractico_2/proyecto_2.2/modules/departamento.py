from comunidad_academica import Profesor

#Diccionario que contendrá todos los departamentos académicos hasta el momento, de forma que se puedan acceder/listar
departamentos = {} 

class  Departamento:
    def __init__(self,nombre:str, director:object, cursos:list, profesores_departamento:list[object]):
        """
        Se crea un departamento académico dentro de una facultad.
        La clase recibe como parámetro el nombre del departamento, el director que le corresponde,
        los profesores que dan clases y los cursos que se dictan en este.
        """
        self.nombre_departamento = nombre
        self.cursos = cursos
        self.director = director
        self.profesores_departamento = profesores_departamento

        


    def agregar_profesor(self,profesor:object):
        """
        Se añade un profesor al departamento académico, el cual debe ser un objeto.
        """
        if not isinstance(profesor):
            raise TypeError("El profesor debe ser la instancia de una clase (objeto)")
        
        else:
            self.profesores_departamento.append(profesor)
            print(f"¡El profesor {profesor.Nombre} ha sido contratado correctamente!")       