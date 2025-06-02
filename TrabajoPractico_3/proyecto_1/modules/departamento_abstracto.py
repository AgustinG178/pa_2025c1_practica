from abc import ABC,abstractmethod

class DepartamentoAbstracto(ABC):

    @property
    @abstractmethod

    def jefe_departamento(self):

        """
        Se devuelve el jefe del departamento
        """
        pass
    @abstractmethod

    def listar_reclamos(self):
        
        """
        Se listan todos los reclamos del departamento
        """
        pass

    @abstractmethod
    def resolver_reclamo_por_id(self,id_reclamo):

        """
        Se resuelve el reclamo según la id del mismo ('pendiente' --> 'resuelto')
        """
        pass

    @abstractmethod
    def ver_analitica(self):

        """
        Se realiza el cálculo de la mediana en el montículo de reclamos clasificados (que clasificacion posee mayor cantidad de reclamos)
        """
        pass
