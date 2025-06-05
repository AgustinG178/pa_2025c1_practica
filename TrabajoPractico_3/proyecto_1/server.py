from flask import render_template, flash, request, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from modules.config import app, login_manager, crear_engine   
from modules.repositorio import RepositorioUsuariosSQLAlchemy, RepositorioReclamosSQLAlchemy
from modules.gestor_usuario import GestorUsuarios
from modules.login import GestorLogin, FlaskLoginUser
from modules.gestor_reclamos import GestorReclamo 
from modules.BaseDeDatos import BaseDatos 

admin_list = [1]
base_datos = BaseDatos("sqlite:///data/base_datos.db")
base_datos.conectar()
Session = crear_engine()
sqlalchemy_session = Session()

repo_usuarios = RepositorioUsuariosSQLAlchemy(sqlalchemy_session)
repo_reclamos = RepositorioReclamosSQLAlchemy(sqlalchemy_session)
gestor_usuarios = GestorUsuarios(repo_usuarios)
gestor_login = GestorLogin(repo_usuarios)
gestor_reclamos = GestorReclamo(repo_reclamos)  

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
        try:
            gestor_usuarios.registrar_nuevo_usuario(
                nombre=nombre,
                apellido=apellido,
                email=email,
                nombre_de_usuario=nombre_de_usuario,
                password=password,
                claustro = 0,
                rol=0
            )
            flash('Usuario registrado exitosamente. ¡Ahora puede iniciar sesión!', 'success')
            return redirect(url_for('iniciar_sesion'))
        except ValueError as e:
            flash(str(e), 'danger')
    return render_template('registrarse.html')

@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        nombre_de_usuario = request.form.get('nombre_de_usuario')
        password = request.form.get('password')
        try:
            usuario = gestor_login.autenticar(nombre_de_usuario, password)
            print("Usuario autenticado:", usuario)
            login_user(FlaskLoginUser(usuario))
            print("Redirigiendo a inicio_usuario")  
            return redirect(url_for('inicio_usuario'))
        except ValueError as e:
            flash(str(e), 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('index'))

@app.route('/inicio_usuario')
@login_required
def inicio_usuario():
    return render_template('usuario_inicio.html', usuario=current_user)

@app.route('/mis_reclamos')
@login_required
def mis_reclamos():
    reclamos = repo_reclamos.obtener_reclamos(current_user.id)
    return render_template('mis_reclamos.html', usuario=current_user, reclamos=reclamos)

@app.route('/crear_reclamos', methods=['GET', 'POST'])
@login_required
def crear_reclamos():
    if request.method == 'POST':
        descripcion = request.form.get('descripcion')
        departamento = request.form.get('departamento')
        try:
            gestor_reclamos.crear_reclamo(
                usuario_id=current_user.id,
                descripcion=descripcion,
                departamento=departamento
            )
            flash('Reclamo creado exitosamente.', 'success')
            return redirect(url_for('mis_reclamos'))
        except Exception as e:
            flash(f'Error al crear el reclamo: {e}', 'danger')
    return render_template('crear_reclamo.html')

@app.route('/listar_reclamos')
@login_required
def listar_reclamos():
    reclamos = repo_reclamos.obtener_todos_los_reclamos()
    return render_template('listar_reclamos.html', reclamos=reclamos)

@login_manager.user_loader
def load_user(user_id):
    usuario = repo_usuarios.obtener_por_id(user_id)
    if usuario:
        return FlaskLoginUser(usuario)
    return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)