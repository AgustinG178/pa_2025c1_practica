class Curso:
    def __init__(self, nombre_curso:str, profesores_curso:list[object], estudiantes_curso:list[object],director:object):
        """
        La clase curso estará en asociación con estudaintes y profesores, los estudaintes asisten a los cursos, los
        profesores enseñan en los cursos.
        """
        self.nombre_curso = nombre_curso

        self.profesores_curso = profesores_curso

        self.estudiantes_curso = estudiantes_curso

        self.director = director    

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

    def mostrar_informacion_curso(self):
        """
        Se mostrará la información basica del curso, como la cantidad de alumnos que lo componen y los profesores que dan clases en este
        """

        return f"En el curso se encuentran {len(self.estudiantes_curso)} estudiantes hasta el momento, y hay {len(self.profesores_curso)}"
    
