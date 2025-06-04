from modules.modelos import Usuario, Reclamo,Departamento
from sqlalchemy.orm import Session
from modules.repositorio import RepositorioReclamosSQLAlchemy

#Tiene sentido esta clase? Para mi no, es lo mismo que los dos repositorios del modulo repositorio
# class IRepositorioReclamos:
#     def __init__(self, session: Session):
#         """
#         Inicializa el repositorio con una sesión de base de datos.
#         """
#         self.session = session

#     def guardar_usuario(self, usuario: Usuario):
#         """
#         Guarda un objeto Usuario en la base de datos.
#         """
#         self.session.add(usuario)
#         self.session.commit()

#     def guardar_reclamo(self, reclamo: Reclamo):
#         """
#         Guarda un objeto Reclamo en la base de datos.
#         """
#         self.session.add(reclamo)
#         self.session.commit()

#     def actualizar_reclamo(self, reclamo: Reclamo):
#         """
#         Actualiza un objeto Reclamo existente en la base de datos.
#         """
#         self.session.merge(reclamo)
#         self.session.commit()

#     def obtener_reclamos(self, usuario: Usuario):
#         """
#         Obtiene todos los reclamos de un usuario.
#         """
#         return self.session.query(Reclamo).filter_by(usuario_id=usuario.id).all()

class GestorReclamo:

    """
    La clase gestor reclamo establece una relacion entre el modelo de negocio con la capa de dominio, sin interaccionar (directamente) con la base de datos
    a la hora de, por ejemplo, eliminar un reclamo.
    Sus metodos son practicamente los mismos que los del repositorio.
    """

    def __init__(self, repositorio_reclamo: RepositorioReclamosSQLAlchemy):
        self.repositorio_reclamo = repositorio_reclamo

    def crear_reclamo(self, usuario: Usuario, descripcion: str, departamento: Departamento):

        """
        Se crea un reclamo a partir de un Usuario, descripcion y Departamento
        """
        if isinstance(usuario, Usuario) and isinstance(departamento, Departamento) and descripcion != "":

            p_reclamo = Reclamo(usuario_id=usuario.id, contenido=descripcion, departamento_id=departamento.id)

            self.repositorio_reclamo.guardar_registro(p_reclamo)

        else:
            return "Verificar que los datos ingresados sean correctos"

    def buscar_reclamos_por_usuario(self, usuario: Usuario):
        """
        Se buscan y devuelven todos los reclamos asociados a un usuario
        """
        if isinstance(usuario, Usuario):
            reclamos_base = self.repositorio_reclamo.obtener_todos_los_registros()
            reclamos_usuario = []

            for reclamo in reclamos_base:
                if reclamo.usuario_id == usuario.id:
                    reclamos_usuario.append(reclamo)

            return reclamos_usuario

        raise TypeError("El usuario no es una instancia de la clase Usuario")

    def actualizar_estado_reclamo(self, usuario: Usuario, reclamo_id: int):

        """
        Se actualiza el estado de un reclamo, solo lo es capaz de realizarlo un Secretario Tecnico o un Jefe de Departamento
        """

        if usuario.rol in ["Secretario Tecnico", "Jefe de Departamento"]:
            try:

                reclamo_a_modificar = self.repositorio_reclamo.obtener_registro_por_filtro(filtro="id", valor=reclamo_id)

                reclamo_a_modificar.estado = "resuelto"

                self.repositorio_reclamo.actualizar_reclamo(reclamo=reclamo_a_modificar)

                return "¡¡Reclamo resuelto correctamente!!"
            except AttributeError:
                return f"El reclamo no existe y/o la id: {reclamo_id} no es correcta"

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

#Asumo que el estado solo es "pendiente" o "resuelto"