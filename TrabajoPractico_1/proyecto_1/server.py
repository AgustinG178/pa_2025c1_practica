from flask import render_template, request
from modules.config import app
from modules.Juego import frases




@app.route('/')
def index():
    return render_template('inicio.html')

@app.route("/Film Trivia Facil", methods=["GET", "POST"])
def pagjuego_facil():
    if request.method == "POST":
        respuesta_usuario = request.form.get("respuesta")
        resultado = procesar_respuesta(respuesta_usuario)
        return render_template("Facil.html", basejuego1=frases, resultado=resultado)
    return render_template("Facil.html", basejuego1=frases)

def procesar_respuesta(respuesta):
    return "Respuesta correcta" if respuesta == "la correcta" else "Respuesta incorrecta"

@app.route("/Film Trivia Normal")
def pagjuego_normal():
    return render_template("Normal.html")

@app.route("/Film Trivia Dificil")
def pagjuego_dificil():
    return render_template("Dificil.html")

if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True)
   