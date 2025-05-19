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
