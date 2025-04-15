class Persona:
    """ clase padre de Estudiante y Profesor """
    def __init__(self, nombre:str, dni:int):

        self.nombre = nombre

        self.dni = dni

    @property
    def get_nombre(self): #getter general
        return self.nombre
        
class Estudiante(Persona):

    def __init__(self, cursos: list, facultades:list, nombre:str , dni:int):
        super().__init__(nombre, dni)

        self.cursos = cursos

        self.facultades = facultades

    def mostrar_informacion(self):

        """
        Se muestra la información del estudiante.
        """
        return f"Nombre: {self.nombre}\n DNI: {self.dni}\n Cursos: {self.cursos}\n Facultades: {self.facultades}"
        
    def mostrar_cursos(self):

        """
        Se muestran todos los cursos a los que el paciente asiste
        """

        return f""

class Profesor(Persona):
    def __init__(self, nombre: str, dni: int, cursos:list, facultades:list):

        super().__init__(nombre, dni)

        self.__cargos = []

        self.cursos = cursos

        self.facultades = facultades

    @property
    def mostrar_cargos(self):

        return self.__cargos

    @mostrar_cargos.setter

    
    def mostrar_cargos(self,cargo):
        """
        Se le asigna un cargo al profesor.
        """

        self.__cargos.append(cargo)
        

    def mostrar_informacion(self) ->str:

        """
        Se muestra la información del profesor.
        """
        return f"Nombre: {self.nombre}\nDNI: {self.dni}\nCursos: {self.cursos}\nCargos:{self.__cargos}\nFacultades: {self.facultades}"


if __name__ == "__main__":
    prof1 = Profesor("Lucas", 485, 9853.5, ["matematica","quimica"],["FIUNER","FIQ"])

    print(f"Cargos iniciales: {prof1.mostrar_cargos}")
    prof1.mostrar_cargos ="matematica"
    """
    prof1.mostrar_cargos muestra el atributo privado cargos relacionado al profesor, prof1.mostrar_cargos = "matematica"
    es un setter, define el cargo (en este caso lo añade a la lista de campos)
    """
    print(f"Cargos actuales: {prof1.mostrar_cargos}")

    print(prof1.mostrar_informacion())