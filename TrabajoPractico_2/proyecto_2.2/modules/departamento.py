from modules.profesor import profesor
from modules.curso import curso


class  departamento:
    def __init__(self, director:object, cursos:list, profesores_departamento:list, nombre_departamento:str):
        """
        Se crea un departamento académico dentro de una facultad.
        La función recibe el nombre del departamento, el director que le corresponde y los cursos que se dictan en este.
        """
        self.nombre_departamento = nombre_departamento
        self.cursos = [cursos]
        self.director = director
        self.profesores_departamento = profesores_departamento
        self.profesor_asistente = []
        self.clases = []
        
        def nombrar_departamento():
            """
            Se le asigna un nombre al departamento académico.
            """
            
            self.nombre_departamento = input("Ingrese el nombre del departamento: ")
        
        def agregar_profesor(profesor:object):
            """
            Se añade un profesor al departamento académico, el cual debe ser un objeto.
            """
            if type(profesor) == object:
                self.profesores_departamento.append(profesor)
                print(f"¡El profesor {profesor.Nombre} ha sido contratado correctamente!")
            
            else: raise TypeError("El profesor debe ser la instancia de una clase (objeto)")
            
        def crear_departamento_nuevo(nombre_departamento:str, director:object, cursos:list, profesores_departamento:list):
            
            self.nombre_departamento = nombrar_departamento()
            self.director = director
            self.cursos = []
            self.nombre_departamento = agregar_profesor(profesor)
            
            
        

        