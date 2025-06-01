from modules.modelos import Usuario, Reclamo
from sqlalchemy.orm import Session

class IRepositorioReclamos:
    def __init__(self, session: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.
        """
        self.session = session

    def guardar_usuario(self, usuario: Usuario):
        """
        Guarda un objeto Usuario en la base de datos.
        """
        self.session.add(usuario)
        self.session.commit()

    def guardar_reclamo(self, reclamo: Reclamo):
        """
        Guarda un objeto Reclamo en la base de datos.
        """
        self.session.add(reclamo)
        self.session.commit()

    def actualizar_reclamo(self, reclamo: Reclamo):
        """
        Actualiza un objeto Reclamo existente en la base de datos.
        """
        self.session.merge(reclamo)
        self.session.commit()

    def obtener_reclamos(self, usuario: Usuario):
        """
        Obtiene todos los reclamos de un usuario.
        """
        return self.session.query(Reclamo).filter_by(usuario_id=usuario.id).all()

class GestorReclamo:
    def __init__(self, repositorio_reclamo):
        self.repositorio_reclamo = repositorio_reclamo

    def crear_reclamo(self, usuario, descripcion, departamento):
        # Lógica para crear y guardar un reclamo
        pass

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
