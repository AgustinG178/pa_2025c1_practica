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
repo_usuarios, repo_ = crear_repositorio()
gestor_usuarios = GestorDeUsuarios(repo_usuarios)
gestor_login = GestorDeLogin(gestor_usuarios, login_manager, admin_list)

# Página de inicio
@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        nombre_de_usuario = request.form.get('nombre_de_usuario')
        password = request.form.get('password')
        rol = request.form.get('rol')
        try:
            gestor_usuarios.registrar_nuevo_usuario(
                nombre=nombre,
                apellido=apellido,
                email=email,
                nombre_de_usuario=nombre_de_usuario,
                password=password,
                rol=rol
            )
            flash('Usuario registrado exitosamente. Ahora puede iniciar sesión.', 'success')
            return redirect(url_for('iniciar_sesion'))
        except ValueError as e:
            flash(str(e), 'danger')
            return render_template('registrarse.html')
    return render_template('registrarse.html')

@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        usuario = gestor_usuarios.autenticar_usuario(email, password)
        if usuario:
            flash(f'Bienvenido, {usuario.nombre_de_usuario}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas. Intente nuevamente.', 'danger')
            return render_template('login.html')
    return render_template('login.html')
    
@app.route('/mis_reclamos')
def reclamos():
    return render_template('reclamos.html')

@app.route('/crear_reclamos')
def crear_reclamos():
    return render_template('usuarios.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)