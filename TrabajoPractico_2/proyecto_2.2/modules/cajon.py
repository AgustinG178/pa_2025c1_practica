from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria, Alimento, Fruta, Verdura
from math import exp

class Cajon:
    """
    Clase que representa un cajón para almacenar alimentos con una capacidad máxima.
    Permite agregar alimentos y acceder a ellos como una colección.
    """
    def __init__(self, capacidad):
        """
        Inicializa un cajón con una capacidad dada.
        Args:
            capacidad (int): Número máximo de alimentos que puede contener el cajón.
        """
        self.__capacidad = capacidad
        self.__alimentos = []
        
    def agregar_alimento(self, alimento:Alimento):
        """
        Agrega un alimento al cajón si hay espacio disponible.
        Args:
            alimento (Alimento): El alimento a agregar.
        """
        if len(self.__alimentos) >= self.__capacidad:
            raise Exception("El cajón está lleno")
        self.__alimentos.append(alimento)
    
    def __iter__(self):
        """
        Permite iterar sobre los alimentos del cajón.
        """
        for alimento in self.__alimentos:
            yield alimento

    def __len__(self):
        """
        Devuelve la cantidad de alimentos en el cajón.
        """
        return len(self.__alimentos)

    def __str__(self):
        """
        Devuelve una representación en cadena del cajón.
        """
        return f"Cajón con capacidad para {self.__capacidad} alimentos y contiene {len(self.__alimentos)} alimentos."

    @property
    def capacidad(self):
        """
        Capacidad máxima del cajón.
        """
        return self.__capacidad

    @property
    def alimentos(self):
        """
        Lista de alimentos en el cajón.
        """
        return self.__alimentos
    
    def __getitem__(self, index):
        """
        Permite acceder a los alimentos por índice.
        Args:
            index (int): Índice del alimento.
        """
        return self.__alimentos[index]
    
class AnalizadorDeCajon:
    """
    Clase utilitaria para calcular métricas sobre los alimentos de un cajón.
    """
    @staticmethod
    def calcular_metricas(cajon:Cajon):
        """
        Calcula métricas estadísticas sobre los alimentos del cajón.
        Args:
            cajon (Cajon): El cajón a analizar.
        """
        try:
            if cajon.capacidad == 0:
                    aw_prom_frutas = 0
                    aw_prom_verduras = 0
                    aw_prom_kiwi = 0
                    aw_prom_manzana = 0
                    aw_prom_papa = 0
                    aw_prom_zanahoria = 0
                    aw_total = 0
            else:
                
                frutas = [alimento for alimento in cajon if isinstance(alimento, Fruta)]
                verduras = [alimento for alimento in cajon if isinstance(alimento, Verdura)]

                aw_prom_frutas = sum(alimento.aw for alimento in frutas) / len(frutas) if frutas else 0
            
                aw_prom_verduras = sum(alimento.aw for alimento in verduras) / len(verduras) if verduras else 0
            
                aw_prom_kiwi = sum(alimento.aw for alimento in frutas if isinstance(alimento, Kiwi)) / len([alimento for alimento in frutas if isinstance(alimento, Kiwi)]) if [alimento for alimento in frutas if isinstance(alimento, Kiwi)] else 0
            
                aw_prom_manzana = sum(alimento.aw for alimento in frutas if isinstance(alimento, Manzana)) / len([alimento for alimento in frutas if isinstance(alimento, Manzana)]) if [alimento for alimento in frutas if isinstance(alimento, Manzana)] else 0
            
                aw_prom_papa = sum(alimento.aw for alimento in verduras if isinstance(alimento, Papa)) / len([alimento for alimento in verduras if isinstance(alimento, Papa)]) if [alimento for alimento in verduras if isinstance(alimento, Papa)] else 0
            
                aw_prom_zanahoria = sum(alimento.aw for alimento in verduras if isinstance(alimento, Zanahoria)) / len([alimento for alimento in verduras if isinstance(alimento, Zanahoria)]) if [alimento for alimento in verduras if isinstance(alimento, Zanahoria)] else 0
            
                aw_total = sum(alimento.aw for alimento in cajon) / len(cajon)

        except Exception as e:
            raise Exception(f"Error al calcular las métricas: {e}")

        return {
            "peso_total": round((sum(alimento.peso for alimento in cajon)), 2),
            "aw_prom_frutas": round(aw_prom_frutas, 2),
            "aw_prom_verduras": round(aw_prom_verduras, 2),
            "aw_prom_kiwi": round(aw_prom_kiwi, 2),
            "aw_prom_manzana": round(aw_prom_manzana, 2),
            "aw_prom_papa": round(aw_prom_papa, 2),
            "aw_prom_zanahoria": round(aw_prom_zanahoria, 2),
            "aw_total": round(aw_total, 2)
        }
        
class GeneradorDeInforme:
    """
    Clase utilitaria para mostrar métricas y advertencias sobre los alimentos del cajón.
    """
    @staticmethod
    def mostrar_metricas(metricas):
        """
        Imprime las métricas calculadas del cajón.
        Args:
            metricas (dict): Diccionario con métricas.
        """
        print("Métricas calculadas:")
        print(f"Peso total del cajón: {metricas['peso_total']} kg")
        print(f"AW promedio de frutas: {metricas['aw_prom_frutas']}")
        print(f"AW promedio de kiwi: {metricas['aw_prom_kiwi']}")
        print(f"AW promedio de manzana: {metricas['aw_prom_manzana']}")
        print(f"AW promedio de verduras: {metricas['aw_prom_verduras']}")
        print(f"AW promedio de papa: {metricas['aw_prom_papa']}")    
        print(f"AW promedio de verduras: {metricas['aw_prom_verduras']}")
        print(f"AW total del cajón: {metricas['aw_total']}")

    @staticmethod
    def generar_advertencias(metricas):
        """
        Genera advertencias si alguna métrica supera los valores recomendados.
        Args:
            metricas (dict): Diccionario con métricas.
        """
        advertencias = []
        if metricas["aw_prom_frutas"] > 0.90:
            advertencias.append("Advertencia: La actividad acuosa promedio de las frutas supera 0.90.")
        if metricas["aw_prom_verduras"] > 0.90:
            advertencias.append("Advertencia: La actividad acuosa promedio de las verduras supera 0.90.")
        if metricas["aw_prom_kiwi"] > 0.90:
            advertencias.append("Advertencia: La actividad acuosa promedio del kiwi supera 0.90.")
        if metricas["aw_prom_manzana"] > 0.90:
            advertencias.append("Advertencia: La actividad acuosa promedio de la manzana supera 0.90.")
        if metricas["aw_prom_papa"] > 0.90:
            advertencias.append("Advertencia: La actividad acuosa promedio de la papa supera 0.90.")
        if metricas["aw_prom_zanahoria"] > 0.90:
            advertencias.append("Advertencia: La actividad acuosa promedio de la zanahoria supera 0.90.")
        if metricas["aw_total"] > 0.90:
            advertencias.append("Advertencia: La actividad acuosa total supera 0.90.")
        return advertencias
    

if __name__ == "__main__": #pragma: no cover
    """
    Ejemplo de uso del módulo: crea un cajón, agrega alimentos, calcula métricas y muestra resultados.
    """
    cajon = Cajon(2)  # Capacidad de 2 alimentos
    cajon.agregar_alimento(Kiwi(500))
    cajon.agregar_alimento(Manzana(300))

    print("Contenido del cajón:")
    for alimento in cajon:
        print(alimento)
        
    analizador = AnalizadorDeCajon()    
        
    metricas = analizador.calcular_metricas(cajon)

    generador = GeneradorDeInforme()

    print(f"Metricas del cajón: {generador.mostrar_metricas(metricas)} ")