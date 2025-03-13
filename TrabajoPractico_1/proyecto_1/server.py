from flask import render_template
from modules.config import app

@app.route('/')
def index():
    cantidad = 32
    return render_template('inicio.html', una_cantidad = cantidad)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    