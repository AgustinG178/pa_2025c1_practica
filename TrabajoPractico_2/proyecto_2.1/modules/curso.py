from modules.comunidad_academica import Estudiante,Profesor
class Curso:
    def __init__(self, nombre_curso:str, profesores_curso:list[object], estudiantes_curso:list[object],titular:object):
        """
        La clase curso estará en asociación con estudaintes y profesores, los estudaintes asisten a los cursos, los
        profesores enseñan en los cursos.
        """
        self.nombre_curso = nombre_curso

        self.profesores_curso = profesores_curso

        self.estudiantes_curso = estudiantes_curso

        self.__titular = [titular]

        profesores_curso[0].titular_cursos.append(self)

        for profesor in profesores_curso:
             profesor.cursos.append(self)

        for estudiante in self.estudiantes_curso:
             estudiante.cursos.append(self)
         
    @property
    
    def titular(self):
         return self.__titular

    @titular.setter
    
    def titular(self,p_profesor):
         
         self.__titular = p_profesor

    def mostrar_estudiantes_curso(self):

        """
        Se muestran todos los estudiantes inscriptos en el curso hasta el momento.
        """

        return [p_estudiante.nombre for p_estudiante in self.estudiantes_curso]
    def mostrar_profesores_curso(self):

        """
        Se muestran todos los profesores que dan clases en el curso hasta el momento.
        """

        return [p_profesor.nombre for p_profesor in self.profesores_curso]

    def agregar_estudiante(self,p_estudiante:object):

            """
            Se añade un estudiante al curso que seleccione el usuario
            """

            if not isinstance(p_estudiante,Estudiante):
                 
                print("El estudiante no es es una instancia de la class Estudiante")
            
            self.estudiantes_curso.append(p_estudiante)
    
    