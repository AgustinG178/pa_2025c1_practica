# Ejemplo de aplicación principal en Flask
from flask import render_template, flash, request, redirect, url_for
from flask import Flask
from modules.config import app, login_manager   
from modules.usuarios import Usuario
from modules.registrar import GestorDeUsuarios
from modules.login import GestorDeLogin
from modules.repositorio import RepositorioAbstracto, RepositorioUsuariosSQLAlchemy
from modules.BaseDeDatos import BaseDatos
from modules.factoria import crear_repositorio

admin_list = [1]
repo_libro, repo_usuario = crear_repositorio()
gestor_libros = GestorDeUsuarios(repo_libro)
gestor_usuarios = GestorDeUsuarios(repo_usuario)
gestor_login = GestorDeLogin(gestor_usuarios, login_manager, admin_list)

# Página de inicio
@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            gestor_usuarios.registrar_nuevo_usuario(nombre, email, password)
            flash('Usuario registrado exitosamente. Ahora puede iniciar sesión.', 'success')
            return redirect(url_for('iniciar_sesion'))
        except ValueError as e:
            flash(str(e), 'danger')
            return render_template('registrarse.html')
    return render_template('registrarse.html')

@app.route('/iniciar_sesion')
def iniciar_sesion():
    return render_template('login.html')
    
@app.route('/mis_reclamos')
def reclamos():
    return render_template('reclamos.html')

@app.route('/crear_reclamos')
def crear_reclamos():
    return render_template('usuarios.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)