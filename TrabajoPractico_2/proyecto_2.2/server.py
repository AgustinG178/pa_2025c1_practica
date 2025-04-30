from flask import Flask, render_template, request
from modules.sensor import Sensor, FabricaDeAlimentos
from modules.cajon import Cajon, AnalizadorDeCajon, GeneradorDeInforme
from modules.cinta_transportadora import CintaTransportadora

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

        fabrica = FabricaDeAlimentos()
        
        sensor = Sensor(fabrica)
        
        cajon = Cajon(total_alimentos_deseados)
        
        cinta = CintaTransportadora(sensor, cajon)

        cinta.iniciar_transporte()

        metricas = AnalizadorDeCajon.calcular_metricas(cajon)
        advertencias = GeneradorDeInforme.generar_advertencias(metricas)

    return render_template("inicio.html", metricas=metricas, advertencias=advertencias)

if __name__ == "__main__":
    app.run(debug=True)
