class Persona:
    def __init__(self, nombre:str, dni:int):

        self.__Nombre = nombre

        self.__DNI = dni

        def get_Nombre(self):
            return self.__Nombre
        
class Estudiante(Persona):
    super()
        