

class  Departamento:
    def __init__(self,nombre:str,lista_cursos:list[object], lista_profesores:list[object], director:object):
        """
        Se crea un departamento académico dentro de una facultad.
        La clase recibe como parámetro el nombre del departamento, el director que le corresponde,
        los profesores que dan clases y los cursos que se dictan en este.
        """
        self.__nombre_departamento = nombre

        self.__cursos = lista_cursos

        self.__profesores_departamento = lista_profesores 

        self.__director = [director]

        
    @property
    def nombre_departamento(self):
        return self.__nombre_departamento
    
   
    @property
    
    def listar_cursos(self):
        
        """
        Se muestran todos los cursos que existen en el departamento hasta el momento.
        """
        return [curso for curso in self.__cursos]
    @listar_cursos.setter
    
    def listar_cursos(self,p_curso):
        from modules.curso import Curso
        if isinstance(p_curso,Curso):
            self.__cursos.append(p_curso)
    @property
    def listar_profesores (self):
        from modules.comunidad_academica import Profesor
        """
        Se muestran todos los profesores que dan clases en el departamento hasta el momento.
        """
        return [profesor for profesor in self.__profesores_departamento]
    
    @listar_profesores.setter

    def listar_profesores (self,p_profesor):
        if p_profesor not in self.__profesores_departamento:
         
         self.__profesores_departamento.append(p_profesor)
    @property
    def director(self):
        """
        Se muestra el director del departamento
        """
        return self.__director[0]
    
    @director.setter
    def director(self,director_p):
        self.__director[0] == director_p
    
    @property

    @property
    def mostrar_cursos(self):
        return[curso for curso in self.__cursos]





