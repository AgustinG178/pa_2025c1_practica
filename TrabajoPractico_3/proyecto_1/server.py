from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required, logout_user, current_user, login_user
from modules.config import app, login_manager, crear_engine   
from modules.repositorio import RepositorioUsuariosSQLAlchemy, RepositorioReclamosSQLAlchemy
from modules.gestor_usuario import GestorUsuarios
from modules.login import GestorLogin, FlaskLoginUser
from modules.gestor_reclamos import GestorReclamo 
from modules.BaseDeDatos import BaseDatos
from modules.classifier import Clasificador
from modules.preprocesamiento import ProcesadorArchivo
from sqlalchemy.exc import IntegrityError

admin_list = [1]
base_datos = BaseDatos("sqlite:///data/base_datos.db")
base_datos.conectar()
engine, Session = crear_engine()
sqlalchemy_session = Session()
repo_usuarios = RepositorioUsuariosSQLAlchemy(sqlalchemy_session)
repo_reclamos = RepositorioReclamosSQLAlchemy(sqlalchemy_session)
gestor_usuarios = GestorUsuarios(repo_usuarios)
gestor_login = GestorLogin(repo_usuarios)
procesador = ProcesadorArchivo("modules/clasificador_de_reclamos/data/frases.json")
X, y = procesador.datosEntrenamiento
clf = Clasificador(X, y)
clf._entrenar_clasificador()
gestor_reclamos = GestorReclamo(repo_reclamos, clf) 
 
@app.route('/')
def index():
    ultimos = repo_reclamos.obtener_ultimos_reclamos(limit=4)
    return render_template('inicio.html', ultimos_reclamos=ultimos)

@app.route('/inicio')
def inicio():
    ultimos = repo_reclamos.obtener_ultimos_reclamos(limit=4)
    return render_template('inicio.html', ultimos_reclamos=ultimos)

@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        nombre_de_usuario = request.form.get('nombre_de_usuario')
        password = request.form.get('password')

        print(f"[DEBUG] Datos recibidos -> nombre: {nombre}, apellido: {apellido}, email: {email}, usuario: {nombre_de_usuario}")

        try:
            print("[DEBUG] Intentando registrar nuevo usuario...")
            gestor_usuarios.registrar_nuevo_usuario(
                nombre=nombre,
                apellido=apellido,
                email=email,
                nombre_de_usuario=nombre_de_usuario,
                password=password,
                claustro=0,
                rol=0,
                id=None  # El ID se asigna automáticamente por la base de datos
            )
            print("[DEBUG] Usuario registrado exitosamente.")
            flash('Usuario registrado exitosamente. ¡Ahora puede iniciar sesión!', 'success')
            return redirect(url_for('iniciar_sesion'))
        except ValueError as e:
            print(f"[ERROR] Error al registrar usuario: {e}")
            flash(str(e), 'danger')
        except Exception as e:
            print(f"[ERROR] Error inesperado al registrar usuario: {e}")
            flash('Ocurrió un error inesperado. Por favor, inténtelo más tarde.', 'danger')
        except IntegrityError as e:
            print(f"[ERROR] Error de integridad: {e}")
            flash('El nombre de usuario o el email ya están en uso. Por favor, elija otro.', 'danger')
            sqlalchemy_session.rollback() #revierte o deshace todos los cambios realizados en la transacción actual que aún no se han confirmado (commit).

    return render_template('registrarse.html')

@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        nombre_de_usuario = request.form.get('nombre_de_usuario')
        password = request.form.get('password')
        print(f"Intentando login: {nombre_de_usuario} / {password}")
        try:
            gestor_login.autenticar(nombre_de_usuario, password)
            usuario = gestor_usuarios.cargar_usuario(nombre_de_usuario)
            print("Usuario cargado:", usuario)
            login_user(FlaskLoginUser(usuario))
            print("Usuario logueado con éxito, redirigiendo...")
            return redirect(url_for('index'))
        except Exception as e:
            print("Error en autenticación:", e)
            flash(str(e))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    print('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('index'))

@app.route('/inicio_usuario')
@login_required
def inicio_usuario():
    return render_template('inicio.html', usuario=current_user)

@app.route('/mis_reclamos')
@login_required
def mis_reclamos():
    reclamos = repo_reclamos.obtener_todos_los_registros(current_user.id)
    return render_template('mis_reclamos.html', usuario=current_user, reclamos=reclamos)

@app.route('/crear_reclamos', methods=['GET', 'POST'])
@login_required
def crear_reclamos():
    if request.method == 'POST':
        descripcion = request.form.get('descripcion')
        departamento = request.form.get('departamento')
        print(f"[DEBUG] Datos recibidos - Descripción: {descripcion}, Departamento: {departamento}")
        print(f"[DEBUG] Usuario actual: {current_user}")

        try:
            clasificacion_predicha = clf.clasificar([descripcion])[0]
            clasificacion_predicha_str = str(clasificacion_predicha)
            print(f"[DEBUG] Clasificación predicha: {clasificacion_predicha} ({type(clasificacion_predicha)})")

            reclamo = gestor_reclamos.crear_reclamo(
                usuario=current_user,
                descripcion=descripcion,
                departamento=departamento,
                clasificacion=clasificacion_predicha_str
            )
            print("[DEBUG] Reclamo creado con éxito.")

            modelo = repo_reclamos.mapear_reclamo_a_modelo(reclamo)
            repo_reclamos.guardar_registro(modelo)
            print("[DEBUG] Reclamo guardado en la base de datos.")

            # Buscar reclamos similares
            reclamos_similares = repo_reclamos.buscar_similares(clasificacion_predicha_str, modelo.id)

            # Redirigir a página de ultimo reclamo
            return render_template(
                'ultimo_reclamo.html',
                reclamo=modelo,
                similares=reclamos_similares
            )

        except Exception as e:
            print(f"[ERROR] Error al crear el reclamo: {e}")
            flash(f'Error al crear el reclamo: {e}', 'danger')

    print("[DEBUG] Método GET: mostrando formulario de creación de reclamos.")
    return render_template('crear_reclamo.html')

@app.route('/adherirse/<int:reclamo_id>', methods=['POST'])
@login_required
def adherirse(reclamo_id):
    usuario_actual = current_user.usuario_orm
    try:
        gestor_reclamos.agregar_adherente(reclamo_id, usuario_actual)
        flash("Te adheriste al reclamo correctamente.", "success")
    except ValueError as e:
        flash(str(e), "warning")
    except Exception as e:
        flash(f"Ocurrió un error inesperado: {e}", "danger")
    except IntegrityError as e:
        flash("Ya estás adherido a este reclamo.", "warning")
        sqlalchemy_session.rollback()
    return redirect(url_for('inicio_usuario'))

@app.route('/listar_reclamos')
@login_required
def listar_reclamos():
    reclamos = repo_reclamos.obtener_todos_los_registros()
    return render_template('listar_reclamos.html', reclamos=reclamos)

@login_manager.user_loader
def load_user(user_id):
    usuario = repo_usuarios.obtener_registro_por_filtro(campo='id', valor = user_id)
    if usuario:
        return FlaskLoginUser(usuario)
    return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)