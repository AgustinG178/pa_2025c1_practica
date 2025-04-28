from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from math import exp


class Cajon:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.alimentos = []

    def agregar_alimento(self, alimento):
        if len(self.alimentos) < self.capacidad:
            self.alimentos.append(alimento)
        else:
            raise Exception("El cajón está lleno.")

    def peso_total(self):
        return sum(alimento.peso for alimento in self.alimentos)

    def __iter__(self):
        return iter(self.alimentos)

    def __len__(self):
        return len(self.alimentos)

class AnalizadorDeCajon:
    @staticmethod
    def calcular_metricas(cajon):
        frutas = [alimento for alimento in cajon if alimento.tipo == "fruta"]
        verduras = [alimento for alimento in cajon if alimento.tipo == "verdura"]

        aw_prom_frutas = sum(alimento.aw for alimento in frutas) / len(frutas) if frutas else 0
        aw_prom_verduras = sum(alimento.aw for alimento in verduras) / len(verduras) if verduras else 0
        aw_total = sum(alimento.aw for alimento in cajon) / len(cajon)

        return {
            "peso_total": round((sum(alimento.peso for alimento in cajon)) / 1000, 2),
            "aw_prom_frutas": round(aw_prom_frutas, 2),
            "aw_prom_verduras": round(aw_prom_verduras, 2),
            "aw_total": round(aw_total, 2)
        }
        
class GeneradorDeInforme:
    @staticmethod
    def mostrar_metricas(metricas):
        print("Métricas calculadas:")
        print(f"Peso total del cajón: {metricas['peso_total']} kg")
        print(f"AW promedio de frutas: {metricas['aw_prom_frutas']}")
        print(f"AW promedio de verduras: {metricas['aw_prom_verduras']}")
        print(f"AW total del cajón: {metricas['aw_total']}")

    @staticmethod
    def generar_advertencias(metricas):
        advertencias = []
        if metricas["aw_prom_frutas"] > 0.90:
            advertencias.append("Advertencia: La actividad acuosa promedio de las frutas supera 0.90.")
        if metricas["aw_prom_verduras"] > 0.90:
            advertencias.append("Advertencia: La actividad acuosa promedio de las verduras supera 0.90.")
        if metricas["aw_total"] > 0.90:
            advertencias.append("Advertencia: La actividad acuosa total supera 0.90.")
        return advertencias
    

if __name__ == "__main__":

    cajon = Cajon(2)  # Capacidad de 2 alimentos
    cajon.agregar_alimento(Kiwi(500))
    cajon.agregar_alimento(Manzana(300))

    print("Contenido del cajón:")
    for alimento in cajon:
        print(alimento)

    print(f"Peso total del cajón: {cajon.peso_total()} g")