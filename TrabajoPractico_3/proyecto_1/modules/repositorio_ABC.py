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
    def obtener_registro_por_filtros(self,mapeo=True, **kwargs):
        """
        Se obtiene un registro (reclamo/usuario) según uno o varios filtros correspondiente a sus atributos (id,nombre...)
        """
        
        raise NotImplementedError

    @abstractmethod
    def obtener_registros_por_filtro(self,filtro,valor,mapeo=True):
        """
        Se obtienen registros (reclamos/usuarios) aplicando un filtro; puede devolverlos mapeados o como modelos.
        """
        
        raise NotImplementedError
    @abstractmethod
    

    def eliminar_registro_por_id(self, id):
        """
        Se elimina un registro mediante su id
        """
            
        raise NotImplementedError

    @abstractmethod


    def map_modelo_a_entidad(entidad:object):

        """
        Se mapea un modelo (reclamo/usuario) a su entidad correspondiente
        """

        raise NotImplementedError

    def map_entidad_a_modelo(entidad:object):
        """
        Se mapea una entidad (reclamo/usuario) al modelo de la base de datos
        """
        raise NotImplementedError
