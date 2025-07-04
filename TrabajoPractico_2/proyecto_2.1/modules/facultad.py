from modules.comunidad_academica import Profesor, Estudiante
from modules.departamento import Departamento
from modules.curso import Curso
import sys

class Facultad:
    def __init__(self, Nombre:str , Direccion:str, departamentos_académicos:list[object:Departamento]):

        """
        La clase facultad describirá el nombre, dirección y número de contacto, asi como la lista de estudiantes, profesores, departamentos y cursos que se brinden en la misma

        """
        self.__Nombre = Nombre

        self.__Direccion = Direccion
        
        self.__departamentosacademicos = departamentos_académicos
        
        self.__estudiantes = [estudiante for dpto in self.__departamentosacademicos for curso in dpto.mostrar_cursos for estudiante in curso.estudiantes]
        
        self.__profesores = [profesor for dpto in self.__departamentosacademicos for profesor in dpto.listar_profesores]

        self.__cursos = [curso for dpto in self.__departamentosacademicos for curso in dpto.mostrar_cursos]

    @property
    def nombre(self):
        return self.__Nombre
    @property
    def listar_departamentos(self):
            
            """
        Se muestran todos los departamentos académicos que existen en la facultad hasta el momento.
            """

            return [departamento for departamento in self.__departamentosacademicos]
    @property
    def listar_cursos(self):
        """
        Se muestran todos los cursos que existen en la facultad hasta el momento.
        """

        return [curso for curso in self.__cursos]
    
    @listar_cursos.setter
    def listar_cursos(self,p_curso:Curso):
        self.__cursos.append(p_curso)
        
        return f"Se ha añadido correctamente el curso: {p_curso.nombre_curso} a la facultad"
    @property
    def listar_estudiantes (self):
        """
        Se muestran todos los estudiantes inscriptos en la facultad hasta el momento.
        """

        return [p_estudiante for p_estudiante in self.__estudiantes]
    @property
    def listar_profesores (self):

        """
        Se muestran todos los profesores contratados por la facultad hasta el momento.
        """

        return [profesor for profesor in self.__profesores]

   

    def añadir_estudiantes(self, *estudiantes:object):

        """
        Se añaden a la facultad los estudiantes, si no es una instancia de la clase estudiante se le indica al usuario cual estudiante es.
        """
        
        for p_estudiante in estudiantes:

            if not isinstance(p_estudiante, Estudiante):

                print(f"El estudiante {p_estudiante} no es una instancia de la clase Estudiante, no será agregado a la facultad")

            else:
                self.__estudiantes.append(p_estudiante)
                p_estudiante.facultades.append(self)
                print(f"Se a añadido el estudiante {p_estudiante.get_nombre} a la facultad correctamente.")

    def contratar_profesor(self, p_profesor:object):
        """
        Se añade a la facultad un profesor que debe ser un objeto
        """
        
        if not isinstance(p_profesor,Profesor):

            raise TypeError("El profesor debe ser la instancia de una clase (objeto)")

        self.__estudiantes.append(p_profesor)
        p_profesor.facultades.append(self)
        print(f"¡El profesor {p_profesor.nombre} ha sido contratado correctamente!")

    def agregar_estudiante_a_curso(self,p_curso:Curso,p_estudiante:Estudiante):

        """
        Se añade un estudiante al curso que seleccione el usuario
        """

        if isinstance(p_curso,Curso) and isinstance(p_estudiante,Estudiante):

            p_estudiante.cursos = p_curso
            return f"Se ha añadido correctamente el estudiante {p_estudiante.get_nombre} al curso {p_curso.nombre_curso}"
        raise TypeError("El curso y el estudiante han de ser ambos objetos de su correspondiente clase.")
    def agregar_curso(self,curso:object):

        if isinstance(curso,Curso):

            self.listar_cursos.append(curso)
            
        
        else:
            raise TypeError("El curso debe ser un objeto")

        
    def agregar_departamento (self, p_departamento:Departamento):

        if not isinstance(p_departamento,Departamento):
            raise TypeError(f"El parámetro {p_departamento} no es una instancia de la clase Departamento")
        
        self.__departamentosacademicos.append(p_departamento)
        return f"Se ha añadido correctamente el departamento {p_departamento.nombre_departamento} a la facultad."
