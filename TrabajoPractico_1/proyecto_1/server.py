from flask import render_template, request, session,redirect,url_for
from modules.config import app
from modules.modulos import juego_opciones, frases, opcion_correcta, escribir_resultados_archivo, leer_archivo_resultados
from datetime import datetime

@app.route("/",methods=["GET","POST"])
def index():   
    if request.method == "POST":
    
        session["usuario"] = request.form.get("input_usuario")
        session["intentos"] = int(request.form.get("input_intentos"))

        return redirect(url_for("juego"))
    
    else:
        session.pop("num_aciertos",None)
        session.pop("input_usuario",None)
        session.pop("input_intentos",None)

        return render_template('inicio.html')

@app.route("/Film Trivia Juego", methods=["GET", "POST"])
def juego():
    ahora = datetime.now()
    solo_fecha = ahora.strftime("%d/%m/%Y")

    if "num_aciertos" not in session:
        session["num_aciertos"] = 0

    intentos = session["intentos"]
    juego = juego_opciones(frases, intentos)
    
    
    if request.method == "POST":
                
                ronda_actual = int(request.form.get("ronda_actual",0)) + 1 #actualiza el valor de la ronda

                if ronda_actual < len(juego) + 1:
                    peli_correcta = request.form["peli_correcta"]
                    peli_elegida = request.form["respuesta"]
                    session["num_aciertos"] += opcion_correcta(peli_correcta,peli_elegida)
                        
                    return render_template("juego.html", ronda = juego[ronda_actual-1],num_ronda = ronda_actual, resultado = request.method == "POST", aciertos = session["num_aciertos"], fecha = solo_fecha, opcion_anterior = opcion_correcta(peli_correcta,peli_elegida),peli_correcta = peli_correcta)

                    
                    #session mantiene el estado de la variable aciertos entre solicitudes, es decir, cuando se llama nuevamente a def dificil,
                    #se mantiene la cantidad de aciertos
                
                else:
                    escribir_resultados_archivo(session["usuario"],session["num_aciertos"],intentos,solo_fecha)
                    return render_template("inicio.html")
                     
    else:
        ronda_actual = 1
    
        return render_template("juego.html", ronda=juego[ronda_actual-1],num_ronda = ronda_actual,aciertos = session["num_aciertos"], fecha = solo_fecha) #devulve la primera pagina
    
@app.route("/historial", methods=["GET", "POST"])
def historial():
     juegos_data = leer_archivo_resultados()
     return render_template("resultados.html",juegos_data = juegos_data)
     
if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True)
