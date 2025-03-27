from flask import render_template, request
from modules.config import app
from modules.modulos import juego_opciones, frases, opcion_correcta

@app.route('/')
def index():    
    return render_template('inicio.html')
@app.route("/Film Trivia Juego", methods=["GET", "POST"])
def dificil():
    try: 
        aciertos = 0
        vidas = 0
        juego = juego_opciones(frases, 10)
        if request.method == "POST":
            peli_correcta = juego[0][1]
            return render_template("juego.html", juego=juego, resultado = request.method == "POST", aciertos = aciertos)
    except IndexError:
        return render_template('inicio.html')
    return render_template("juego.html", juego=juego )

if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True)
