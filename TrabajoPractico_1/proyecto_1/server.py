from flask import render_template, request
from modules.config import app
from modules.modulos import juego_opciones, frases
from random import shuffle

@app.route('/')
def index():    
    return render_template('inicio.html')

@app.route("/Film Trivia Juego", methods=["GET", "POST"])
def dificil():

    frase, listaop = juego_opciones(frases, 10)
    
    if request.method == "POST":
        
        return render_template("juego.html", frase=frase, resultado = request.method == "POST")
    
    return render_template("juego.html", frase=frase, listaop = listaop)

if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True)
