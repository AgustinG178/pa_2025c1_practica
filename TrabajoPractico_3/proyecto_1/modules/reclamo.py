from datetime import datetime

class Reclamo:
    """Clase para instanciar los reclamos echos por los usuarios"""
    def __init__(self, estado: str, fecha_hora: datetime, contenido: str, clasificacion: str, usuario_id: int = None, **kwargs):
        self.id = kwargs.get("id")  # se agrega solo si está presente
        self.estado = estado
        self.fecha_hora = fecha_hora
        self.contenido = contenido
        self.clasificacion = clasificacion
        self.usuario_id = usuario_id
        self.cantidad_adherentes = kwargs.get("cantidad_adherentes")
        self.tiempo_estimado = kwargs.get("tiempo_estimado")
        self.resuelto_en = kwargs.get("resuelto_en")


    def __repr__(self):
        return f"Reclamo(estado={self.estado}, fecha_hora={self.fecha_hora}, contenido={self.contenido}, clasificacion={self.clasificacion}, usuario_id={self.usuario_id})"

    def __str__(self):
        return f"Reclamo: {self.contenido} | Estado: {self.estado} | Fecha: {self.fecha_hora} | Clasificación: {self.clasificacion} | Usuario ID: {self.usuario_id}"
    