from modules.comunidad_academica import Profesor, Estudiante
from modules.departamento import Departamento
from modules.curso import Curso

class Facultad:
    def __init__(self, Nombre:str , Direccion:str, departamentos_académicos:list[object:Departamento]):

        """
        La clase facultad describirá el nombre, dirección y número de contacto, asi como la lista de estudiantes, profesores, departamentos y cursos que se brinden en la misma

        """
        self.Nombre = Nombre

        self.Direccion = Direccion
        
        self.departamentos_academicos = departamentos_académicos
        
        self.estudiantes = [estudiante for dpto in self.departamentos_academicos for curso in dpto.cursos for estudiante in curso.estudiantes_curso]
        
        self.profesores = [profesor for dpto in self.departamentos_academicos for profesor in dpto.profesores_departamento]

        self.cursos = [curso for dpto in self.departamentos_academicos for curso in dpto.cursos]


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
        p_profesor.facultades.append(self)
        print(f"¡El profesor {p_profesor.nombre} ha sido contratado correctamente!")

    def agregar_estudiante_a_curso(self):

        """
        Se añade un estudiante al curso que seleccione el usuario
        """


        print("La lista de estudiantes hasta el momento es")
        for indice,estudiante in enumerate(self.estudiantes):
            print(f"{indice}: {estudiante.nombre}")

        while True:
            indice_estudiante = input("Numero estudiante: ")
            try:
                estudiante_seleccionado = self.estudiantes[int(indice_estudiante)]
                break
            except(ValueError,IndexError):
                print("Ingrese nuevamente el número del estudiante, verifique que sea correcto")


        print("Los cursos que se brindan en la facultad son:")

        for indice,curso in enumerate(self.cursos):
            print(f"{indice}: {curso.nombre_curso}")

        while True:
            num_curso = input("Numero curso: ")
            try:
                curso = self.cursos[indice]
                if estudiante_seleccionado not in curso.estudiantes_curso:
                    curso.agregar_estudiante(estudiante_seleccionado) #se añade al curso el estudiante
                    estudiante_seleccionado.cursos.append(curso)

                    print(f"¡¡Se ha añadido correctamente el estudiante {estudiante_seleccionado.nombre} al curso {curso.nombre_curso}!!")
                    break
                else:
                    print("El estudiante ya se encuentra en el curso")
                    break
            except (ValueError,IndexError):
                print("Ingrese un número valido: ")
     
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
                print("Nombre no válido, ingréselo nuevamente")
                

        print("Seleccione el departamento en el cual se encontrará el curso ")
        for indice,departamento in enumerate(self.departamentos_academicos):
            print(f"{indice}:{departamento.nombre_departamento}")

        while True:
            num_departamento = input("Ingrese el número del departamento: ")

            try:
                int(num_departamento)
                dep_academico = self.departamentos_academicos[int(num_departamento)]
                break

            except (ValueError,IndexError):
                print("Ingrese un número válido o que corresponda al departamente seleccionado")
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


                curso_nuevo = Curso(nombre_curso,profesores,estudiantes,profesores[0])

                profesores[0].titular = curso_nuevo

                self.agregar_curso(curso=curso_nuevo)

                dep_academico.agregar_curso(curso_nuevo)

                print(f"¡Se ha creado el curso {curso_nuevo.nombre_curso} correctamente!")

                print(f"Los cursos que se dictarán ahora en el departamento {dep_academico.nombre_departamento} son :")
                for p_curso in dep_academico.mostrar_cursos():

                    print(p_curso)
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

                            profesores[0].titular = curso_nuevo.nombre_curso

                            estudiantes.curso.extend(curso_nuevo.estudiantes_curso)

                            profesor.curso.extend(curso_nuevo.profesores_curso)

                            self.agregar_curso(curso=curso_nuevo)
                            print(f"¡Se ha creado el curso {curso_nuevo.nombre_curso} correctamente!")

                            print(f"Los cursos que se dictarán ahora en el departamento {dep_academico.nombre_departamento} son :")
                            for p_curso in dep_academico.mostrar_cursos():

                                print(p_curso)
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
                    

        print("\nLos cursos ya existentes son: ")
        for indice,curso in enumerate(self.cursos):
            print(f"{indice}:{curso.nombre_curso}")

        print("\n Seleccione los cursos que se encontrarán en el departamento, si ya finalizo ingresen FIN: ")

        while True:
            
            numero_curso = input("Número de curso (FIN para terminar): ")

            if numero_curso.upper() == "FIN" and cursos:
                break
            elif numero_curso.upper() == "FIN" and cursos == []:
                print("Debe agregar al menos un curso en el departamento, ingrese nuevamente el número.")
                continue
            try:
                
                curso = self.cursos[int(numero_curso)]

                if curso not in cursos:
                    
                    cursos.append(curso)
                    profesores_departamento.extend(curso.profesores_curso) #se añaden los profesores del curso al departamento

                    if len(cursos) == len(self.cursos):

                        print("Ya añadió la cantidad máxima de cursos.")
                        break

                else:
                    print("El curso ya se encuentra en el departamento, por favor ingrese otro.")

            
            except (ValueError,IndexError):
                print("EL número ingresado no es válido o no corresponde a ningun curso")


        print("Los profesores que por ahora integran el departamento son: ")

        for profesor in profesores_departamento:
            print(f"{profesor.nombre}")

        print("\nLos profesores que no se encuentran en este departamento son: ")

        for indice,profesor in enumerate(self.profesores):
            if profesor not in profesores_departamento:
                print(f"{indice}:{profesor.nombre}")

        print("\nSi desea añadir algún profesor más al departamento, ingrese el número que le corresponde, sino ingrese FIN.")
        while True:

            num_profesor = input("Numero Profesor: ").strip()

            if num_profesor == "FIN":
                break
            try:
                profesor = self.profesores[int(num_profesor)]

                if len(profesores_departamento) == len(self.profesores):
                    print("No hay más profesores para añadir")
                    break

                if profesor not in profesores_departamento:
                    profesores_departamento.append(self.profesores[int(num_profesor)])

                else:
                    print("El profesor ya se encuentra añadido, por favor seleccione otro.")
            except (IndexError,TypeError,ValueError):
                print("El número ingresado no corresponde a ningún profesor o no es valido, por favor ingrese uno correctamente")


        print("Por último seleccione quien será el director del departamento")
        
        for indice,profesor in enumerate(profesores_departamento):
            print(f"{indice}:{profesor.nombre}")

        while True:
            num_director = input("Número Director: ")
            try:
                
                director = profesores_departamento[int(num_director)]
                director.director_departamento = nombre_departamento

                nuevo_departamento = Departamento(nombre=nombre_departamento, lista_cursos= [curso for curso in cursos], lista_profesores=[profesor for profesor in profesores_departamento],director=director)
                
                self.departamentos_academicos.append(nuevo_departamento)
                
                print(f"Se ha creado correctamente el departamento {nombre_departamento}.")

                break
            except(ValueError,IndexError):
                print("Ingrese un número válido que corresponda a un profesor")



if __name__ == "__main__":

    """
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
""" 
    