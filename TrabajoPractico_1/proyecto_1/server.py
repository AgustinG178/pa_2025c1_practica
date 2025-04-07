from flask import render_template, request, session, redirect, url_for, send_file, make_response
from modules.config import app
<<<<<<< HEAD
from modules.modulos import (
    juego_opciones,
    opcion_correcta,
    escribir_resultados_archivo,
    leer_archivo_resultados,
    leer_frases_de_peliculas,
    graficar_intentos_vs_aciertos,  # Importar la función para graficar
    graficar_aciertos_vs_desaciertos_por_fecha  # Importar la nueva función para graficar
)
from datetime import datetime
import os
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

=======
from modules.modulos import juego_opciones, opcion_correcta, escribir_resultados_archivo, leer_archivo_resultados, leer_frases_de_peliculas,graficar_intentos_vs_aciertos
from datetime import datetime
file_path = "TrabajoPractico_1/proyecto_1/data/resultados.txt"
folder = "TrabajoPractico_1/proyecto_1/static/graficos"
>>>>>>> 8d7e4372524bae2515ef9fa65b48deecd1273235
nombre_archivo = "frases_de_peliculas.txt"

frases = leer_frases_de_peliculas(nombre_archivo)      


@app.route("/",methods=["GET","POST"])
def index():   
    if request.method == "POST":
        
        session["usuario"] = request.form.get("input_usuario")
        session["intentos"] = int(request.form.get("input_intentos"))

        return redirect(url_for("juego"))
    
    else:
        return render_template('inicio.html')

@app.route("/Film Trivia Juego", methods=["GET", "POST"])
def juego():
    ahora = datetime.now()
    solo_fecha = ahora.strftime("%d/%m/%Y")

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
                        fecha=solo_fecha,
                        opcion_anterior=opcion_correcta(peli_correcta, peli_elegida),
                        peli_correcta=peli_correcta,
                    )
                else:
<<<<<<< HEAD
                    # Escribimos los resultados en un archivo solo una vez
                    escribir_resultados_archivo(
                        session["usuario"], session["num_aciertos"], intentos, solo_fecha
                    )

                    # Actualizar el gráfico de torta y el gráfico de curvas
                    graficar_intentos_vs_aciertos("data/resultados.txt", "static/graficos")
                    graficar_aciertos_vs_desaciertos_por_fecha("data/resultados.txt", "static/graficos")

                    # Limpiamos todos los valores de las claves de la sesión
=======
                    #escribimos los resultados en un archivo

                    escribir_resultados_archivo(session["usuario"],session["num_aciertos"],intentos,solo_fecha)
                    graficar_intentos_vs_aciertos(file_path, folder)
                    #eliminamos todos los valores de las claves de la sesion, de esta manera la proxima partida no contiene ningún dato de la anterior
>>>>>>> 8d7e4372524bae2515ef9fa65b48deecd1273235
                    session.clear()

                    # Redirigimos al historial
                    return redirect(url_for("historial"))
                    
    else:
        #Se devuelve la primera página de juego (primera ronda)
        ronda_actual = 1

        return render_template("juego.html", ronda=session["rondas"][ronda_actual-1],num_ronda = ronda_actual,aciertos = session["num_aciertos"], fecha = solo_fecha) 
    
@app.route("/historial", methods=["GET", "POST"])
def historial():
     juegos_data = leer_archivo_resultados()
     return render_template("resultados.html",juegos_data = juegos_data) 
 
@app.route("/graficos", methods=["GET"])
def graficos():
    # Ruta para mostrar el gráfico de torta
    return render_template("graficos.html", grafico_url=url_for('static', filename='graficos/grafico_torta_general.png'))

@app.route("/descargar_grafico", methods=["GET"])
def descargar_grafico():
    file_path = "static/graficos/grafico_torta_general.png"  # Ruta al gráfico
    return send_file(file_path, as_attachment=True)

@app.route("/descargar_grafico/<filename>", methods=["GET"])
def descargar_grafico2(filename):
    # Ruta al archivo de imagen
    image_path = os.path.join("static/graficos", filename)
    
    # Crear un archivo PDF temporal
    pdf_path = os.path.join("static/graficos", f"{os.path.splitext(filename)[0]}.pdf")
    with PdfPages(pdf_path) as pdf:
        # Leer la imagen y agregarla al PDF
        img = plt.imread(image_path)
        plt.figure(figsize=(8, 6))
        plt.imshow(img)
        plt.axis('off')  # Ocultar los ejes
        pdf.savefig()  # Guardar la figura en el PDF
        plt.close()

    # Enviar el archivo PDF al cliente
    return send_file(pdf_path, as_attachment=True)

     
if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True)
