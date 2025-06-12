from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required, logout_user, current_user, login_user
from modules.config import app, login_manager, crear_engine   
from modules.repositorio import RepositorioUsuariosSQLAlchemy, RepositorioReclamosSQLAlchemy
from modules.gestor_usuario import GestorUsuarios
from modules.login import GestorLogin, FlaskLoginUser
from modules.gestor_reclamos import GestorReclamo 
from modules.gestor_base_datos import GestorBaseDatos
from modules.classifier import Clasificador
from modules.preprocesamiento import ProcesadorArchivo
from sqlalchemy.exc import IntegrityError
from modules.reportes import GeneradorReportes
from modules.graficos import Graficadora, GraficadoraTorta, GraficadoraHistograma
from modules.gestor_imagen_reclamo import GestorImagenReclamoPng
import os
# Inicialización de componentes del sistema

""" Conexión con la base de datos """
base_datos = GestorBaseDatos("sqlite:///data/base_datos.db")
base_datos.conectar()

""" Configuración de SQLAlchemy """
engine, Session = crear_engine()
sqlalchemy_session = Session()

""" Repositorios y gestores """
repo_usuarios = RepositorioUsuariosSQLAlchemy(sqlalchemy_session)
repo_reclamos = RepositorioReclamosSQLAlchemy(sqlalchemy_session)
gestor_usuarios = GestorUsuarios(repo_usuarios)
gestor_login = GestorLogin(repo_usuarios)
gestor_imagenes_reclamos = GestorImagenReclamoPng()
"""Procesamiento del archivo JSON y entrenamiento del clasificador"""
procesador = ProcesadorArchivo("data/frases.json")
X, y = procesador.datosEntrenamiento
clf = Clasificador(X, y)
clf._entrenar_clasificador()

"""Gestor principal de reclamos """
gestor_reclamos = GestorReclamo(repo_reclamos, clf)

# Inicialización de la aplicación
"""logica principal del server"""
@app.route('/')
def index():
    """
    Página principal del sitio. Muestra los últimos reclamos ingresados.
    """
    ultimos = repo_reclamos.obtener_ultimos_reclamos(limit=4)
    return render_template('inicio.html', ultimos_reclamos=ultimos, current_user=current_user)


@app.route('/inicio')
def inicio():
    """
    Alias de la página principal. También muestra los últimos reclamos.
    """
    ultimos = repo_reclamos.obtener_ultimos_reclamos(limit=4)
    return render_template('inicio.html', ultimos_reclamos=ultimos)


@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    """
    Página de registro de nuevos usuarios. Muestra el formulario y lo procesa si es POST.
    """
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
                rol=0,  # Rol por defecto: estudiante
                claustro="estudiante"
            )
            print("[DEBUG] Usuario registrado exitosamente.")
            flash('Usuario registrado exitosamente. ¡Ahora puede iniciar sesión!', 'success')
            return redirect(url_for('iniciar_sesion'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash('Ocurrió un error inesperado. Por favor, inténtelo más tarde.', 'danger')
        except IntegrityError:
            flash('El nombre de usuario o el email ya están en uso.', 'danger')
            sqlalchemy_session.rollback()

    return render_template('registrarse.html')


@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    """
    Página de inicio de sesión. Verifica credenciales del usuario.
    """
    if request.method == 'POST':
        nombre_de_usuario = request.form.get('nombre_de_usuario')
        password = request.form.get('password')
        try:
            gestor_login.autenticar(nombre_de_usuario, password)
            usuario = gestor_usuarios.cargar_usuario(nombre_de_usuario)
            login_user(FlaskLoginUser(usuario))
            return redirect(url_for('index'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """
    Cierra la sesión del usuario actual.
    """
    logout_user()
    return redirect(url_for('index'))

@app.route('/inicio_usuario')
@login_required
def inicio_usuario():
    """
    Página de inicio personalizada para el usuario autenticado.
    """
    return render_template('inicio.html', usuario=current_user)

@app.route('/mis_reclamos')
@login_required
def mis_reclamos():
    """
    Muestra todos los reclamos realizados por el usuario actual.
    """
    reclamos = repo_reclamos.obtener_todos_los_registros(current_user.id)
    return render_template('mis_reclamos.html', usuario=current_user, reclamos=reclamos,os=os)

@app.route('/crear_reclamos', methods=['GET', 'POST'])
@login_required
def crear_reclamos():
    """
    Permite al usuario crear un nuevo reclamo.
    Si se envía el formulario (POST), predice la clasificación y busca similares.
    """
    if request.method == 'POST':
        descripcion = request.form.get('descripcion')
        departamento = request.form.get('departamento')
        
        try:
            clasificacion_predicha = clf.clasificar([descripcion])[0]
            reclamo = gestor_reclamos.crear_reclamo(
                usuario=current_user,
                descripcion=descripcion,
                departamento=departamento,
                clasificacion=str(clasificacion_predicha)
            )
            modelo = repo_reclamos.mapear_reclamo_a_modelo(reclamo)
            #Provisoriamente guardamos el reclamo en la bd, si posteriormente se adhiere a otro el usuario, lo borramos, lo mismo con la imagen si es que se adjunta una
            repo_reclamos.guardar_registro(modelo)
            
            sqlalchemy_session.refresh(modelo)
            imagen = request.files.get('imagen')
            reclamos_similares = repo_reclamos.buscar_similares(str(clasificacion_predicha), modelo.id)

            if imagen and imagen.filename:

                gestor_imagenes_reclamos.guardar_imagen(reclamo_id=modelo.id,imagen=imagen)

                return render_template('ultimo_reclamo.html', reclamo=modelo, similares=reclamos_similares)
            

            return render_template('ultimo_reclamo.html', reclamo=modelo, similares=reclamos_similares)
        except Exception as e:
            flash(f'Error al crear el reclamo: {e}', 'danger')

    return render_template('crear_reclamo.html')

@app.route('/adherirse/<int:reclamo_id>', methods=['POST'])
@login_required
def adherirse(reclamo_id):
    """
    Permite al usuario confirmar o adherirse a un reclamo existente.
    """
    usuario_actual = current_user
    print(f"[DEBUG] Entrando a adherirse con reclamo_id: {reclamo_id}")
    print(f"[DEBUG] Usuario actual: {usuario_actual}")
    print(f"[DEBUG] Form data: {request.form}")
    accion = request.form.get('accion')
    print(f"[DEBUG] Acción seleccionada: {accion}")

    #Ids de los reclamos, tanto el creado como el adherido (si es que se adhirio a uno)
    reclamo_id_adherido = reclamo_id
    reclamo_id_creado = request.form.get('reclamo_id_creado')
    print(f"[DEBUG] reclamo_id_adherido: {reclamo_id_adherido}, reclamo_id_creado: {reclamo_id_creado}")

    if accion == "confirmar":
        print("[DEBUG] Confirmando reclamo, no se elimina nada.")
        flash("Reclamo creado exitosamente.", "success")
    elif accion == "adherir":
        print("[DEBUG] Adhiriendo a reclamo existente. Ejecutando lógica de adhesión...")
        try:
            gestor_reclamos.agregar_adherente(reclamo_id, usuario_actual)
            print(f"[DEBUG] Adherente agregado a reclamo {reclamo_id}")
            gestor_imagenes_reclamos.eliminar_imagen(reclamo_id=reclamo_id_creado)
            print(f"[DEBUG] Imagen eliminada para reclamo creado {reclamo_id_creado}")
            repo_reclamos.eliminar_registro_por_id(id=reclamo_id_creado)
            print(f"[DEBUG] Reclamo creado {reclamo_id_creado} eliminado de la base de datos")
            flash("Te adheriste al reclamo correctamente.", "success")
        except ValueError as e:
            print(f"[DEBUG] ValueError: {e}")
            flash(str(e), "warning")
        except Exception as e:
            print(f"[DEBUG] Exception: {e}")
            flash(f"Ocurrió un error inesperado: {e}", "danger")
        except IntegrityError:
            print("[DEBUG] IntegrityError: Ya estás adherido a este reclamo.")
            flash("Ya estás adherido a este reclamo.", "warning")
            sqlalchemy_session.rollback()

    return redirect(url_for('inicio_usuario'))

@app.route('/listar_reclamos')
@login_required
def listar_reclamos():
    """
    Muestra todos los reclamos registrados en el sistema.
    """
    reclamos = repo_reclamos.obtener_todos_los_registros(current_user.id)
    return render_template('listar_reclamos.html', reclamos=reclamos)

@app.route("/analitica")
@login_required
def analitica_reclamos():
    """
    Muestra gráficos y estadísticas de reclamos según el rol del usuario.
    """
    clasificacion_map = {
        "2": "soporte informatico",
        "3": "secretario tecnico",
        "4": "maestranza"
    }

    rol_usuario = current_user.rol
    clasificacion_usuario = clasificacion_map.get(rol_usuario)
    es_secretario = (rol_usuario == "1")

    generador = GeneradorReportes(repo_reclamos)
    graficadora = Graficadora(generador, GraficadoraTorta(), GraficadoraHistograma())
    rutas = graficadora.graficar_todo(clasificacion=clasificacion_usuario, es_secretario_tecnico=es_secretario)

    cantidad_total = generador.cantidad_total_reclamos()
    promedio_adherentes = round(generador.cantidad_promedio_adherentes(), 2)

    return render_template(
        "analitica_reclamos.html",
        current_user=current_user,
        cantidad_total=cantidad_total,
        promedio_adherentes=promedio_adherentes,
        graficos=rutas
    )
    
@app.route('/editar_reclamo/<int:reclamo_id>', methods=['GET', 'POST'])
@login_required
def editar_reclamo(reclamo_id):
    print(f"[DEBUG] Entrando a /editar_reclamo con ID: {reclamo_id}")
    modelo_reclamo = repo_reclamos.obtener_registro_por_filtro(filtro="id", valor=reclamo_id)
    print(f"[DEBUG] Reclamo obtenido: {modelo_reclamo}")

    if request.method == 'POST':
        nuevo_contenido = request.form.get('descripcion')
        imagen = request.files.get('imagen')
        print(f"[DEBUG] Contenido recibido del formulario: {nuevo_contenido}")

        try:
            nueva_clasificacion = clf.clasificar([nuevo_contenido])[0]
            print(f"[DEBUG] Clasificación predicha: {nueva_clasificacion}")
        except Exception as e:
            print(f"[ERROR] Falló la clasificación: {e}")
            flash(f"Error al clasificar el contenido: {e}", "danger")
            return render_template("editar_reclamo.html", reclamo=modelo_reclamo)

        # Actualizamos el reclamo
        modelo_reclamo.contenido = nuevo_contenido
        modelo_reclamo.clasificacion = nueva_clasificacion

        try:
            repo_reclamos.modificar_registro_orm(repo_reclamos.mapear_reclamo_a_modelo(modelo_reclamo))

            # Manejo de imagen
            if imagen and imagen.filename:
                try:
                    gestor_imagenes_reclamos.guardar_imagen(reclamo_id=reclamo_id, imagen=imagen, reemplazar=True)
                    print(f"[DEBUG] Imagen reemplazada exitosamente.")
                except Exception as e:
                    print(f"[ERROR] Falló al guardar la imagen: {e}")
                    flash(f"Error al guardar la imagen: {e}", "warning")

            flash("Reclamo actualizado correctamente.", "success")
            return redirect(url_for('mis_reclamos'))

        except Exception as e:
            print(f"[ERROR] Falló al guardar el reclamo: {e}")
            flash(f"Error al actualizar el reclamo: {e}", "danger")

    return render_template("editar_reclamo.html", reclamo=modelo_reclamo)

@app.route("/manejar_reclamos", methods=["GET", "POST"])
@login_required
def manejo_reclamos():
    rol = current_user.rol
    if rol not in ['1','2','3','4']:
        flash("No tienes permisos para acceder.","danger")
        return redirect(url_for('index'))

    # traigo todos los reclamos
    reclamos = repo_reclamos.obtener_todos_los_registros(usuario_id=current_user.id)
    selected_id = None

    if request.method == "POST":
        selected_id = request.form.get('reclamo_id')
        accion = request.form.get('accion')
        reclamo = repo_reclamos.obtener_registro_por_filtro(filtro="id", valor=selected_id)
        try:
            if accion == "resolver":
                gestor_reclamos.actualizar_estado_reclamo(reclamo=reclamo, usuario=current_user, accion="resolver")
                flash("Reclamo resuelto exitosamente.","success")
            elif accion == "actualizar":
                gestor_reclamos.actualizar_estado_reclamo(reclamo=reclamo, usuario=current_user, accion="actualizar")
                flash("Reclamo actualizado exitosamente.","success")
            elif accion == "eliminar":
                gestor_reclamos.invalidar_reclamo(usuario=current_user, reclamo_id=selected_id)
                gestor_imagenes_reclamos.eliminar_imagen(reclamo_id=selected_id)
                flash("Reclamo eliminado exitosamente.","success")
        except Exception as e:
            flash(f"Error al procesar el reclamo: {e}","danger")

        # recargo la lista
        reclamos = repo_reclamos.obtener_todos_los_registros(usuario_id=current_user.id)

    return render_template(
        'manejo_reclamos.html',
        reclamos=reclamos,
        usuario=current_user,
        selected_id=selected_id
    )

@login_manager.user_loader
def load_user(user_id):
    """
    Carga un usuario desde la base de datos por su ID para integrarlo con Flask-Login.

    Args:
        user_id (int): ID del usuario a cargar.

    Returns:
        FlaskLoginUser | None: Objeto de sesión si se encuentra el usuario, None si no.
    """
    usuario = repo_usuarios.obtener_registro_por_filtro(campo='id', valor=user_id)
    if usuario:
        return FlaskLoginUser(usuario)
    return None

if __name__ == "__main__":
    # Inicia el servidor Flask en modo desarrollo.
    app.run(host="0.0.0.0", debug=True)
