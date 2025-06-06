from datetime import datetime
from typing import List

class Reclamo:
    def __init__(self, estado: str, fecha_hora: datetime, contenido: str, departamento: str, clasificacion: str, usuario_id: int = None):
        self.estado = estado
        self.fecha_hora = fecha_hora
        self.contenido = contenido
        self.departamento = departamento
        self.clasificacion = clasificacion
        self.usuario_id = usuario_id  # asignado luego cuando se cree el reclamo
        
    def __repr__(self):
        return f"Reclamo(estado={self.estado}, fecha_hora={self.fecha_hora}, contenido={self.contenido}, departamento={self.departamento}, clasificacion={self.clasificacion}, usuario_id={self.usuario_id})"

    def cambiar_estado(self, nuevo_estado: str):
        self.estado = nuevo_estado