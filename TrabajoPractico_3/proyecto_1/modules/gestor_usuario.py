from modules.usuarios import Usuario
from modules.repositorio import RepositorioAbstracto, RepositorioUsuariosSQLAlchemy
from modules.BaseDeDatos import BaseDatos

class GestorDeUsuarios:
    def __init__(self, repo: RepositorioUsuariosSQLAlchemy):
        self.__repo = repo  

    """
    Intermediario entre el usuario y la base de datos, consiste de métodos para registrar, autenticar, cargar, actualizar, eliminar y buscar usuarios.
    """

    def registrar_nuevo_usuario(self, nombre, apellido, email, nombre_de_usuario, password, rol, claustro):
        if self.__repo.obtener_registro_por_filtro("email", email):
            raise ValueError("El usuario ya está registrado, por favor inicie sesión")
        usuario = Usuario(nombre, apellido, email, nombre_de_usuario, password, rol, claustro)
        self.__repo.guardar_registro(usuario.map_to_modelo_bd())

    def autenticar_usuario(self, email, password):
        usuario = self.__repo.obtener_registro_por_filtro("email", email)
        if not usuario:
            raise ValueError("El usuario no está registrado")
        if usuario.contraseña != password:
            raise ValueError("Contraseña incorrecta")
        return usuario.__dict__ 
        
    def cargar_usuario(self, id_usuario):
        usuario = self.__repo.obtener_registro_por_filtro("id", id_usuario)
        if usuario:
            return usuario.to_dict()
        else:
            raise ValueError("Usuario no encontrado")

    def actualizar_usuario(self, usuario_modificado):
        if not hasattr(usuario_modificado, "id"):
            raise ValueError("El usuario modificado debe tener un id")
        self.__repo.modificar_registro(usuario_modificado)

    def eliminar_usuario(self, usuario_id):
        usuario = self.__repo.obtener_registro_por_filtro("id", usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        self.__repo.eliminar_registro(usuario_id)

    def buscar_usuario(self, filtro, valor):
        usuario = self.__repo.obtener_registro_por_filtro(filtro, valor)
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
    gestor = GestorDeUsuarios(repo)
    try:
        gestor.registrar_nuevo_usuario(
            nombre="nicolas",
            apellido="ramirez",
            email="ramiresn@gmail.com",
            nombre_de_usuario="tupapacitoXD_123",
            password="1234",
            rol = 0,
            claustro = "estudiante"
        )
        print("Usuario registrado correctamente")
    except Exception as e:
        print(f"Error: {e}")
        
    print(gestor.buscar_usuario("email", "ramiresn@gmail.com"))