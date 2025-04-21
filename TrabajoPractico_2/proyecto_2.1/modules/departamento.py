from modules.curso import Curso
from modules.comunidad_academica import Profesor
class  Departamento:
    def __init__(self,nombre:str,lista_cursos:list[object], lista_profesores:list[object], director:object):
        """
        Se crea un departamento académico dentro de una facultad.
        La clase recibe como parámetro el nombre del departamento, el director que le corresponde,
        los profesores que dan clases y los cursos que se dictan en este.
        """
        self.nombre_departamento = nombre

        self.cursos = lista_cursos

        self.profesores_departamento = lista_profesores 

        self.director = [director]
        
    def agregar_curso(self, p_curso:object):
        if not isinstance(p_curso,Curso):

            return "El curso que se desea añadir no es una instancia de la clase Curso"
        self.cursos.append(p_curso)
        print(f"Se ha añadido correctamente el curso {p_curso.nombre_curso} al departamento {self.nombre_departamento}")
    def mostrar_cursos(self):

        return[curso for curso in self.cursos]
    def nombrar_director(self,p_profesor:object):

        if not isinstance(p_profesor,Profesor):

            return "El profesor no es una instancia de la clase Profesor"
        
        self.director[0] = p_profesor
        print(f"Se ha nombrado correctamente al profesor {p_profesor.nombre} como director del departamento")


        
    

    


           