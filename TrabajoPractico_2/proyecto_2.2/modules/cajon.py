from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from math import exp


class Cajon:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.__alimentos = []
        
    def agregar_alimento(self, alimento):
        if len(self.__alimentos) >= self.capacidad:
            raise Exception("El cajón está lleno")
        self.__alimentos.append(alimento)
        
    def __iter__(self):
        return iter(self.__alimentos)

    def __len__(self):
        return len(self.__alimentos)

    @property
    def alimentos(self):
        return self.__alimentos
    
class AnalizadorDeCajon:
    @staticmethod
    def calcular_metricas(cajon):
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
                
                frutas = [alimento for alimento in cajon if alimento.tipo == "fruta"]
                verduras = [alimento for alimento in cajon if alimento.tipo == "verdura"]

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
    @staticmethod
    def mostrar_metricas(metricas):
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