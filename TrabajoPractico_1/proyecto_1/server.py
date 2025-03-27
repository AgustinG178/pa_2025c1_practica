from flask import render_template, request
from modules.config import app
from modules.modulos import seleccionar_peli, frases
from random import shuffle

@app.route('/')
def index():    
    return render_template('inicio.html')

@app.route("/Film Trivia Juego", methods=["GET", "POST"])
def dificil():

    frase, listaop = seleccionar_peli(frases, 10)
    
    if request.method == "POST":
        
        return render_template("juego.html", frase=frase, listaop = listaop, resultado = request.method == "POST")
    
    return render_template("juego.html", frase=frase, listaop = listaop)

if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True)
