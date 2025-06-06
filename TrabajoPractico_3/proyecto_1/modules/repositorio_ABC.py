from abc import ABC, abstractmethod

class Repositorio(ABC):
    @abstractmethod
    def guardar_registro(self, entidad:object):
        """
        Se guarda la entidad (objeto) en la base de datos
        """

        raise NotImplementedError

    @abstractmethod
    def obtener_todos_los_registros(self) -> list:
        """
        Se obtienen todos los registros (reclamos/usuarios) existentes en la base de daots
        """
        raise NotImplementedError
    
    @abstractmethod
    def modificar_registro(self, entidad_modificada:object):
        """
        Se modifica una entidad, se pasa como parámetro la misma entidad con sus atributos modificados
        """
        raise NotImplementedError   
    
    @abstractmethod
    def obtener_registro_por_filtro(self, filtro, valor):
        """
        Se obtiene un registro (reclamo/usuario) según un filtro correspondiente a sus atributos (id,nombre...)
        """
        
        raise NotImplementedError
    
    @abstractmethod

    def eliminar_registro_por_id(self, id):
        """
        Se elimina un registro mediante su id
        """
            
        raise NotImplementedError
