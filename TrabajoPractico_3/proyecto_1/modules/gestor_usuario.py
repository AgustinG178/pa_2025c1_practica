from modules.usuarios import Usuario
from modules.repositorio import RepositorioUsuariosSQLAlchemy
from modules.BaseDeDatos import BaseDatos

class GestorUsuarios:
    def __init__(self, repositorio_usuario: RepositorioUsuariosSQLAlchemy):
        self.repositorio = repositorio_usuario

    """
    Intermediario entre el usuario y la base de datos, consiste de métodos para registrar, autenticar, cargar, actualizar, eliminar y buscar usuarios.
    """

    def registrar_nuevo_usuario(self, nombre, apellido, email, nombre_de_usuario, password, rol, claustro, id):
        if self.repositorio.obtener_registro_por_filtro("email", email):
            raise ValueError("El usuario ya está registrado, por favor inicie sesión")
        usuario = Usuario(nombre, apellido, email, nombre_de_usuario, password, rol, claustro, id)
        self.repositorio.guardar_registro(usuario)

    def autenticar_usuario(self, nombre_de_usuario, password):
        usuario = self.repositorio.obtener_registro_por_filtro("nombre_de_usuario", nombre_de_usuario, "contraseña", password)
        if not usuario:
            raise ValueError("El usuario no está registrado")
        if usuario.contraseña != password:
            raise ValueError("Contraseña incorrecta")
        return usuario.__dict__ 
        
    def cargar_usuario(self, nombre_de_usuario):
        usuario = self.repositorio.obtener_registro_por_filtro("nombre_de_usuario", nombre_de_usuario)
        if usuario:
            return usuario.__dict__
        else:
            raise ValueError("Usuario no encontrado")

    def actualizar_usuario(self, usuario_modificado):
        if not hasattr(usuario_modificado, "id"):
            raise ValueError("El usuario modificado debe tener un id")
        self.repositorio.modificar_registro(usuario_modificado)

    def eliminar_usuario(self, usuario_id):
        usuario = self.repositorio.obtener_registro_por_filtro("id", usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        self.repositorio.eliminar_registro_por_id(usuario_id)

    def buscar_usuario(self, filtro, valor):
        usuario = self.repositorio.obtener_registro_por_filtro(filtro, valor)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        return usuario.__str__()

    def generar_reporte_usuario(self, tipo_reporte, *args, **kwargs):

        if tipo_reporte == "pdf":
            return "Reporte PDF generado para usuarios"
        elif tipo_reporte == "html":
            return "Reporte HTML generado para usuarios"
        else:
            raise ValueError("Tipo de reporte no soportado")
        
if __name__ == "__main__":
    session = BaseDatos("sqlite:///data/base_datos.db")
    session.conectar()
    repo = RepositorioUsuariosSQLAlchemy(session=session.session)
    gestor = GestorUsuarios(repo)

    nombre_usuario = "tupapacitoXD_123"

    # #Intentamos registrar el usuario si no existe
    # """Registrar Usuario anda correctamente"""
    # try:
    #     gestor.registrar_nuevo_usuario(
    #         nombre="nicolas",
    #         apellido="ramirez",
    #         email="ramiresn@gmail.com",
    #         nombre_de_usuario=nombre_usuario,
    #         password="1234",
    #         rol=0,
    #         claustro="estudiante"
    #     )
    #     print("Usuario registrado correctamente")
    # except Exception as e:
    #     print(f"No se registró nuevo usuario (probablemente ya existe): {e}")

    # #Ahora probamos cargar_usuario
    # """Cargar Usuario anda correctamente"""
    # try:
    #     usuario = gestor.cargar_usuario(nombre_usuario)
    #     print("Usuario cargado correctamente:")
    #     print(usuario)
    # except Exception as e:
    #     print(f"Error al cargar usuario: {e}")
    #Intentamos autenticar al usuario
    """Autenticar Usuario anda correctamente"""
    try:
        usuario_autenticado = gestor.autenticar_usuario(nombre_usuario, "1234")
        print("Usuario autenticado correctamente:")
        print(usuario_autenticado)
    except Exception as e:
        print(f"Error al autenticar usuario: {e}")
    # #Intentamos actualizar el usuario
    # try:
    #     usuario_modificado = Usuario(
    #         id=usuario['id'],  # Asegúrate de que el ID esté presente
    #         nombre="nicolas",
    #         apellido="Ramírez",
    #         email="ramirezn@gmail.com",
    #         nombre_de_usuario=nombre_usuario,
    #         contraseña="1234",
    #         rol=0,
    #         claustro="estudiante"
    #     )
    #     gestor.actualizar_usuario(usuario_modificado)
    #     print("Usuario actualizado correctamente")
    # except Exception as e:
    #     print(f"Error al actualizar usuario: {e}")
        