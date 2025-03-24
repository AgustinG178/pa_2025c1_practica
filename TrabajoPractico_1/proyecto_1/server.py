from flask import render_template, request
from modules.config import app
from modules.modulos import seleccionar_peli, frases

@app.route('/')
def index():    
    return render_template('inicio.html')

@app.route("/Film Trivia Juego", methods=["GET", "POST"])
def dificil():

    frase, peli_c, peli_i = seleccionar_peli(frases, 10)

    if request.method == "POST":
        
        return render_template("juego.html", frase=frase, peli_c=peli_c, peli_i=peli_i)
    
    return render_template("juego.html", frase=frase, peli_c=peli_c, peli_i=peli_i)

if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True)

