from flask import render_template, request
from modules.config import app
from modules.Juego import dif_dificil, peliculas, frases, frase
from modules.modulos import procesar_respuesta, dif_dificil

frase = frase
opciones = []

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route("/Film Trivia Facil", methods=["GET", "POST"])
def pagjuego_facil():
    if request.method == "POST":
        respuesta_usuario = request.form.get("respuesta")
        resultado = procesar_respuesta(respuesta_usuario)
        return render_template("Facil.html", resultado=resultado)
    return render_template("Facil.html", frasesitas = frases )

@app.route("/Film Trivia Normal")
def pagjuego_normal():
    return render_template("Normal.html")

@app.route("/Film Trivia Dificil", methods=["GET", "POST"])
def dificil():
    if request.method == "POST":
        respuesta_usuario = request.form.get("respuesta")
        resultado2 = procesar_respuesta(respuesta_usuario)  
        return render_template("Dificil.html", resultado2=resultado2, opciones=opciones)
    dif_dificil(peliculas)
    return render_template("Dificil.html",opciones=peliculas, frase = frase)

if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True)

