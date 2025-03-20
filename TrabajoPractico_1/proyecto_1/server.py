from flask import render_template, request
from modules.config import app
from modules.modulos import procesar_respuesta, seleccionar_peli, frases

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

    frase, peli_c, peli_i = seleccionar_peli(frases, 10)

    if request.method == "POST":
        
        return render_template("Dificil.html", frase=frase, peli_c=peli_c, peli_i=peli_i)
    
    return render_template("Dificil.html", frase=frase, peli_c=peli_c, peli_i=peli_i)

if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True)

