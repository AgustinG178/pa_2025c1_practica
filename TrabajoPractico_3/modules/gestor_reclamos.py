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

    def __init__(self, repositorio_reclamo:RepositorioReclamosSQLAlchemy):
        self.repositorio_reclamo = repositorio_reclamo

    def crear_reclamo(self, usuario:Usuario, descripcion:str, departamento:Departamento):

        if isinstance(usuario,Usuario) and isinstance(departamento,Departamento) and descripcion != "":

            p_reclamo = Reclamo(usuario_id= usuario.id,)


    def buscar_reclamos_por_usuario(self, usuario):
        # Lógica para buscar reclamos de un usuario
        pass

    def actualizar_estado_reclamo(self, reclamo_id, nuevo_estado):
        # Lógica para actualizar estado
        pass

    def eliminar_reclamo(self, reclamo_id):
        # Lógica para eliminar reclamo
        pass

    def asignar_departamento(self, reclamo_id, departamento):
        # Lógica para asignar departamento
        pass

    def agregar_adherente(self, reclamo_id, usuario):
        # Lógica para adherir usuario a reclamo
        pass
