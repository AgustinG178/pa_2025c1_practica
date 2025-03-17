from flask import render_template
from modules.config import app

from modules.Juego import frases

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route("/Film Trivia Facil")
def pagjuego_facil():
    return render_template("Facil.html")

@app.route("/Film Trivia Normal")
def pagjuego_normal():
    return render_template("Normal.html")

@app.route("/Film Trivia Dificil")
def pagjuego_dificil():
    return render_template("Dificil.html")

if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True)