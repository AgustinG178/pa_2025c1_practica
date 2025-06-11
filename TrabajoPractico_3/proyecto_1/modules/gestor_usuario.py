from modules.usuarios import Usuario
from modules.repositorio import RepositorioUsuariosSQLAlchemy
from modules.gestor_base_datos import GestorBaseDatos

class GestorUsuarios:
    def __init__(self, repositorio_usuario: RepositorioUsuariosSQLAlchemy):
        """
        Inicializa el gestor de usuarios con el repositorio proporcionado.
        """
        self.repositorio = repositorio_usuario

        """
        Intermediario entre el usuario y la base de datos, consiste de métodos para registrar, autenticar, cargar, actualizar, eliminar y buscar usuarios.
        """

    def registrar_nuevo_usuario(self, nombre, apellido, email, nombre_de_usuario, password, rol, claustro):
        if self.repositorio.obtener_registro_por_filtro("email", email):
            raise ValueError("El usuario ya está registrado, por favor inicie sesión")
        usuario = Usuario(nombre, apellido, email, nombre_de_usuario, password, rol, claustro)
        modelo_usuario = self.repositorio._map_entidad_a_modelo(usuario) 
        self.repositorio.guardar_registro(modelo_usuario)


    def autenticar_usuario(self, nombre_de_usuario, password):
        """
        Autentica un usuario por nombre de usuario y contraseña.
        Lanza ValueError si el usuario no está registrado o la contraseña es incorrecta.
        """
        usuario = self.repositorio.obtener_registro_por_filtro("nombre_de_usuario", nombre_de_usuario, "contraseña", password)
        if not usuario:
            raise ValueError("El usuario no está registrado")
        if usuario.contraseña != password:
            raise ValueError("Contraseña incorrecta")
        return usuario
        
    def actualizar_usuario(self, usuario_modificado):

        """
        Actualiza los datos de un usuario existente en la base de datos.
        Lanza ValueError si el usuario no tiene id.
        """
        if not hasattr(usuario_modificado, "id"):
            raise ValueError("El usuario modificado debe tener un id")
        
        #Se mapea el usuario modificado a uno del modelo de la base de datos
        self.repositorio.modificar_registro(self.repositorio._map_entidad_a_modelo(usuario_modificado))

    def eliminar_usuario(self, usuario_id):
        """
        Elimina un usuario de la base de datos por su id.
        Lanza ValueError si el usuario no existe.
        """
        usuario = self.repositorio.obtener_registro_por_filtro("id", usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        self.repositorio.eliminar_registro_por_id(usuario_id)

    def buscar_usuario(self, filtro, valor):
        """
        Busca un usuario por un filtro y valor dados.
        Lanza ValueError si el usuario no existe.
        """
        usuario = self.repositorio.obtener_registro_por_filtro(filtro, valor)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        return usuario.__str__()

    def generar_reporte_usuario(self, tipo_reporte, *args, **kwargs):
        """
        Genera un reporte de usuarios en el formato especificado (pdf o html).
        Lanza ValueError si el tipo de reporte no es soportado.
        """
        if tipo_reporte == "pdf":
            return "Reporte PDF generado para usuarios"
        elif tipo_reporte == "html":
            return "Reporte HTML generado para usuarios"
        else:
            raise ValueError("Tipo de reporte no soportado")
        
    def cargar_usuario(self, nombre_de_usuario):
        """
        Carga un usuario por su nombre de usuario.
        Lanza ValueError si el usuario no existe.
        """
        usuario = self.repositorio.obtener_registro_por_filtro("nombre_de_usuario", nombre_de_usuario)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        return usuario
if __name__ == "__main__":
    session = BaseDatos("sqlite:///data/base_datos.db")
    session.conectar()
    repo = RepositorioUsuariosSQLAlchemy(session=session.session)
    gestor = GestorUsuarios(repo)

    nombre_usuario = "tupapacitoXD_123"

    #Intentamos registrar el usuario si no existe
    """Registrar Usuario anda correctamente"""
    try:
        gestor.registrar_nuevo_usuario(
            nombre="nicolas",
            apellido="ramirez",
            email="ramiresn@gmail.com",
            nombre_de_usuario=nombre_usuario,
            password="1234",
            rol=0,
            claustro="estudiante"
        )
        print("Usuario registrado correctamente")
    except Exception as e:
        print(f"No se registró nuevo usuario (probablemente ya existe): {e}")

    #Intentamos autenticar al usuario
    """Autenticar Usuario anda correctamente"""
    try:
        usuario_autenticado = gestor.autenticar_usuario(nombre_usuario, "1234")
        print("Usuario autenticado correctamente:")
        print(usuario_autenticado)
    except Exception as e:
        print(f"Error al autenticar usuario: {e}")
    #Intentamos actualizar el usuario
    try:
        usuario_modificado = Usuario(
            id=usuario['id'],  # Asegúrate de que el ID esté presente
            nombre="nicolas",
            apellido="Ramírez",
            email="ramirezn@gmail.com",
            nombre_de_usuario=nombre_usuario,
            contraseña="1234",
            rol=0,
            claustro="estudiante"
        )
        gestor.actualizar_usuario(usuario_modificado)
        print("Usuario actualizado correctamente")
    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
