from modules.repositorio import RepositorioReclamosSQLAlchemy
from modules.usuarios import Usuario
from modules.reclamo import Reclamo

repositorio_reclamo = RepositorioReclamosSQLAlchemy()

class GestorReclamo:

    """
    La clase gestor reclamo establece una relacion entre el modelo de negocio con la capa de dominio, sin interaccionar (directamente) con la base de datos
    a la hora de, por ejemplo, eliminar un reclamo.
    Sus metodos son practicamente los mismos que los del repositorio.
    """

    def __init__(self, repositorio_reclamo: RepositorioReclamosSQLAlchemy):
        self.repositorio_reclamo = repositorio_reclamo

    def crear_reclamo(self, usuario: Usuario, descripcion: str):

        """
        Se crea un reclamo a partir de un Usuario, descripcion y Departamento
        """
        if isinstance(usuario, Usuario) and descripcion != "":

            p_reclamo = Reclamo(usuario_id=usuario.id, contenido=descripcion)

            self.repositorio_reclamo.guardar_registro(p_reclamo)

        else:
            return "Verificar que los datos ingresados sean correctos"

    def buscar_reclamos_por_usuario(self, usuario: Usuario):
        """
        Se buscan y devuelven todos los reclamos asociados a un usuario
        """
        if isinstance(usuario, Usuario):

            try:

                reclamos = self.repositorio_reclamo.obtener_registro_por_filtro(filtro="usuario_id", valor=usuario.__id)

                return reclamos

            except AttributeError:
                return "El usuario no posee reclamos asociados"

        raise TypeError("El usuario no es una instancia de la clase Usuario")

    def actualizar_estado_reclamo(self, usuario: Usuario, reclamo: Reclamo):

        """
        Se actualiza el estado de un reclamo, solo lo es capaz de realizarlo un Secretario Tecnico o un Jefe de Departamento
        """

        if usuario.rol in ["Secretario Tecnico", "Jefe de Departamento"]:
            try:

                reclamo_a_modificar = self.reclamo.obtener_registro_por_filtro(filtro="id", valor=reclamo.id)

                reclamo_a_modificar.estado = "resuelto"

                self.repositorio_reclamo.actualizar_reclamo(reclamo=reclamo_a_modificar)

                return "¡¡Reclamo resuelto correctamente!!"
            except AttributeError:
                return f"El reclamo no existe y/o la id: {reclamo.id} no es correcta"

        raise PermissionError("El usuario no posee los permisos para realizar dicha modificación")

    def eliminar_reclamo(self, usuario: Usuario, reclamo_id: int):
        """
        Se elimina un reclamo (accediendo a este con su id) asociado a un usuario, realizando sus  pertinentes verificaciones.
        """
        if usuario.rol in ["Secretario Tecnico", "Jefe de Departamento"]:

            try:

                self.repositorio_reclamo.eliminar_registro_por_id(reclamo_id=reclamo_id)

                return f"El reclamo de id:{reclamo_id} se ha eliminado correctamente."

            except AttributeError:
                return f"El reclamo no existe y/o la id: {reclamo_id} no es correcta"

        raise PermissionError("El usuario no posee los permisos para realizar dicha modificacion.")

    def asignar_departamento(self, usuario: Usuario, reclamo_id: int, departamento_nuevo: Departamento):
        """
        Se cambia el departamento al cual está asociado un reclamo.
        """
        if usuario.rol == "Secretario Tecnico":

            try:

                reclamo = self.repositorio_reclamo.obtener_registro_por_filtro(filtro="id", valor=reclamo_id)

                reclamo.departamento_id == departamento_nuevo.id

                self.repositorio_reclamo.actualizar_reclamo(reclamo=reclamo)

                return f"El reclamo fue asignado al departamento {departamento_nuevo.nombre} correctamente!"
            except AttributeError:
                return f"El reclamo no existe y/o la id: {reclamo_id} no es correcta"

        raise PermissionError("El usuario no posee los permisos para realizar dicha modificacion.")

    def agregar_adherente(self, reclamo_id, usuario: Usuario):
        """
        Se agrega un adherente a un reclamo
        """

        if isinstance(usuario, Usuario):

            try:

                reclamo_a_adherir = self.repositorio_reclamo.obtener_registro_por_filtro(filtro="id", valor=reclamo_id)

                reclamo_a_adherir.usuarios.append(usuario)

                return "El usuario se ha adherido correctamente al reclamo."
            except AttributeError:

                return f"El reclamo no existe y/o la id: {reclamo_id} no es correcta"

        raise TypeError("El usuario no es una instancia de la clase reclamo.")
