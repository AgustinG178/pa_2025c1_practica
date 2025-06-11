from datetime import datetime

class Reclamo:
    def __init__(self, estado: str, fecha_hora: datetime, contenido: str, departamento: str, clasificacion: str, usuario_id: int = None, **kwargs):
        self.id = kwargs.get("id")  # se agrega solo si está presente
        self.estado = estado
        self.fecha_hora = fecha_hora
        self.contenido = contenido
        self.departamento = departamento
        self.clasificacion = clasificacion
        self.usuario_id = usuario_id
        self.cantidad_adherentes = kwargs.get("cantidad_adherentes")

    def __repr__(self):
        return f"Reclamo(estado={self.estado}, fecha_hora={self.fecha_hora}, contenido={self.contenido}, departamento={self.departamento}, clasificacion={self.clasificacion}, usuario_id={self.usuario_id})"

    def __str__(self):
        return f"Reclamo: {self.contenido} | Estado: {self.estado} | Fecha: {self.fecha_hora} | Departamento: {self.departamento} | Clasificación: {self.clasificacion} | Usuario ID: {self.usuario_id}"
    