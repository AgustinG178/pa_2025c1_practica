from flask import Flask, render_template, request
from modules.verduleria import CintaTransportadora, Cajon, FabricaDeAlimentos, Sensor, AnalizadorDeCajon, GeneradorDeInforme

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def iniciar():
    metricas = None
    advertencias = []

    if request.method == "POST":
        try:
            # Obtener el número total de alimentos deseados desde el formulario
            total_alimentos_deseados = int(request.form["total_alimentos"])
        except (KeyError, ValueError):
            return "Error: Datos no válidos o no proporcionados.", 400

        # Configurar la capacidad del cajón
        capacidad = total_alimentos_deseados

        # Crear los objetos necesarios
        fabrica = FabricaDeAlimentos()
        sensor = Sensor(fabrica)
        cajon = Cajon(capacidad)
        cinta = CintaTransportadora(sensor, cajon)

        # Iniciar el transporte de alimentos
        cinta.iniciar_transporte()

        # Calcular las métricas del cajón
        metricas = AnalizadorDeCajon.calcular_metricas(cajon)

        # Generar el informe con advertencias
        advertencias = GeneradorDeInforme.generar_advertencias(metricas)

    # Renderizar la plantilla HTML con las métricas y advertencias
    return render_template("inicio.html", metricas=metricas, advertencias=advertencias)

if __name__ == "__main__":
    app.run(debug=True)