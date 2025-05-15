from modules.comunidad_academica import Estudiante,Profesor
class Curso:
    def __init__(self, nombre_curso:str, profesores:list[object], estudiantes_curso:list[object],titular:object):
        """
        La clase curso estará en asociación con estudaintes y profesores, los estudaintes asisten a los cursos, los
        profesores enseñan en los cursos.
        """
        self.__nombre_curso = nombre_curso

        self.__profesores_curso = profesores

        self.__estudiantes_curso = estudiantes_curso

        self.__titular = [titular]


         
    
    @property
    
    def titular(self):
         return self.____titular

    @titular.setter
    
    def titular(self,p_profesor):
         
         self.____titular = p_profesor

    @property
    def nombre_curso(self):
        """
        Se muestra el nombre del curso.
        """
        return self.__nombre_curso
    @property
    def estudiantes(self):

        """
        Se muestran todos los estudiantes inscriptos en el curso hasta el momento.
        """

        return [p_estudiante for p_estudiante in self.__estudiantes_curso]
    
    @estudiantes.setter
    def estudiantes(self,p_estudiante:Estudiante):
        self.__estudiantes_curso.append(p_estudiante)

    @property
    def listar_profesores(self):
         return [profesor for profesor in self.__profesores_curso]
    

    def agregar_estudiante(self,p_estudiante:object):

            """
            Se añade un estudiante al curso que seleccione el usuario
            """
           
            if not isinstance(p_estudiante,Estudiante):
                 
                print("El estudiante no es es una instancia de la class Estudiante")
            
            self.__estudiantes_curso.append(p_estudiante)
    
    