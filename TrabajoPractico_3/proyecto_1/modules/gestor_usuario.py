from modules.usuarios import Usuario
from modules.repositorio import RepositorioUsuariosSQLAlchemy
from modules.reportes import Reportes
class GestorUsuarios:
    def __init__(self, repositorio_usuarios:RepositorioUsuariosSQLAlchemy):
        """
        Inicializa el gestor de usuarios con el repositorio proporcionado.
        """
        self.__repositorio_usuarios = repositorio_usuarios

        """
        Intermediario entre el usuario y la base de datos, consiste de métodos para registrar, autenticar, cargar, actualizar, eliminar y buscar usuarios.
        """


    def registrar_nuevo_usuario(self, nombre, apellido, email, nombre_de_usuario, password, rol, claustro):
        if self.__repositorio_usuarios.obtener_registro_por_filtros(mapeo=True,**{"email":email}):
            raise ValueError("El usuario ya está registrado, por favor inicie sesión")
        usuario = Usuario(nombre, apellido, email, nombre_de_usuario, password, rol, claustro)
        print("[DEBUG] registrar usuarios")
        
        modelo_usuario = self.__repositorio_usuarios.map_entidad_a_modelo(usuario) 
        modelo_usuario.nombre
        self.__repositorio_usuarios.guardar_registro(modelo_usuario)


    def actualizar_usuario(self, usuario_modificado:Usuario):

        """
        Actualiza los datos de un usuario existente en la base de datos.
        Lanza ValueError si el usuario no tiene id.
        """
        if not hasattr(usuario_modificado, "id"):
            raise ValueError("El usuario modificado debe tener un id")
        
        #Se mapea el usuario modificado a uno del modelo de la base de datos
        self.__repositorio_usuarios.modificar_registro(self.__repositorio_usuarios.map_entidad_a_modelo(usuario_modificado))

    def eliminar_usuario(self, usuario_id):
        """
        Elimina un usuario de la base de datos por su id.
        Lanza ValueError si el usuario no existe.
        """
        usuario = self.__repositorio_usuarios.obtener_registro_por_filtros(**{id:usuario_id})
        if not usuario:
            raise ValueError("Usuario no encontrado")
        self.__repositorio_usuarios.eliminar_registro_por_id(usuario_id)

    def buscar_usuario(self, filtro, valor,mapeo=True):
        """
        Busca un usuario por un filtro y valor dados.
        Lanza ValueError si el usuario no existe.
        """
        usuario = self.__repositorio_usuarios.obtener_registro_por_filtros(mapeo=mapeo,**{f"{filtro}":valor})
        if not usuario:
            raise ValueError("Usuario no encontrado")
        return usuario

    def generar_reporte_usuario(self, tipo_reporte, ruta_salida,clasificacion_usuario,reporte:Reportes):
        """
        Genera un reporte de usuarios en el formato especificado (pdf o html).
        Lanza ValueError si el tipo de reporte no es soportado.
        """
        try:

            if tipo_reporte == "pdf":
                reporte.generar(ruta_salida=ruta_salida,clasificacion_usuario=clasificacion_usuario)
                return "Reporte PDF generado para usuarios"

            elif tipo_reporte == "html":
                reporte.generar(ruta_salida=ruta_salida,clasificacion_usuario=clasificacion_usuario)
                return "Reporte HTML generado para usuarios"
            else:
                raise ValueError("Tipo de reporte no soportado. Use 'pdf' o 'html'.")
        except Exception as e:
            raise Exception(f"Error {e} al generar el reporte.")

