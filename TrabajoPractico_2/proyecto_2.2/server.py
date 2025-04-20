from flask import Flask, render_template, request
from modules.cinta_transportadora import Sensor, CintaTransportadora, Cajon, Controlador

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def iniciar():
    metricas = None
    advertencias = []

    if request.method == "POST":
        try:
            total_alimentos_deseados = int(request.form["total_alimentos"])
        except (KeyError, ValueError):
            return "Error: Datos no válidos o no proporcionados.", 400

        # La capacidad del cajón será igual a la cantidad total de alimentos deseados
        capacidad = total_alimentos_deseados

        sensor = Sensor()
        cinta = CintaTransportadora(sensor)
        cajon = Cajon(capacidad)
        controlador = Controlador(cinta, cajon, total_alimentos_deseados)

        controlador.iniciar_transporte()
        metricas = controlador.calcular_metricas()

        # Generar advertencias si alguna métrica supera 0.90
        if metricas["aw_prom_frutas"] > 0.90:
            advertencias.append("Advertencia: La actividad acuosa promedio de las frutas supera 0.90")
        if metricas["aw_prom_verduras"] > 0.90:
            advertencias.append("Advertencia: La actividad acuosa promedio de las verduras supera 0.90")
        if metricas["aw_total"] > 0.90:
            advertencias.append("Advertencia: La actividad acuosa total supera 0.90")

    return render_template("inicio.html", metricas=metricas, advertencias=advertencias)

if __name__ == "__main__":
    app.run(debug=True)