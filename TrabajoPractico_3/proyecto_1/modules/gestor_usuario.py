from modules.usuarios import Usuario, UsuarioFinal, JefeDepartamento, SecretarioTecnico
from modules.repositorio import RepositorioAbstracto

class GestorDeUsuarios:
    def __init__(self, repo: RepositorioAbstracto):
        self.__repo = repo  

    """
    Intermediario entre el usuario y la base de datos, consiste de métodos para registrar, autenticar, cargar, actualizar, eliminar y buscar usuarios.
    """

    def registrar_nuevo_usuario(self, nombre, apellido, email, nombre_de_usuario, password, rol):
        if self.__repo.obtener_registro_por_filtro("email", email):
            raise ValueError("El usuario ya está registrado, por favor inicie sesión")
        # Guardar la contraseña en texto plano (NO recomendado en producción)
        if rol == "0":
            usuario = UsuarioFinal(nombre, apellido, email, nombre_de_usuario, password, rol)
        elif rol == "1":
            usuario = JefeDepartamento(nombre, apellido, email, nombre_de_usuario, password, rol)
        elif rol == "2":
            usuario = SecretarioTecnico(nombre, apellido, email, nombre_de_usuario, password, rol)

    def autenticar_usuario(self, email, password):
        usuario = self.__repo.obtener_registro_por_filtro("email", email)
        if not usuario:
            raise ValueError("El usuario no está registrado")
        if usuario.contraseña != password:
            raise ValueError("Contraseña incorrecta")
        return usuario.__dict__  # o usuario.to_dict() si tienes ese método
        
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
        return usuario

    def generar_reporte_usuario(self, tipo_reporte, *args, **kwargs):
        # Ejemplo: tipo_reporte puede ser "pdf" o "html"
        if tipo_reporte == "pdf":
            # Aquí deberías integrar con tu clase de reporte PDF
            return "Reporte PDF generado para usuarios"
        elif tipo_reporte == "html":
            # Aquí deberías integrar con tu clase de reporte HTML
            return "Reporte HTML generado para usuarios"
        else:
            raise ValueError("Tipo de reporte no soportado")
