import abc

class Persona(abc.ABC):
    """ clase padre de Estudiante y Profesor """
    def __init__(self, nombre:str, dni:int):

        self.__nombre = nombre

        self.__dni = dni
    
    @property
    def get_nombre(self):
        return self.__nombre

class Estudiante(Persona):

    def __init__(self,nombre:str , dni:int):
        super().__init__(nombre, dni)

        self.__nombre = nombre

        self.__dni = dni

        self.__cursos = []

        self.__facultades = []
   
    @property
    def mostrar_informacion(self):

        """
        Se muestra la información del estudiante.
        """
        return f"Nombre: {self.__nombre}/ DNI: {self.__dni}/ Cursos: {', '.join(curso.nombre_curso for curso in self.__cursos)}/ Facultades: {', '.join(facultad.nombre for facultad in self.__facultades)}"

    
    
   
    
    @property
    def lista_cursos(self):
        self.__cursos
    @lista_cursos.setter
    
    def cursos(self,curso):
        self.__cursos.append(curso)

    @property 
    def facultades(self):
        return self.__facultades
    
    @facultades.setter
    def facultades (self, facultad):
        self.__facultades.append(facultad)

class Profesor(Persona):
    def __init__(self, nombre: str, dni: int, curso, departamentos:list, facultades:list):

        super().__init__(nombre, dni)

        self.__nombre = nombre

        self.__dni = dni
        self.__director_departamento = ""

        self.__titular_curso = []

        self.__curso = curso

        self.__facultades = facultades

        self.__departamentos = departamentos

    from modules.departamento import Departamento

    @property 
    def facultades(self):
        return self.__facultades
    
    @facultades.setter
    def facultades (self, facultad):
        self.__facultades.append(facultad)
    @property
    def nombre(self) ->str:

        """
        Se muestra el nombre del profesor.
        """
        return self.__nombre
    
    @property
    def mostrar_informacion(self) ->str:

        """
        Se muestra la información del profesor.
        """
        return f"Nombre: {self.__nombre}/ DNI: {self.__dni}/ Curso: {self.__curso.nombre_curso} / Titular de: {self.__titular_curso} / Departamentos: {', '.join(self.__departamentos)}/ Facultades: {', '.join(facultad.nombre for facultad in self.__facultades)}"
    
    @property
    def mostrar_curso(self):

        return self.__curso
           
    @property
    def mostrar_departamentos (self):

        return[departamento for departamento in self.__departamentos]
    @property
    def director (self):
        return self.__director_departamento
    @director.setter
    def director(self,departamento:Departamento):
        self.__director_departamento = departamento

    @property
    def titular(self):
        return self.__titular_curso
    
    @titular.setter
    def titular (self,curso):
        self.__titular_curso.append(curso)

