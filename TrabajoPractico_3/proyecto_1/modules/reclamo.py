from datetime import datetime

class Reclamo:
    """Clase para instanciar los reclamos echos por los usuarios"""
    def __init__(self, estado: str, fecha_hora: datetime, contenido: str, clasificacion: str, usuario_id: int = None, **kwargs):
        self.__id = kwargs.get("id")  # se agrega solo si está presente
        self.__estado = estado
        self.__fecha_hora = fecha_hora
        self.__contenido = contenido
        self.__clasificacion = clasificacion
        self.__usuario_id = usuario_id
        self.__cantidad_adherentes = kwargs.get("cantidad_adherentes")
        self.__tiempo_estimado = kwargs.get("tiempo_estimado")
        self.__resuelto_en = kwargs.get("resuelto_en")

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, nuevo_id):
        if isinstance(nuevo_id, int) and nuevo_id > 0:
            self.__id = nuevo_id
        else:
            raise ValueError("El ID debe ser un entero positivo.")
    
    @property
    def estado(self):
        return self.__estado
    
    @estado.setter
    def estado(self, nuevo_estado):
        if nuevo_estado in ["pendiente", "en_proceso", "resuelto", "invalidado"]:
            self.__estado = nuevo_estado
        else:
            raise ValueError("Estado inválido. Debe ser 'pendiente', 'en_proceso', 'resuelto' o 'invalidado'.")
        
    @property
    def fecha_hora(self):
        return self.__fecha_hora
    
    @fecha_hora.setter
    def fecha_hora(self, nueva_fecha_hora):
        if isinstance(nueva_fecha_hora, datetime):
            self.__fecha_hora = nueva_fecha_hora
        else:
            raise ValueError("Fecha y hora deben ser un objeto datetime.")
        
    @property
    def contenido(self):
        return self.__contenido
    
    @contenido.setter
    def contenido(self, nuevo_contenido):
        if isinstance(nuevo_contenido, str) and nuevo_contenido:
            self.__contenido = nuevo_contenido
        else:
            raise ValueError("El contenido debe ser una cadena no vacía.")
        
    @property
    def clasificacion(self):
        return self.__clasificacion
    
    @clasificacion.setter
    def clasificacion(self, nueva_clasificacion):
        if isinstance(nueva_clasificacion, str) and nueva_clasificacion:
            self.__clasificacion = nueva_clasificacion
        else:
            raise ValueError("La clasificación debe ser una cadena no vacía.")
        
    @property
    def usuario_id(self):
        return self.__usuario_id
    
    @usuario_id.setter
    def usuario_id(self, nuevo_usuario_id):
        if isinstance(nuevo_usuario_id, int) and nuevo_usuario_id > 0:
            self.__usuario_id = nuevo_usuario_id
        else:
            raise ValueError("El ID del usuario debe ser un entero positivo.")
        
    @property
    def cantidad_adherentes(self):
        return self.__cantidad_adherentes
   
    @cantidad_adherentes.setter
    def cantidad_adherentes(self, nueva_cantidad):
        if isinstance(nueva_cantidad, int) and nueva_cantidad >= 0:
            self.__cantidad_adherentes = nueva_cantidad
        else:
            raise ValueError("La cantidad de adherentes debe ser un entero no negativo.")
   
    @property
    def tiempo_estimado(self):
        return self.__tiempo_estimado
   
    @tiempo_estimado.setter
    def tiempo_estimado(self, nuevo_tiempo):
        if isinstance(nuevo_tiempo, int) and nuevo_tiempo >= 0:
            self.__tiempo_estimado = nuevo_tiempo
        else:
            raise ValueError("El tiempo estimado debe ser un entero no negativo.")
   
    @property
    def resuelto_en(self):
        return self.__resuelto_en
   
    @resuelto_en.setter
    def resuelto_en(self, nuevo_tiempo):
        if isinstance(nuevo_tiempo, int) and nuevo_tiempo >= 0:
            self.__resuelto_en = nuevo_tiempo
        else:
            raise ValueError("El tiempo de resolución debe ser un entero no negativo.") 

    def __repr__(self):
        return f"Reclamo(estado={self.estado}, fecha_hora={self.fecha_hora}, contenido={self.contenido}, clasificacion={self.clasificacion}, usuario_id={self.usuario_id})"

    def __str__(self):
        return f"Reclamo: {self.contenido} | Estado: {self.estado} | Fecha: {self.fecha_hora} | Clasificación: {self.clasificacion} | Usuario ID: {self.usuario_id}"
    