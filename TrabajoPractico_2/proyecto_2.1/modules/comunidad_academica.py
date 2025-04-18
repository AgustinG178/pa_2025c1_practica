class Persona:
    """ clase padre de Estudiante y Profesor """
    def __init__(self, nombre:str, dni:int):

        self.nombre = nombre

        self.dni = dni
        
class Estudiante(Persona):

    def __init__(self, cursos: list, facultades:list, nombre:str , dni:int):
        super().__init__(nombre, dni)

        self.cursos = cursos

        self.facultades = facultades

    def mostrar_informacion(self):

        """
        Se muestra la información del estudiante.
        """
        return f"Nombre: {self.nombre}/ DNI: {self.dni}/ Cursos: {",".join(self.cursos)}/ Facultades: {",".join(self.facultades)}"
        
    def mostrar_cursos(self):

        """
        Se muestran todos los cursos a los que el paciente asiste
        """

        return f""

class Profesor(Persona):
    def __init__(self, nombre: str, dni: int, cursos:list, departamentos:list, facultades:list):

        super().__init__(nombre, dni)

        self.__cargos = []

        self.cursos = cursos

        self.facultades = facultades

        self.departamento = departamentos

    @property
    def cargos(self):
        """
        Se muestran los cargos directivos del profesor
        """
        return self.__cargos

    @cargos.setter

    
    def cargos(self,cargo):
        """
        Se le asigna un cargo al profesor.
        """

        self.__cargos.append(cargo)
        

    def mostrar_informacion(self) ->str:

        """
        Se muestra la información del profesor.
        """
        return f"Nombre: {self.nombre}/ DNI: {self.dni}/ Cursos: {",".join(self.cursos)} / Cargos:{",".join(self.__cargos)} / Departamentos: {",".join(self.departamento)}/ Facultades: {",".join(self.facultades)}"


if __name__ == "__main__":
    prof1 = Profesor("Lucas", 485,["Matematica","Quimica"],["Fisico Química"],["FIUNER","FIQ"])

    print(f"Cargos iniciales: {prof1.cargos}")
    prof1.cargos ="Matematica"
    """
    prof1.mostrar_cargos muestra el atributo privado cargos relacionado al profesor, prof1.mostrar_cargos = "matematica"
    es un setter, define el cargo (en este caso lo añade a la lista de campos)
    """
    print(f"Cargos actuales: {prof1.cargos}")

    print(prof1.mostrar_informacion())