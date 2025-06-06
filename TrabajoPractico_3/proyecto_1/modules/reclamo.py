from datetime import datetime
from typing import List


class Reclamo:
    def __init__(self, ID: int, estado: str, fecha_hora: datetime, contenido: str, departamento: str, departamentos: List[str], clasificacion: str):
        self.ID = ID
        self.estado = estado
        self.fecha_hora = fecha_hora
        self.contenido = contenido
        self.departamento = departamento
        self.departamentos = departamentos
        self.clasificacion = clasificacion

    def cambiar_estado(self, nuevo_estado: str):
        self.estado = nuevo_estado