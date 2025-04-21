
class  Departamento:
    def __init__(self,nombre:str, cursos:list, profesores_departamento:list[object],director = object):
        """
        Se crea un departamento académico dentro de una facultad.
        La clase recibe como parámetro el nombre del departamento, el director que le corresponde,
        los profesores que dan clases y los cursos que se dictan en este.
        """
        self.nombre_departamento = nombre

        self.cursos = cursos

        self.profesores_departamento = profesores_departamento

        self.director = director
    def mostrar_información(self):

        return f"Nombre departamento:{self.nombre_departamento}/Cursos:{",".join(self.cursos)}/Profesores:{",".join(self.profesores_departamento)}"

           