# módulo para organizar funciones o clases utilizadas en nuestro proyecto
# Crear tantos módulos como sea necesario para organizar el código
from comunidad_academica import Profesor, Estudiante
from departamento import Departamento
from curso import Curso

class Facultad:
    def __init__(self, Nombre:str , Direccion:str):

        """
        La clase facultad describirá el nombre, dirección y número de contacto, asi como la lista de estudiantes, profesores, departamentos y cursos que se brinden en la misma

        """
        self.Nombre = Nombre

        self.Direccion = Direccion
        
        self.estudiantes =[]

        self.profesores = []

        self.departamentos_academicos = []

        self.cursos = []

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


    def agregar_estudiante_a_curso(self):
        """
        Se añade un estudiante al curso que seleccione el usuario
        """


        print("La lista de estudiantes hasta el momento es")
        for indice,estudiante in enumerate(self.estudiantes):
            print(f"{indice}: {estudiante.nombre}")

        
        
        while True:
            num_estudiante = input("Seleccione el número del estudiante que quiera asignar a un curso")
            try:

                indice = int(num_estudiante)
                estudiante = self.estudiantes[indice]
                break
            except (ValueError,IndexError):
                print("Ingrese un número valido: ")

        print("Los cursos que se brindan en la facultad son:")

        for indice,curso in enumerate(self.cursos):
            print(f"{indice}: {curso.nombre_curso}")

        while True:
            num_curso = input("Seleccione el número del estudiante que quiera asignar a un curso")
            try:

                indice = int(num_curso)
                curso = self.cursos[indice]
                break
            except (ValueError,IndexError):
                print("Ingrese un número valido: ")

        curso.estudiantes_curos.append(estudiante) #se añade al curso el estudiante

        print(f"¡¡Se ha añadido correctamente el estudiante {estudiante.nombre} al curso {curso.nombre_curso}!!")
        
        return "¿Que acción desea realizar ahora?"
    

    def crear_curso(self):

        """
        Se creará un curso con los estudiantes y profesores presentes hasta el momento que el usuario seleccione
        """

        estudiantes = []
        profesores = []
        while True:

            nombre_curso = input("Introduzca el nombre del curso (No vacio): ")

            if nombre_curso != "":

                break
            else:
                nombre_curso = input("Nombre no válido, ingréselo nuevamente: ")

        
        print("La lista de estudiantes hasta el momento es")

        for indice,estudiante in enumerate(self.estudiantes):
            print(f"{indice}: {estudiante.get_nombre}")

            
        while len(estudiantes) < len(self.estudiantes):

            num_estudiante = input("Seleccione el número del estudiante que estará en el curso, ingrese FIN para terminar: ")
            if num_estudiante == "FIN":
                break
             
            try:
                indice = int(num_estudiante)
                if self.estudiantes[indice] not in estudiantes:

                    estudiantes.append(self.estudiantes[indice])

                    self.estudiantes[indice].cursos.append(nombre_curso)
                else:
                     num_estudiante = input("El estudiante ya se encuentra en el curso, seleccione otro")

                

            except (ValueError,IndexError,TypeError):
                    print("Ingrese un número valido: ")

        print("La lista de profesores hasta el momento es:")

        for indice,profesor in enumerate(self.profesores):
            print(f"{indice}:{profesor.get_nombre}")
            
        while True:

            num_profesor = input("Ingrese el número del profesor a seleccionar, el primero que ingrese será el que estará a cargo del curso: ").strip()

            if len(profesores) == len(self.profesores):
                print("No hay más profesores para añadir, continue con la creación del departamento.")
                break
            elif num_profesor == "FIN":
                break

            try:
                profesor = self.profesores[int(num_profesor)]
                if  profesor not in profesores:
                    

                    profesores.append(self.profesores[int(num_profesor)])
                    profesor.cursos.append(nombre_curso)

                else:
                    print("El profesor ya se encuentra añadido, por favor seleccione otro.")
            except (IndexError,TypeError,ValueError):
                print("El número ingresado no corresponde a ningún profesor o no es valido, por favor ingrese uno correctamente")

        """
        Se asigna el cargo de director al primer profesor añadido
        """
        director = profesores[0]
        director.cargos = nombre_curso

        curso_nuevo = Curso(nombre_curso,profesores,estudiantes,director)

    def crear_departamento (self):
            
        """
        Se crea un departamento académico con todos los elementos que contiene, 
        la creación es interactiva con el usuario que lo crea.
        """

        profesores_departamento = []
        cursos = []


        nombre_departamento = input("Ingrese el nombre del departamento académico: ")
            
        print("Los profesores disponibles para el departamento son:")
        for indice,profesor in enumerate(self.profesores):
            print(f"{indice}:{profesor.nombre}")
            

        print("Ingrese primero el número del profesor que será director, posteriormente ingrese los demás profesores que integren el departamento,escriba FIN para terminar la seleccion")
        while True:

            num_profesor = input("Ingrese el número del profesor: ").strip()

            if len(profesores_departamento) == len(self.profesores):
                print("No hay más profesores para añadir, continue con la creación del departamento.")
                break
            if num_profesor == "FIN":
                break
            try:
                profesor = self.profesores[int(num_profesor)]
                if  profesor not in profesores_departamento:

                    profesores_departamento.append(self.profesores[int(num_profesor)])
                    profesor.departamento.append(nombre_departamento)

                else:
                    print("El profesor ya se encuentra añadido, por favor seleccione otro.")
            except (IndexError,TypeError,ValueError):
                print("El número ingresado no corresponde a ningún profesor o no es valido, por favor ingrese uno correctamente")
                

        print("\nLos cursos ya existentes son: ")
        for indice,profesor in enumerate(self.profesores):
            print(f"{indice}:{profesor.nombre}")
                
        while True:
            
            numero_curso = input("\n Seleccione los cursos que se encontrarán en el departamento, si ya finalizo ingresen FIN")

            if numero_curso == "FIN" and cursos != []:
                break
            else:
                numero_curso = input("\nDebe de haber almenos 1 curso, porfavor ingrese 0 o 1")

            if len(cursos) == len(self.cursos):
                    print("Ya añadió la cantidad máxima de cursos, siga con la creación del departamento")
                    break
            
            try:
                int(numero_curso)

                try:
                    
                    curso = self.cursos[int(numero_curso)]
                    if curso not in cursos:
                            
                        cursos.append(curso)

                        print(f"¡¡Se ha añadido el curso {self.cursos[int(numero_curso)].nombre_curso} correctamente!!")
                    else:
                        num_curso = input("El curso ya se encuentra en el departamento, por favor ingrese otro: ")

                except (IndexError):
                        num_curso = input("Ingrese un número que corresponda a un curso: ")


            except ValueError:

                numero_curso = input("Ingrese un número válido de curso: ")

        nuevo_departamento = Departamento(nombre_departamento,cursos,profesores_departamento)

        self.departamentos_academicos.append(nuevo_departamento)

        return nuevo_departamento
    

if __name__ == "__main__":

    fac1 = Facultad("fiuner","oro verde")
    prof2 = Profesor("María", 789, ["física general", "termodinámica"],["Fisico Química"], ["FIQ", "FCE"])
    fac1.contratar_profesor(prof2)
    prof3 = Profesor("Carlos", 321, ["biología molecular", "genética"],["Fisico Química"], ["FCByF"])
    fac1.contratar_profesor(prof3)
    prof4 = Profesor("Ana", 655, ["química orgánica", "química analítica"],["Fisico Química"], ["FIQ", "FIQUI"])
    fac1.contratar_profesor(prof4)

    

    fac1.crear_departamento()
    