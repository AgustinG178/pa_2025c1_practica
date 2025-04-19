from modules.cinta_transportadora import Sensor, Alimento, Cajon, CintaTransportadora, Controlador

def main():
    # Configuración inicial
    capacidad_cajon = 5  # Número máximo de alimentos por cajón
    sensor = Sensor()
    cinta = CintaTransportadora(sensor)
    cajon = Cajon(capacidad_cajon)
    controlador = Controlador(cinta, cajon)

    # Iniciar transporte
    print("Iniciando transporte de alimentos...")
    controlador.iniciar_transporte()

    # Calcular métricas
    metricas = controlador.calcular_metricas()

    # Mostrar resultados
    print("\nResultados:")
    print(f"Peso total del cajón: {metricas['peso_total']} kg")
    print(f"Actividad acuosa promedio de frutas: {metricas['aw_prom_frutas']:.2f}")
    print(f"Actividad acuosa promedio de verduras: {metricas['aw_prom_verduras']:.2f}")
    print(f"Actividad acuosa promedio total: {metricas['aw_total']:.2f}")

    # Advertencias
    if metricas["aw_prom_frutas"] > 0.90:
        print("Advertencia: La actividad acuosa promedio de frutas supera 0.90")
    if metricas["aw_prom_verduras"] > 0.90:
        print("Advertencia: La actividad acuosa promedio de verduras supera 0.90")
    if metricas["aw_total"] > 0.90:
        print("Advertencia: La actividad acuosa promedio total supera 0.90")

    # Mostrar alimentos en el cajón
    print("\nAlimentos en el cajón:")
    for alimento in cajon:
        print(f"- {alimento.nombre} ({alimento.tipo}), Peso: {alimento.peso} g, aw: {alimento.aw:.2f}")

if __name__ == "__main__":
    main()