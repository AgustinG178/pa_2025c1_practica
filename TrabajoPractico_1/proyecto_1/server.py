from flask import render_template, request, session, redirect, url_for, send_file, make_response
from modules.config import app
import os
import datetime
from modules.juego import (
    juego_opciones,
    listar_peliculas,
    opcion_correcta,
    escribir_resultados_archivo,
    leer_archivo_resultados,
    leer_frases_de_peliculas
)

from modules.graficos import (
    convertir_pdf,
    graficar_intentos_vs_aciertos,
    graficar_aciertos_vs_desaciertos_por_fecha  
)


# Definimos la ruta del archivo de resultados y el nombre del archivo de frases, las cuale son constantes

file_path = "data/resultados.txt"
folder = "TrabajoPractico_1/proyecto_1/static/graficos"
nombre_archivo = "frases_de_peliculas.txt"
frases = leer_frases_de_peliculas(nombre_archivo)
STATIC_GRAPH_PATH = "static/grafico_torta.png"
nombre_archivo = "frases_de_peliculas.txt"      

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Ruta de pagina de inicio.
    - GET: Muestra la página de inicio con el formulario para ingresar el nombre de usuario y la cantidad de intentos.
    - POST: Guarda los datos del usuario en la sesión y redirige a la página del juego.
    """
    if request.method == "POST":
        session["usuario"] = request.form.get("input_usuario")
        session["intentos"] = int(request.form.get("input_intentos"))
        return redirect(url_for("juego"))
    else:
        return render_template('inicio.html')

@app.route("/Film Trivia Juego", methods=["GET", "POST"])
def juego():
    """
    Maneja la lógica principal del juego.
    - GET: Muestra la primera ronda del juego.
    - POST: Procesa las respuestas del usuario, actualiza los aciertos y genera la siguiente ronda.
    - Al finalizar las rondas, guarda los resultados en el archivo y redirige al historial.
    """

    #definimos los aciertos como un atributo de session para poder actualizarlos a medida que transcurre el juego
    if "num_aciertos" not in session:
        session["num_aciertos"] = 0

    #definimos el número de intentos
    intentos = session["intentos"]

    #construimos las rondas como un atributo de session, de esta manera no se repiten las frases
    if "rondas" not in session:
         session["rondas"] = juego_opciones(frases, intentos)
    
    
    #Establecemos las operaciones que realiza la pagina cuando se envia una solicitud POST, es decir, cuando el usuario selecciona una opción
    if request.method == "POST":


                ronda_actual = int(request.form.get("ronda_actual",0)) + 1 #actualiza el valor de la ronda

                #Verificamos si el usuario selecciona el metodo terminar partida (no se guardan los datos)


                if ronda_actual <= intentos:
                    # Verificamos la opción elegida por el usuario
                    peli_correcta = request.form["peli_correcta"]
                    peli_elegida = request.form["respuesta"]
                    session["num_aciertos"] += opcion_correcta(peli_correcta, peli_elegida)

                    return render_template(
                        "juego.html",
                        ronda=session["rondas"][ronda_actual - 1],
                        num_ronda=ronda_actual,
                        resultado=request.method == "POST",
                        aciertos=session["num_aciertos"],
                        opcion_anterior=opcion_correcta(peli_correcta, peli_elegida),
                        peli_correcta=peli_correcta,
                    )
                else:
                    # Escribimos los resultados en un archivo solo una vez
                    escribir_resultados_archivo(
                        session["usuario"], session["num_aciertos"], intentos,
                    )

                    # Actualizar el gráfico de torta y el gráfico de curvas
                    graficar_intentos_vs_aciertos("data/resultados.txt", "static/graficos")
                    graficar_aciertos_vs_desaciertos_por_fecha("data/resultados.txt", "static/graficos")

                    # Limpiamos todos los valores de las claves de la sesión
                    session.clear()

                    # Redirigimos al historial
                    return redirect(url_for("historial"))
                    
    else:
        #Se devuelve la primera página de juego (primera ronda)
        ronda_actual = 1

        return render_template("juego.html", ronda=session["rondas"][ronda_actual-1],num_ronda = ronda_actual,aciertos = session["num_aciertos"]) 
    
@app.route("/historial", methods=["GET", "POST"])
def historial():
    """
    Muestra el historial de resultados de las partidas jugadas.
    - Lee los datos del archivo de resultados y los envía al HTML para su visualización.
    """
    juegos_data = leer_archivo_resultados()
    return render_template("resultados.html", juegos_data=juegos_data)

@app.route("/graficos", methods=["GET"])
def graficos():
    """
    Muestra la página de gráficos.
    - Incluye los gráficos generados a partir de los resultados de las partidas.
    """
    return render_template("graficos.html", grafico_url=url_for('static', filename='graficos/grafico_torta_general.png'))

@app.route("/descargar_grafico/<filename>", methods=["GET"])
def descargar_grafico(filename):
    """
    Convierte un gráfico en formato PNG a PDF y lo descarga.
    Args:
        filename (str): Nombre del archivo PNG a convertir.
    """
    pdf_path = convertir_pdf(filename)
    return send_file(pdf_path, as_attachment=True)

@app.route("/listado_peliculas", methods=["GET"])
def listado_peliculas():
    """
    Muestra un listado de todas las películas únicas ordenadas alfabéticamente.
    - Lee las películas del archivo frases_de_peliculas.txt.
    """
    file_path = "TrabajoPractico_1/proyecto_1/data/frases_de_peliculas.txt"
    peliculas = listar_peliculas(file_path)
    return render_template("listado_peliculas.html", peliculas=peliculas)
     
if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True)
