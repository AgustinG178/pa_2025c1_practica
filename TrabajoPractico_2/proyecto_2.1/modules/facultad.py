from modules.comunidad_academica import Profesor, Estudiante
from modules.departamento import Departamento
from modules.curso import Curso
import sys

class Facultad:
    def __init__(self, Nombre:str , Direccion:str, departamentos_académicos:list[object:Departamento]):

        """
        La clase facultad describirá el nombre, dirección y número de contacto, asi como la lista de estudiantes, profesores, departamentos y cursos que se brinden en la misma

        """
        self.Nombre = Nombre

        self.Direccion = Direccion
        
        self.departamentos_academicos = departamentos_académicos
        
        self.estudiantes = [estudiante for dpto in self.departamentos_academicos for curso in dpto.cursos for estudiante in curso.estudiantes_curso]
        
        self.profesores = [profesor for dpto in self.departamentos_academicos for profesor in dpto.profesores_departamento]

        self.cursos = [curso for dpto in self.departamentos_academicos for curso in dpto.cursos]


    def listar_estudiantes (self):
        """
        Se muestran todos los estudiantes inscriptos en la facultad hasta el momento.
        """

        return [p_estudiante.nombre for p_estudiante in self.estudiantes]
    
    def listar_profesores (self):

        """
        Se muestran todos los profesores contratados por la facultad hasta el momento.
        """

        return [profesor.nombre for profesor in self.profesores]

    def listar_departamentos(self):
            
            """
        Se muestran todos los departamentos académicos que existen en la facultad hasta el momento.
            """

            return [departamento.nombre_departamento for departamento in self.departamentos_academicos]

    def añadir_estudiantes(self, *estudiantes:object):

        """
        Se añaden a la facultad los estudiantes, si no es una instancia de la clase estudiante se le indica al usuario cual estudiante es.
        """
        
        for p_estudiante in estudiantes:

            if not isinstance(p_estudiante, Estudiante):

                print(f"El estudiante {p_estudiante} no es una instancia de la clase Estudiante, no será agregado a la facultad")

            else:
                self.estudiantes.append(p_estudiante)
                p_estudiante.facultades.append(self)
                print(f"Se a añadido el estudiante {p_estudiante.nombre} a la facultad correctamente.")

    def contratar_profesor(self, p_profesor:object):
        """
        Se añade a la facultad un profesor que debe ser un objeto
        """
        
        if not isinstance(p_profesor,Profesor):

            raise TypeError("El profesor debe ser la instancia de una clase (objeto)")

        self.profesores.append(p_profesor)
        p_profesor.facultades.append(self)
        print(f"¡El profesor {p_profesor.nombre} ha sido contratado correctamente!")

    def agregar_estudiante_a_curso(self,p_curso:Curso,p_estudiante:Estudiante):

        """
        Se añade un estudiante al curso que seleccione el usuario
        """

        if isinstance(p_curso,Curso) and isinstance(p_estudiante,Estudiante):

            p_estudiante.cursos.append(p_curso)
            return f"Se ha añadido correctamente el estudiante {p_estudiante} al curso {p_curso}"
        raise TypeError("El curso y el estudiante han de ser ambos objetos de su correspondiente clase.")
    def agregar_curso(self,curso:object):

        if isinstance(curso,Curso):

            self.cursos.append(curso)
            return f"Se ha añadido correctamente el curso: {curso.nombre_curso} a la facultad"
        
        else:
            raise TypeError("El curso debe ser un objeto")

        
    def agregar_departamento (self, p_departamento:Departamento):

        if not isinstance(p_departamento,Departamento):
            raise TypeError(f"El parámetro {p_departamento} no es una instancia de la clase Departamento")
        
        self.departamentos_academicos.append(p_departamento)
        return f"Se ha añadido correctamente el departamento {p_departamento.nombre_departamento} a la facultad."



if __name__ == "__main__":

    """
    fac1 = Facultad("fiuner","oro verde")
    prof2 = Profesor("María", 789, [],[], [fac1])
    fac1.contratar_profesor(prof2)
    prof3 = Profesor("Carlos", 321, [],[],[fac1])
    fac1.contratar_profesor(prof3)
    prof4 = Profesor("Ana", 655, [],[], [fac1])
    fac1.contratar_profesor(prof4)

    estudiante1 = Estudiante(nombre="María", dni="10111213")
    estudiante2 = Estudiante(nombre="Juan", dni="14151617")
    estudiante3 = Estudiante(nombre="Sofía", dni="18192021")

    fac1.añadir_estudiantes(estudiante1,estudiante2,estudiante3)
    curso_programacion = Curso("programacion",[prof2,prof3,prof4],[estudiante1,estudiante2,estudiante3],director=prof2)
    fac1.agregar_curso(curso_programacion)
    
    fac1.crear_departamento()
    fac1.crear_curso()
    departamento = Departamento("Computación",cursos=[curso_programacion],profesores_departamento=[prof2,prof3,prof4])
    print(estudiante1.mostrar_informacion())
    print(prof2.mostrar_informacion())
""" 
    