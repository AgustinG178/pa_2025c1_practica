from abc import ABC,abstractmethod
from modules.departamento_abstracto import DepartamentoAbstracto
class InterfazGrafica(ABC):

    @abstractmethod
    def generar_dashboard(self):

        """
        Se devuelven todos los datos necesarios para que el jefe de departamento o secretario tecnico vea en la pantalla
        tales como los reclamos, o las métricas
        """
        pass


class InterfazJefeDepartamento(InterfazGrafica):

    def __init__(self,departamento=DepartamentoAbstracto):

        self.__departamento = departamento

    def generar_dashboard(self):
        
        reclamos = self.__departamento.listar_reclamos()

        analitica = self.__departamento.ver_analitica()

        jefe_dpto = self.__departamento.jefe_departamento
        
        return reclamos,analitica,jefe_dpto
