from flask import render_template, request
from modules.config import app
from modules.modulo1 import leer_frases_de_peliculas, seleccionar_frase
import random
nombre_archivo = "frases_de_peliculas.txt"

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route("/Film Trivia Facil", methods=["GET", "POST"])
def pagjuego_facil():
    frases = leer_frases_de_peliculas(nombre_archivo)
    if request.method == "POST":
        respuesta_usuario = request.form.get("respuesta")
        resultado = procesar_respuesta(respuesta_usuario)
        return render_template("Facil.html", resultado=resultado)
    return render_template("Facil.html", frases = frases )

def procesar_respuesta(respuesta):
    return "Respuesta correcta" if respuesta == "la correcta" else "Respuesta incorrecta"

@app.route("/Film Trivia Normal")
def pagjuego_normal():
    return render_template("Normal.html")

@app.route("/Film Trivia Dificil")
def pagjuego_dificil():
    frases = leer_frases_de_peliculas(nombre_archivo)
    opciones=[]

    for i in range(3): 
        try:
            opciones.append([seleccionar_frase(frases)[0],seleccionar_frase(frases)[1]]) 
        except TypeError:
            return render_template("Inicio.html")     

        frase_random = random.choice(opciones)[1] 

    return render_template("Dificil.html",opciones=opciones,frase_random=frase_random)

if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True)

