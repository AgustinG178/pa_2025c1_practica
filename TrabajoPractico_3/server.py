import flask
print(dir(flask))
from flask import render_template, flash, request, redirect, url_for
from flask import Flask
from flask_login import login_user, login_required, current_user
from modules.config import app, login_manager   
from modules.usuarios import Usuario, UsuarioFinal, JefeDepartamento, SecretarioTecnico, FlaskLoginUser
from modules.registrar import GestorDeUsuarios
from modules.login import GestorDeLogin
from modules.repositorio import RepositorioAbstracto, RepositorioUsuariosSQLAlchemy
from modules.BaseDeDatos import BaseDatos
from modules.factoria import crear_repositorio

admin_list = [1]
repo_usuarios, repo_ = crear_repositorio()
gestor_usuarios = GestorDeUsuarios(repo_usuarios)
gestor_login = GestorDeLogin(gestor_usuarios, login_manager, admin_list)

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
            flash('Usuario registrado exitosamente. ¡Ahora puede iniciar sesión!', 'success')
            return redirect(url_for('iniciar_sesion'))
        except ValueError as e:
            flash(str(e), 'danger')
            return render_template('registrarse.html')
    # Para GET, mostrar el formulario de registro
    return render_template('registrarse.html')

@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            usuario = gestor_usuarios.autenticar_usuario(email, password)
            from modules.login import FlaskLoginUser
            login_user(FlaskLoginUser(usuario))
            return redirect(url_for('inicio_usuario'))
        except ValueError as e:
            flash(str(e), 'danger')
            return render_template('inicio_sesion.html')
    # Para GET, mostrar el formulario de login
    return render_template('inicio_sesion.html')

@app.route('/inicio_usuario')
@login_required
def inicio_usuario():
    return render_template('usuario_inicio.html', usuario=current_user)    
    
@app.route('/mis_reclamos')
def reclamos():
     return render_template('reclamos.html')

@app.route('/crear_reclamos')
def crear_reclamos():
     return render_template('usuarios.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)