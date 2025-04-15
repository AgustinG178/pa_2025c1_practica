# módulo para organizar funciones o clases utilizadas en nuestro proyecto
# Crear tantos módulos como sea necesario para organizar el código
from comunidad_academica import Profesor, Estudiante
from departamento import Departamento
class Facultad:
    def __init__(self, Nombre:str , Direccion:str):

        """
        La clase facultad describirá el nombre, dirección y número de contacto, asi como la lista de estudiantes

        """
        self.Nombre = Nombre

        self.Direccion = Direccion
        
        self.estudiantes =[]

        self.profesores = []
        self.departamentos_academicos = []

    def listar_estudiantes (self):
        """
        Se muestran todos los estudiantes inscriptos en la facultad hasta el momento.
        """

        return [p_estudiante.get_nombre for p_estudiante in self.estudiantes]
    
    def listar_profesores (self):

        """
        Se muestran todos los profesores contratados por la facultad hasta el momento.
        """

        return [profesor.get_nombre for profesor in self.profesores]

        
    
    def listar_departamentos(self):
            
            """
        Se muestran todos los departamentos académicos que existen en la facultad hasta el momento.
            """

            return [departamento.get_Nombre() for departamento in self.departamentos]

    def añadir_estudiante(self, p_estudiante:object):

        """
        Se añade a la facultad un estudiante que debe ser un objeto
        """
        if not isinstance(p_estudiante, Estudiante):

            raise TypeError("El estudiante debe ser la instancia de una clase (objeto)")

        self.estudiantes.append(p_estudiante)

    def contratar_profesor(self, p_profesor:object):
        """
        Se añade a la facultad un profesor que debe ser un objeto
        """
        
        if not isinstance(p_profesor,Profesor):

            raise TypeError("El profesor debe ser la instancia de una clase (objeto)")

        self.profesores.append(p_profesor)
        print(f"¡El profesor {p_profesor.nombre} ha sido contratado correctamente!")



    def crear_departamento (self):
            
        """
        Se crea un departamento académico con todos los elementos que contiene, 
        la creación es interactiva con el usuario que la crea.
        """

        profesores_departamento = []
        cursos = []


        nombre = input("Ingrese el nombre del departamento académico: ")
            
        print("Los profesores disponibles son:")
        for indice,profesor in enumerate(self.profesores):
            print(f"{indice}:{profesor.get_nombre}")
            
        num_director = int(input("Ingrese el número que corresponde al profesor que será director:"))
        director = self.profesores[num_director]

        profesores_departamento.append(self.profesores[num_director])


        print("Ahora ingrese el número de los demás profesores que se encontrarán en el departamento,ingrese FIN para terminar la seleccion")
        while True:

            num_profesor = input("Ingrese el número del profesor").strip()
            if len(profesores_departamento) == len(self.profesores):
                print("No hay más profesores para añadir, continue con la creación del departamento.")
                break
            if num_profesor == "FIN":
                break
            try:
                if self.profesores[int(num_profesor)] not in profesores_departamento:

                    profesores_departamento.append(self.profesores[int(num_profesor)])

                else:
                    print("El profesor ya se encuentra añadido, por favor seleccione otro.")
            except (IndexError,TypeError,ValueError):
                print("El número ingresado no corresponde a ningún profesor o no es valido, por favor ingrese uno correctamente")
                
        print("\nIngrese los cursos que se dictarán en el departamento, ingrese FIN para terminar")

        while True:
            nombre_curso = input("Nombre del curso: ")
            if nombre_curso == "FIN":
                break
            
            cursos.append(nombre_curso)
            
            
        
        nuevo_departamento = Departamento(nombre,director,cursos,profesores_departamento)
        return nuevo_departamento

if __name__ == "__main__":

    fac1 = Facultad("fiuner","oro verde")
    prof2 = Profesor("María", 789, ["física general", "termodinámica"], ["FIQ", "FCE"])
    fac1.contratar_profesor(prof2)
    prof3 = Profesor("Carlos", 321, ["biología molecular", "genética"], ["FCByF"])
    fac1.contratar_profesor(prof3)
    prof4 = Profesor("Ana", 655, ["química orgánica", "química analítica"], ["FIQ", "FIQUI"])
    fac1.contratar_profesor(prof4)

    fac1.crear_departamento()
    