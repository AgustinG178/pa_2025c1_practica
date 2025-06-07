from modules.repositorio import RepositorioReclamosSQLAlchemy
from modules.usuarios import Usuario
from modules.reclamo import Reclamo
from modules.config import crear_engine
from datetime import datetime, UTC
from modules.classifier import Clasificador

session = crear_engine()
repositorio_reclamo = RepositorioReclamosSQLAlchemy(session)

class GestorReclamo:

    """
    La clase gestor reclamo establece una relacion entre el modelo de negocio con la capa de dominio, sin interaccionar (directamente) con la base de datos
    a la hora de, por ejemplo, eliminar un reclamo.
    Sus metodos son practicamente los mismos que los del repositorio.
    """

    def __init__(self, repositorio_reclamo: RepositorioReclamosSQLAlchemy, clasificador: Clasificador):
        self.repositorio_reclamo = repositorio_reclamo
        self.clasificador = clasificador

    def crear_reclamo(self, usuario, descripcion: str, departamento: str, clasificacion: str):
        # acepta cualquier objeto con atributo id, por ejemplo
        if not hasattr(usuario, 'id') or not descripcion or not departamento:
            raise ValueError("Verificar que los datos ingresados sean correctos")
        p_reclamo = Reclamo(
            estado="pendiente",
            fecha_hora=datetime.now(),
            usuario_id=usuario.id,
            contenido=descripcion,
            departamento=departamento,
            clasificacion=clasificacion
        )
        return p_reclamo
    
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
