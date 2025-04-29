
class Persona:
    """ clase padre de Estudiante y Profesor """
    def __init__(self, nombre:str, dni:int):

        self.nombre = nombre

        self.dni = dni
        
class Estudiante(Persona):

    def __init__(self,nombre:str , dni:int):
        super().__init__(nombre, dni)

        self.cursos = []

        self.facultades = []

    def mostrar_informacion(self):

        """
        Se muestra la información del estudiante.
        """
        return f"Nombre: {self.nombre}/ DNI: {self.dni}/ Cursos: {",".join(curso.nombre_curso for curso in self.cursos)}/ Facultades: {",".join(facultad.Nombre for facultad in self.facultades)}"
        
    def mostrar_cursos(self):

        """
        Se muestran todos los cursos a los que el paciente asiste
        """

        return f""

class Profesor(Persona):
    def __init__(self, nombre: str, dni: int, cursos:list, departamentos:list, facultades:list):

        super().__init__(nombre, dni)

        self.director_departamento = ""

        self.titular_cursos = []

        self.cursos = cursos

        self.facultades = facultades

        self.departamentos = departamentos


    def mostrar_informacion(self) ->str:

        """
        Se muestra la información del profesor.
        """
        return f"Nombre: {self.nombre}/ DNI: {self.dni}/ Cursos: {",".join(curso.nombre_curso for curso in self.cursos)} / Director de:{",".join(self.titular_cursos)} / Departamentos: {",".join(self.departamentos)}/ Facultades: {",".join(facultad.Nombre for facultad in self.facultades)}"

    def mostrar_cursos(self):

        return[curso for curso in self.cursos]
    
    def mostrar_departamentos (self):

        return[departamento for departamento in self.departamentos]