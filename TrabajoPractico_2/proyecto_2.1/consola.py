from modules.comunidad_academica import Profesor, Estudiante
from modules.facultad import Facultad
from modules.curso import Curso
from modules.departamento import Departamento
from modules.archivos import leer_archivo_txt


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

    profesor = Profesor(nombre = profesor[0],dni = profesor[1],cursos=[],departamentos=[],facultades=[])

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
                
                nombre_estudiante = input("Indique el nombre del alumno: ")

                dni = input("Indique el DNI: ")


                try:
                    int(dni)
                    
                    estudiante = Estudiante(nombre=nombre_estudiante,dni=dni)

                    fac_ejemplo.añadir_estudiantes(estudiante)

                    print(f"El estudiante {nombre_estudiante} ha sido añadido a la facultad {fac_ejemplo.Nombre}")
                    break

                except ValueError:
                    print("Ingrese nuevamente los datos del estudiante, verifique que el dni sea un número.")

        elif int(opcion_usuario) == 2:

            while True:

                nombre_profesor = input("Indique el nombre del profesor: ")

                dni_profesor = input ("Indique el DNI del profesor: ")

                print("Los departamentos disponibles hasta la fecha son")
                for indice,departamento in enumerate(fac_ejemplo.departamentos_academicos):

                    print(f"{indice}:{departamento.nombre_departamento}")

                num_departamento = input("Seleccione el departamento académico al cual se agregará el profesor: ")

                
                try:
                    int(dni_profesor)
                    int(num_departamento)

                    print("Los cursos que están  disponibles en el departamento son")

                    for indice,curso in enumerate(fac_ejemplo.departamentos_academicos[int(num_departamento)].cursos):
                    
                        print(f"{indice}:{curso.nombre_curso}")

                    curso_seleccionado = input("Ingrese el número del curso en el cual el profesor dará clases: ")

                    try:
                        int(curso_seleccionado)

                        profesor = Profesor(nombre=nombre_profesor , dni=dni_profesor , cursos = [curso_seleccionado], departamentos= [fac_ejemplo.departamentos_academicos[int(num_departamento)]],facultades=[fac_ejemplo])

                        fac_ejemplo.contratar_profesor(profesor)

                    

                        break
                    except (ValueError,IndexError):

                        print("Ingrese nuevamente los datos, verifique que el curso seleccionado sea un número y corresponda a algún curso")

                except (ValueError,IndexError):
                    print("Ingrese nuevamente los datos, verifique el dni sea un número y que el curso seleccionado sea correcto: ")

        elif int(opcion_usuario) == 3:

            fac_ejemplo.crear_departamento()

            print("Departamentos hasta el momento: ")

            for depto_academico in fac_ejemplo.departamentos_academicos:
                print(depto_academico.nombre_departamento)

        elif int(opcion_usuario) == 4:

            fac_ejemplo.crear_curso()

        elif int(opcion_usuario) == 5:

            fac_ejemplo.agregar_estudiante_a_curso()

        elif int(opcion_usuario) == 6:
            break

    except ValueError:
    
        print("Ingrese un número válido de opción: ")


