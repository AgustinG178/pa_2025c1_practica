from flask import render_template
from modules.config import app
import sys
import os

"""ruta_juego = "C:\\\\Users\\\\agugr\\\\OneDrive\\\\Programacion\\\\Programacion_Avanzada\\\\REPO_tp1\\\\pa_2025c1_practica\\\\TrabajoPractico_1\\\\proyecto_1\\\\templates\\\\Juego.py"

sys.path.append(ruta_juego)

from Juego import frases"""

@app.route('/')
def index():
    return render_template('inicio.html')   

@app.route("/Film Trivia Facil")
def pagjuego_facil():
    frasespelis = frases
    return render_template("Facil.html", frasespelis = frases)

@app.route("/Film Trivia Normal")
def pagjuego_normal():
    return render_template("Normal.html")

@app.route("/Film Trivia Dificil")
def pagjuego_dificil():
    return render_template("Dificil.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    