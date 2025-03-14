from flask import render_template
from modules.config import app

@app.route('/')
def index():
    return render_template('inicio.html')

"""@app.route("/Juego")
def index():
    return render_template("Pagina1.html")"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    