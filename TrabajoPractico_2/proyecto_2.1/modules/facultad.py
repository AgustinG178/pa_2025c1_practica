from modules.comunidad_academica import Profesor, Estudiante
from modules.departamento import Departamento
from modules.curso import Curso

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
            num_curso = input("Seleccione el número del estudiante que quiera asignar a un curso: ")
            try:

                indice = int(num_curso)
                curso = self.cursos[indice]
                break
            except (ValueError,IndexError):
                print("Ingrese un número valido: ")

        curso.estudiantes_curso.append(estudiante) #se añade al curso el estudiante

        print(f"¡¡Se ha añadido correctamente el estudiante {estudiante.nombre} al curso {curso.nombre_curso}!!")
        
    def agregar_curso(self,curso:object):

        if isinstance(curso,Curso):

            self.cursos.append(curso)
            print(f"Se ha añadido correctamente el curso: {curso.nombre_curso} a la facultad")
        
        else:
            raise TypeError("El curso debe ser un objeto")

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

        
        print("La lista de estudiantes hasta el momento es:")

        for indice,estudiante in enumerate(self.estudiantes):
            print(f"{indice}: {estudiante.nombre}")

        print("Ingrese los estudiantes que integren el curso, debe haber al menos un estudiante, escriba FIN para terminar la seleccion")

        while True:

            num_estudiante = input("Numero estudiante (FIN para terminar): ")

            if num_estudiante == "FIN" and estudiantes:
                break
             
            elif num_estudiante == "FIN" and not estudiantes:

                print("No se añadió ningún estudiante al curso, por favor agregue al menos uno.")
                continue

            try:
                indice = int(num_estudiante)
                if self.estudiantes[indice] not in estudiantes:

                    estudiantes.append(self.estudiantes[indice])

                    if len(estudiantes) == len(self.estudiantes):
                        print("Ya se añadieron todos los estudiantes de la facultad al curso, continue con la creación.")
                        break
                else:
                     print("El estudiante ya se encuentra en el curso, seleccione otro")

            except (ValueError,IndexError):
                    print("El número ingresado no corresponde a ningún estudiante o no es válido, ingrese otro.")


        print("La lista de profesores hasta el momento es:")

        for indice,profesor in enumerate(self.profesores):
            print(f"{indice}:{profesor.nombre}")

        print("Ingrese el número del profesor a seleccionar, el primero que ingrese será el que estará a cargo del curso.")
            
        while True:

            num_profesor = input("Número profesor(FIN para terminar): ").strip()
            
            if num_profesor == "FIN" and profesores:

                profesores[0].cargos = nombre_curso

                curso_nuevo = Curso(nombre_curso,profesores,estudiantes,profesores[0])

                for estudiante in estudiantes:

                    estudiante.cursos.append(curso_nuevo)
                for profesor in profesores:

                    profesor.cursos.append(curso_nuevo)

                self.agregar_curso(curso=curso_nuevo)

                print(f"¡Se ha creado el curso {curso_nuevo.nombre_curso} correctamente!")

                break

            elif num_profesor == "FIN" and not profesores:
                print("No se añadió ningún profesor al curso, agregue al menos uno.")
                continue

            else:

                try:

                    profesor = self.profesores[int(num_profesor)]

                    if  profesor not in profesores:
                        
                        profesores.append(self.profesores[int(num_profesor)])

                        if len(profesores) == len(self.profesores):
                            print("No hay más profesores para añadir.")

                            curso_nuevo = Curso(nombre_curso,profesores,estudiantes,profesores[0])

                            profesores[0].cargos = curso_nuevo

                            for estudiante in estudiantes:

                                estudiante.curso.append(curso_nuevo)

                            for profesor in profesores:

                                profesor.curso.append(curso_nuevo)

                            self.agregar_curso(curso=curso_nuevo)
                            print(f"¡Se ha creado el curso {curso_nuevo.nombre_curso} correctamente!")
                            break

                    else:
                        print("El profesor ya se encuentra añadido, por favor seleccione otro.")
                except (IndexError,ValueError):
                    print("El número ingresado no corresponde a ningún profesor o no es valido , por favor ingrese uno correctamente")
       
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
            

        print("Ingrese los profesores que integren el departamento,escriba FIN para terminar la seleccion")
        while True:

            num_profesor = input("Numero Profesor: ").strip()

            
            if num_profesor == "FIN":
                break
            try:
                profesor = self.profesores[int(num_profesor)]
                if  profesor not in profesores_departamento:

                    profesores_departamento.append(self.profesores[int(num_profesor)])


                    if len(profesores_departamento) == len(self.profesores):
                        print("No hay más profesores para añadir, continue con la creación del departamento.")
                        break

                else:
                    print("El profesor ya se encuentra añadido, por favor seleccione otro.")
            except (IndexError,TypeError,ValueError):
                print("El número ingresado no corresponde a ningún profesor o no es valido, por favor ingrese uno correctamente")
                

        print("\nLos cursos ya existentes son: ")
        for indice,curso in enumerate(self.cursos):
            print(f"{indice}:{curso.nombre_curso}")

        print("\n Seleccione los cursos que se encontrarán en el departamento, si ya finalizo ingresen FIN: ")

        while True:
            
            numero_curso = input("Número de curso (FIN para terminar): ")

            if numero_curso == "FIN" and cursos != []:
                nuevo_departamento = Departamento(nombre_departamento,cursos,profesores_departamento,director=profesores_departamento[0])

                self.departamentos_academicos.append(nuevo_departamento)

                for profesor in profesores_departamento:
                    
                    profesor.departamento.append(nuevo_departamento)
                
                print(f"¡Se ha creado el departamento {nuevo_departamento.nombre_departamento} correctamente!")
                break
                
            try:
                    
                    curso = self.cursos[int(numero_curso)]
                    if curso not in cursos:
                            
                        cursos.append(curso)

                        print(f"¡¡Se ha añadido el curso {self.cursos[int(numero_curso)].nombre_curso} al departamento!!")

                        if len(cursos) == len(self.cursos):

                            print("Ya añadió la cantidad máxima de cursos.")

                            nuevo_departamento = Departamento(nombre_departamento,cursos,profesores_departamento,director=profesores_departamento[0])

                            self.departamentos_academicos.append(nuevo_departamento)


                            print(f"¡Se ha creado el departamento {nuevo_departamento.nombre_departamento} correctamente!")

                            break

                        
                    else:
                        print("El curso ya se encuentra en el departamento, por favor ingrese otro.")
            except (ValueError,IndexError):
                print("EL número ingresado no es válido o no corresponde a ningun curso")


if __name__ == "__main__":

    
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
