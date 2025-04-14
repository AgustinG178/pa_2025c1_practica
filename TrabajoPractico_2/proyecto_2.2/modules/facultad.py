class Facultad:
    def __init__(self, Nombre:str , Direccion:str , Num_contacto:int, estudiantes:list[object], profesores:list[object], departamentos:list[object]):

        """
        La clase facultad describirá el nombre, dirección y número de contacto, asi como la lista de estudiantes

        """
        self.Nombre = Nombre

        self.Direccion = Direccion
        
        self.Num_contacto = Num_contacto

        self.estudiantes = estudiantes

        self.profesores = profesores

        def listar_estudiantes ():
            """
            Se muestran todos los estudiantes inscriptos en la facultad hasta el momento.
            """

            for estudiante in estudiantes:
                    print(estudiante.Nombre)
        
        def listar_profesores ():

            """
            Se muestran todos los profesores contratados por la facultad hasta el momento.
            """

            for profesor in profesores:
                    print(profesor.Nombre)
        
        def listar_departamentos():
             
             """
            Se muestran todos los departamentos académicos que existen en la facultad hasta el momento.
             """

             for departamento in departamentos:
                  print(departamento.Nombre)

        def añadir_estudiante(self, estudiante:object):
            """
            Se añade a la facultad un estudiante que debe ser un objeto
            """
            if type(estudiante) == object:

                estudiantes.append(estudiante)
                print(f"¡El estudiante {estudiante.Nombre} ha sido inscripto correctamente!")

            else: raise TypeError("El estudiante debe ser la instancia de una clase (objeto)")

        def contratar_profesor(profesor:object):
            """
            Se añade a la facultad un estudiante que debe ser un objeto
            """
            if type(profesor) == object:

                profesores.append(profesor)
                print(f"¡El profesor {profesor.Nombre} ha sido contratado correctamente!")

            else: raise TypeError("El profesor debe ser la instancia de una clase (objeto)")

        def crear_departamento (nombre_departamento:str,cursos:list, profesores_departamento: list, director:object):
             
             """
             Se crea un departamento académico, la función debe recibir el nombre de este y el director que le corresponde, además de los cursos
             que se dictan y los profesores que componen el departamento.
             """

             

