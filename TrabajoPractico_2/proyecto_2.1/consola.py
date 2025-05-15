from modules.comunidad_academica import Profesor, Estudiante
from modules.facultad import Facultad
from modules.curso import Curso
from modules.departamento import Departamento
from modules.archivos import leer_archivo_txt
import sys


RUTA_estudiantes = "TrabajoPractico_2/proyecto_2.1/data/Estudiantes.txt"

RUTA_profesores =  "TrabajoPractico_2/proyecto_2.1/data/Profesores.txt"
#Se define una facultad por defecto con algunos estudiantes y profesores, ademas de 1 curso y departamento

informacion_estudiantes = leer_archivo_txt(RUTA_estudiantes)

informacion_profesores = leer_archivo_txt(RUTA_profesores)

lista_estudiantes = []
lista_profesores = []

for estudiante in informacion_estudiantes:

    estudiante = Estudiante(nombre=estudiante[0],dni=estudiante[1])

    lista_estudiantes.append(estudiante)

for profesor in informacion_profesores:

    profesor = Profesor(nombre = profesor[0],dni = profesor[1],curso=[],departamentos=[],facultades=[])

    lista_profesores.append(profesor)

curso_programacion = Curso("programacion",[lista_profesores[2],lista_profesores[0]],estudiantes_curso= [lista_estudiantes[1],lista_estudiantes[2]],titular=lista_profesores[2])

departamento = Departamento("Computación",lista_cursos=[curso_programacion],lista_profesores=lista_profesores,director=lista_profesores[0])

fac_ejemplo = Facultad("FIUNER","OROVERDE",departamentos_académicos=[departamento])

print("##########################################\n#  Sistema de Información Universitaria  #\n##########################################")

while True:
    

    print(
        \
        "1 - Inscribir alumno\n" \
        "2 - Contratar profesor\n" \
        "3 - Crear departamento nuevo\n" \
        "4 - Crear curso nuevo\n" \
        "5 - Inscribir estudiante a un curso\n" \
        "6 - Salir\n"
    )

    opcion_usuario = input("Ingrese una opción: ")


    try:
        int(opcion_usuario)
        if int(opcion_usuario) == 1:
            while True:
                
                nombre_estudiante = input("Indique el nombre del alumno(en caso de querer cancelar seleccione 'FIN'): ")

                if nombre_estudiante == "FIN":
                    
                    sys.exit("Se ha cancelado la inscripción del estudiante. Por favor reinicie el programa.")

                dni = input("Indique el DNI: ")

                try:
                    int(dni)
                    
                    estudiante = Estudiante(nombre=nombre_estudiante,dni=dni)

                    fac_ejemplo.añadir_estudiantes(estudiante)

                    print(f"El estudiante {nombre_estudiante} ha sido añadido a la facultad {fac_ejemplo.nombre}")
                    break

                except ValueError:
                    print("Ingrese nuevamente los datos del estudiante, verifique que el dni sea un número.")

        elif int(opcion_usuario) == 2:

            while True:

                nombre_profesor = input("Indique el nombre del profesor(si quiere cancelar la accion introduzca 'FIN'): ")

                if nombre_profesor == "FIN":
                
                    sys.exit("Se ha cancelado la creación del departamento académico. Porfavor reinicie el programa.")

                dni_profesor = input ("Indique el DNI del profesor: ")

                print("Los departamentos disponibles hasta la fecha son")
                for indice,departamento in enumerate(fac_ejemplo.listar_departamentos):

                    print(f"{indice}:{departamento.nombre_departamento}")

                num_departamento = input("Seleccione el departamento académico al cual se agregará el profesor: ")
                
                try:
                    int(dni_profesor)
                    int(num_departamento)

                    print("Los cursos que están  disponibles en el departamento son")

                    for indice,curso in enumerate(fac_ejemplo.listar_departamentos[int(num_departamento)].listar_cursos):
                    
                        print(f"{indice}:{curso.nombre_curso}")

                    curso_seleccionado = input("Ingrese el número del curso en el cual el profesor dará clases(para cancelar introduzca 'FIN'): ")
                    
                    if curso_seleccionado == "FIN":
                
                        sys.exit("Se ha cancelado la agregacion del profesor al sistema. Porfavor reinicie el programa.")
                
                    try:
                        int(curso_seleccionado)

                        profesor = Profesor(nombre=nombre_profesor , dni=dni_profesor , curso = [curso_seleccionado], departamentos= [fac_ejemplo.listar_departamentos[int(num_departamento)]],facultades=[fac_ejemplo])

                        fac_ejemplo.contratar_profesor(profesor)

                        break
                    except (ValueError,IndexError):

                        print("Ingrese nuevamente los datos, verifique que el curso seleccionado sea un número y corresponda a algún curso")

                except (ValueError,IndexError):
                    print("Ingrese nuevamente los datos, verifique el dni sea un número y que el curso seleccionado sea correcto: ")

        elif int(opcion_usuario) == 3:

                        
            """
            Se crea un departamento académico con todos los elementos que contiene, 
            la creación es interactiva con el usuario que lo crea.
            """

            profesores_departamento = []
            cursos = []


            nombre_departamento = input("Ingrese el nombre del departamento académico(En caso de cancelar seleccione 'FIN') : " )
                
            if nombre_departamento == "FIN":
                    
                sys.exit("Se ha cancelado la creación del departamento académico. Porfavor reinicie el programa.")
                    
            print("\nLos cursos ya existentes son: ")
            for indice,curso in enumerate(fac_ejemplo.listar_cursos):
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
                    if numero_curso == "FIN":
                    
                        sys.exit("Se ha cancelado la creación del departamento académico. Porfavor reinicie el programa.")
                
                    curso = fac_ejemplo.listar_cursos[int(numero_curso)]

                    if curso not in cursos:
                        
                        cursos.append(curso)
                        profesores_departamento.extend(curso.listar_profesores) #se añaden los profesores del curso al departamento

                        if len(cursos) == len(fac_ejemplo.listar_cursos):

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

            for indice,profesor in enumerate(fac_ejemplo.listar_profesores):
                if profesor not in profesores_departamento:
                    print(f"{indice}:{profesor.nombre}")

            print("\nSi desea añadir algún profesor más al departamento, ingrese el número que le corresponde, sino ingrese FIN.")
            while True:

                num_profesor = input("Numero Profesor: ").strip()

                if num_profesor == "FIN":
                    break
                try:
                    profesor = fac_ejemplo.listar_profesores[int(num_profesor)]

                    if len(profesores_departamento) == len(fac_ejemplo.listar_profesores):
                        print("No hay más profesores para añadir")
                        break

                    if profesor not in profesores_departamento:
                        profesores_departamento.append(fac_ejemplo.listar_profesores[int(num_profesor)])

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
                    
                    director_dpto = profesores_departamento[int(num_director)]
                    director_dpto.director = nombre_departamento

                    nuevo_departamento = Departamento(nombre=nombre_departamento, lista_cursos= [curso for curso in cursos], lista_profesores=[profesor for profesor in profesores_departamento],director=director_dpto)
                    
                    fac_ejemplo.agregar_departamento(nuevo_departamento)
                    
                    print(f"Se ha creado correctamente el departamento {nombre_departamento}.")
                    print("Departamentos hasta el momento: ")

                    for depto_academico in fac_ejemplo.listar_departamentos:
                        print(depto_academico.nombre_departamento)

                    break
                except(ValueError,IndexError):
                    print("Ingrese un número válido que corresponda a un profesor")


                

        elif int(opcion_usuario) == 4:

            estudiantes = []
            profesores = []

            while True:

                nombre_curso = input("Introduzca el nombre del curso (No vacio): ")

                if nombre_curso != "":

                    break
                else:
                    print("Nombre no válido, ingréselo nuevamente")
                    

            print("Seleccione el departamento en el cual se encontrará el curso(Si quiere cancelar introduzca 'FIN'): ")
            for indice,departamento in enumerate(fac_ejemplo.listar_departamentos):
                print(f"{indice}:{departamento.nombre_departamento}")
                    
            while True:
                num_departamento = input("Ingrese el número del departamento: ")


                try:
                    if num_departamento == "FIN":
                    
                        sys.exit("Se ha cancelado la creación del departamento académico. Porfavor reinicie el programa.")        
                    else: 
                        
                        int(num_departamento)
                        dep_academico = fac_ejemplo.listar_departamentos[int(num_departamento)]
                        break

                except (ValueError,IndexError):
                    print("Ingrese un número válido o que corresponda al departamente seleccionado")
            print("La lista de estudiantes hasta el momento es:")

            for indice,estudiante in enumerate(fac_ejemplo.listar_estudiantes):
                print(f"{indice}: {estudiante.get_nombre}")

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
                    if fac_ejemplo.listar_estudiantes[indice] not in estudiantes:

                        estudiantes.append(fac_ejemplo.listar_estudiantes[indice])

                        if len(estudiantes) == len(fac_ejemplo.listar_estudiantes):
                            print("Ya se añadieron todos los estudiantes de la facultad al curso, continue con la creación.")
                            break
                    else:
                        print("El estudiante ya se encuentra en el curso, seleccione otro")

                except (ValueError,IndexError):
                        print("El número ingresado no corresponde a ningún estudiante o no es válido, ingrese otro.")


            print("La lista de profesores hasta el momento es:")

            for indice,profesor in enumerate(fac_ejemplo.listar_profesores):
                print(f"{indice}:{profesor.nombre}")

            print("Ingrese el número del profesor a seleccionar, el primero que ingrese será el que estará a cargo del curso.")
                
            while True:

                num_profesor = input("Número profesor(FIN para terminar): ").strip()
                
                if num_profesor == "FIN" and profesores:


                    curso_nuevo = Curso(nombre_curso,profesores,estudiantes,profesores[0])

                    profesores[0].titular = curso_nuevo

                    #Se actualizan los cursos de estudiantes y profesores

                    for estudiante in estudiantes: estudiante.cursos = curso_nuevo


                    # Se añaden los profesores del curso al departamento
                    dep_academico.listar_profesores.extend(curso_nuevo.listar_profesores)

                    fac_ejemplo.agregar_curso(curso=curso_nuevo)

                    dep_academico.listar_cursos = curso_nuevo

                    print(f"¡Se ha creado el curso {curso_nuevo.nombre_curso} correctamente!")

                    print(f"Los cursos que se dictarán ahora en el departamento {dep_academico.nombre_departamento} son :")
                    for p_curso in dep_academico.mostrar_cursos:

                        print(p_curso.nombre_curso)
                    break

                elif num_profesor == "FIN" and not profesores:
                    print("No se añadió ningún profesor al curso, agregue al menos uno.")
                    continue

                else:

                    try:

                        profesor = fac_ejemplo.listar_profesores[int(num_profesor)]

                        if  profesor not in profesores:
                            
                            profesores.append(fac_ejemplo.listar_profesores[int(num_profesor)])

                            if len(profesores) == len(fac_ejemplo.listar_profesores):
                                print("No hay más profesores para añadir.")

                                curso_nuevo = Curso(nombre_curso,profesores,estudiantes,profesores[0])

                                profesores[0].titular = curso_nuevo.nombre_curso

                                for estudiante in estudiantes: estudiante.cursos = curso_nuevo



                                dep_academico.agregar_curso(curso_nuevo)
                                
                                for profesor in curso_nuevo.profesores_curso: dep_academico.listar_profesores = profesor

                                fac_ejemplo.agregar_curso(curso=curso_nuevo)

                                print(f"¡Se ha creado el curso {curso_nuevo.nombre_curso} correctamente!")

                                print(f"Los cursos que se dictarán ahora en el departamento {dep_academico.nombre_departamento} son :")
                                for p_curso in dep_academico.mostrar_cursos():

                                    print(p_curso)
                                break

                        else:
                            print("El profesor ya se encuentra añadido, por favor seleccione otro.")
                    except (IndexError,ValueError):
                        print("El número ingresado no corresponde a ningún profesor o no es valido , por favor ingrese uno correctamente")
            
        elif int(opcion_usuario) == 5:

            print("La lista de estudiantes hasta el momento es")
            for indice,estudiante in enumerate(fac_ejemplo.listar_estudiantes):
                print(f"{indice}: {estudiante.get_nombre}")

            while True:
                indice_estudiante = input("Numero estudiante: ")
                try:
                    estudiante_seleccionado = fac_ejemplo.listar_estudiantes[int(indice_estudiante)]
                    break
                except(ValueError,IndexError):
                    print("Ingrese nuevamente el número del estudiante, verifique que sea correcto")


            print("Los cursos que se brindan en la facultad son(si quiere cancelar ingrese 'FIN'):")

            for indice,curso in enumerate(fac_ejemplo.listar_cursos):
                print(f"{indice}: {curso.nombre_curso}")

            while True:
                num_curso = input("Numero curso: ")
                try:
                    if num_curso == "FIN":
                    
                        sys.exit("Se ha cancelado la selección del curso. Porfavor reinicie el programa.")
                    
                    else:
                    
                        curso = fac_ejemplo.listar_cursos[indice]
                        if estudiante_seleccionado not in curso.estudiantes:
                            curso.agregar_estudiante(estudiante_seleccionado) #se añade al curso el estudiante

                            fac_ejemplo.agregar_estudiante_a_curso(curso,estudiante_seleccionado)
                            print("Se ha añadido correctamente el estudiante al curso.")
                            break
                        else:
                            print("El estudiante ya se encuentra en el curso")
                            break
                except (ValueError,IndexError):
                    print("Ingrese un número valido")
        

        elif int(opcion_usuario) == 6:
            break

    except ValueError:
    
        print("Ingrese un número válido de opción: ")

#Atributos privados a todo el sistema