from flask import render_template, request, session
from modules.config import app
from modules.modulos import juego_opciones, frases, opcion_correcta

@app.route('/')
def index():   
    session.pop("num_aciertos",None) 
    return render_template('inicio.html')

@app.route("/Film Trivia Juego", methods=["GET", "POST"])
def dificil():
    if "num_aciertos" not in session:
        session["num_aciertos"] = 0
    
    try: 
        juego = juego_opciones(frases, 10)
        if request.method == "POST":

            peli_correcta = request.form["peli_correcta"]
            peli_elegida = request.form["respuesta"]
            
            if opcion_correcta(peli_correcta,peli_elegida) == True: 
                  session["num_aciertos"] +=1
                
            return render_template("juego.html", juego=juego, resultado = request.method == "POST", aciertos = session["num_aciertos"])
            #session mantiene el estado de la variable aciertos entre solicitudes, es decir, cuando se llama nuevamente a def dificil,
            #se mantiene la cantidad de aciertos

        
        return render_template("juego.html", juego=juego,aciertos = 0) #devulve la primera pagina
    except IndexError:
        return render_template('inicio.html',frases=frases)

    
if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True)
