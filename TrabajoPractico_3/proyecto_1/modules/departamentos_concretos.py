from modules.departamento_abstracto import DepartamentoAbstracto
from modules.usuarios import JefeDepartamento, SecretarioTecnico
from modules.modelos import Reclamo
from modules.repositorio  import RepositorioReclamosSQLAlchemy

class DepartamentoMatematica(DepartamentoAbstracto):


    def __init__(self, reclamos: list[Reclamo], jefe_departamento:JefeDepartamento,conexion_base:RepositorioReclamosSQLAlchemy):

        self.__conexion_base = RepositorioReclamosSQLAlchemy

        self.__reclamos_departamento = reclamos

        self.__jefe_departamento = jefe_departamento

    @property
    def jefe_departamento(self):

        return self.__jefe_departamento
        
    def listar_reclamos(self):
        return [reclamo for reclamo in self.__reclamos_departamento]
    
    def resolver_reclamo_por_id(self, id_reclamo):
        
       reclamo = self.__conexion_base.obtener_registro_por_filtro(filtro="id",valor=id_reclamo)

       if reclamo.departamento == "Departamento Natenatica":

            self.__jefe_departamento.manejar_reclamo(id_reclamo=id_reclamo,base_datos=self.__conexion_base)


    def ver_analitica(self):
        
        pass


class DepartamentoComputacion(DepartamentoAbstracto):


    def __init__(self, reclamos: list[Reclamo], jefe_departamento:JefeDepartamento,conexion_base:RepositorioReclamosSQLAlchemy):

        self.__conexion_base = RepositorioReclamosSQLAlchemy

        self.__reclamos_departamento = reclamos

        self.__jefe_departamento = jefe_departamento

    @property
    def jefe_departamento(self):

        return self.__jefe_departamento
        
    def listar_reclamos(self):
        return [reclamo for reclamo in self.__reclamos_departamento]
    
    def resolver_reclamo_dpto_por_id(self, id_reclamo):
        
        reclamo = self.__conexion_base.obtener_registro_por_filtro(filtro="id",valor=id_reclamo)

        if reclamo.departamento == "Departamento Computacion":

            self.__jefe_departamento.manejar_reclamo(id_reclamo=id_reclamo,base_datos=self.__conexion_base)


    def ver_analitica(self):
        
        pass



