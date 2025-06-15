from flask import render_template, flash, request, redirect, url_for, send_file, send_from_directory, abort
from flask_login import login_required, logout_user, current_user, login_user
from modules.config import app, login_manager, crear_engine   
from modules.repositorio import RepositorioUsuariosSQLAlchemy, RepositorioReclamosSQLAlchemy
from modules.gestor_usuario import GestorUsuarios
from modules.login import GestorLogin, FlaskLoginUser
from modules.gestor_reclamos import GestorReclamo 
from modules.gestor_base_datos import GestorBaseDatos
from sqlalchemy.exc import IntegrityError
from modules.monticulos import MonticuloMediana
from modules.reportes import GeneradorReportes, ReporteHTML, ReportePDF
from modules.graficos import Graficadora, GraficadoraTorta, GraficadoraHistograma, GraficadoraNubePalabras
from modules.gestor_imagen_reclamo import GestorImagenReclamoPng
import os
import datetime as date
from modules.monticulos import MonticuloMediana
import pickle

base_datos = GestorBaseDatos("sqlite:///data/base_datos.db")
base_datos.conectar()

engine, Session = crear_engine()
sqlalchemy_session = Session()

repo_usuarios = RepositorioUsuariosSQLAlchemy(sqlalchemy_session)
repo_reclamos = RepositorioReclamosSQLAlchemy(sqlalchemy_session)
gestor_usuarios = GestorUsuarios(repo_usuarios)
gestor_login = GestorLogin(repo_usuarios)
gestor_imagenes_reclamos = GestorImagenReclamoPng()

with open('./data/claims_clf.pkl', 'rb') as archivo:
  
  clf  = pickle.load(archivo)

gestor_reclamos = GestorReclamo(repo_reclamos)

@app.route('/')
def index():
    ultimos = repo_reclamos.obtener_ultimos_reclamos(limit=4)
    return render_template('inicio.html')

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

        try:
            gestor_usuarios.registrar_nuevo_usuario(
                nombre=nombre,
                apellido=apellido,
                email=email,
                nombre_de_usuario=nombre_de_usuario,
                password=password,
                rol=0,
                claustro="estudiante"
            )
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
    logout_user()
    return redirect(url_for('index'))

@app.route('/inicio_usuario')
@login_required
def inicio_usuario():
    return render_template('inicio.html', usuario=current_user)

@app.route('/mis_reclamos')
@login_required
def mis_reclamos():
    if current_user.rol == '1':
        reclamos = repo_reclamos.obtener_todos_los_reclamos_base()
    else:
        reclamos = repo_reclamos.obtener_todos_los_registros(current_user.id)
        
    return render_template('mis_reclamos.html', usuario=current_user, reclamos=reclamos, os=os)

@app.route('/crear_reclamos', methods=['GET', 'POST'])
@login_required
def crear_reclamos():
    if request.method == 'POST':
        descripcion = request.form.get('descripcion')
        
        try:
            clasificacion_predicha = clf.clasificar([descripcion])[0]
            reclamo = gestor_reclamos.crear_reclamo(
                usuario=current_user,
                descripcion=descripcion,
                clasificacion=str(clasificacion_predicha)
            )
            modelo = repo_reclamos.mapear_reclamo_a_modelo(reclamo)
            repo_reclamos.guardar_registro(modelo)
            sqlalchemy_session.refresh(modelo)
            imagen = request.files.get('imagen')
            reclamos_similares = repo_reclamos.buscar_similares(str(clasificacion_predicha), modelo.id)

            if imagen and imagen.filename:
                gestor_imagenes_reclamos.guardar_imagen(reclamo_id=modelo.id, imagen=imagen)
                return render_template('ultimo_reclamo.html', reclamo=modelo, similares=reclamos_similares)

            return render_template('ultimo_reclamo.html', reclamo=modelo, similares=reclamos_similares)
        except Exception as e:
            flash(f'Error al crear el reclamo: {e}', 'danger')

    return render_template('crear_reclamo.html')

@app.route('/adherirse/<int:reclamo_id>', methods=['POST'])
@login_required
def adherirse(reclamo_id):
    usuario_actual = current_user
    accion = request.form.get('accion')
    reclamo_id_adherido = reclamo_id
    reclamo_id_creado = request.form.get('reclamo_id_creado')

    if accion == "confirmar":
        flash("Reclamo creado exitosamente.", "success")
    elif accion == "adherir":
        try:
            gestor_reclamos.agregar_adherente(reclamo_id, usuario_actual)
            gestor_imagenes_reclamos.eliminar_imagen(reclamo_id=reclamo_id_creado)
            repo_reclamos.eliminar_registro_por_id(id=reclamo_id_creado)
            flash("Te adheriste al reclamo correctamente.", "success")
        except ValueError as e:
            flash(str(e), "warning")
        except Exception as e:
            flash(f"Ocurrió un error inesperado: {e}", "danger")
        except IntegrityError:
            flash("Ya estás adherido a este reclamo.", "warning")
            sqlalchemy_session.rollback()

    return redirect(url_for('inicio_usuario'))

@app.route('/listar_reclamos', methods=['GET', 'POST'])
@login_required
def listar_reclamos():
    """
    Lista todos los reclamos pendientes y permite aplicar filtros por departamento.
    """
    generador = GeneradorReportes(repo_reclamos)
    departamentos = generador.listar_clasificaciones_unicas()

    filtro_departamento = request.args.get('departamento', None)

    if filtro_departamento:
        reclamos = repo_reclamos.obtener_registros_por_filtro(filtro="clasificacion", valor=filtro_departamento)
    else:
        reclamos = repo_reclamos.obtener_registros_por_filtro(filtro="estado", valor="pendiente")

    return render_template(
        'listar_reclamos.html',
        reclamos=reclamos,
        departamentos=departamentos,
        filtro_departamento=filtro_departamento
    )
    
@app.route("/analitica")
@login_required
def analitica_reclamos():
    clasificacion_map = {
        "2": "soporte informatico",
        "3": "secretario tecnico",
        "4": "maestranza"
    }
    rol_usuario = current_user.rol
    clasificacion_usuario = clasificacion_map.get(rol_usuario)
    
    generador = GeneradorReportes(repo_reclamos)
    mediana_tiempo = generador.mediana_tiempo_resolucion()

    es_secretario = (rol_usuario == "1")

    generador = GeneradorReportes(repo_reclamos)
    graficadora = Graficadora(
        generador_reportes=generador,
        graficadora_torta=GraficadoraTorta(),
        graficadora_histograma=GraficadoraHistograma(),
        graficadora_nube=GraficadoraNubePalabras()
    )

    rutas = graficadora.graficar_todo(
        reclamos = repo_reclamos.obtener_todos_los_registros(usuario_id=2),
        clasificacion=clasificacion_usuario, 
        es_secretario_tecnico=es_secretario
    )

    cantidad_total = generador.cantidad_total_reclamos()
    promedio_adherentes = round(generador.cantidad_promedio_adherentes(), 2)

    reclamos_resueltos = repo_reclamos.obtener_registros_por_filtro(filtro="estado", valor="resuelto")

    tiempo_reclamos = [
        reclamo.resuelto_en for reclamo in reclamos_resueltos if reclamo.clasificacion == clasificacion_usuario
    ]
    
    # Solo los reclamos del departamento del usuario
    reclamos_departamento = repo_reclamos.obtener_registros_por_filtro(
        filtro="clasificacion", valor=clasificacion_usuario
    )

    monticulo = MonticuloMediana(tiempo_reclamos)

    return render_template(
        "analitica_reclamos.html",
        current_user=current_user,
        cantidad_total=cantidad_total,
        promedio_adherentes=promedio_adherentes,
        reclamos_departamento=reclamos_departamento,
        mediana_tiempo=mediana_tiempo,
        graficos=rutas,
        mediana=monticulo.obtener_mediana()
    )

@app.route('/descargar_reporte/<formato>')
@login_required
def descargar_reporte(formato):
    """
    Endpoint para descargar reportes en formato PDF o HTML.
    Filtra los reclamos según la clasificación del usuario.
    """
    # Mapeo de roles a clasificaciones
    clasificacion_map = {
        "2": "soporte informático",
        "3": "secretaría técnica",
        "4": "maestranza"
    }

    # Obtener el rol del usuario actual
    rol_usuario = current_user.rol
    clasificacion_usuario = clasificacion_map.get(rol_usuario)

    # Verificar si el usuario tiene una clasificación válida
    if not clasificacion_usuario:
        abort(403)  # Prohibido si el rol no está mapeado

    # Crear el generador de reportes
    generador = GeneradorReportes(repo_reclamos)

    # Lógica para generar y enviar el reporte
    if formato == 'pdf':
        # Ruta para guardar el PDF
        ruta_pdf = 'static/reporte_departamento.pdf'
        reporte_pdf = ReportePDF(generador)
        # Generar el PDF filtrado por clasificación
        reporte_pdf.generarPDF(ruta_pdf, clasificacion_usuario)
        # Enviar el archivo PDF como descarga
        return send_file(ruta_pdf, as_attachment=True)

    elif formato == 'html':
        # Ruta para guardar el HTML
        ruta_html = 'static/reporte_departamento.html'
        reporte_html = ReporteHTML(generador)
        # Generar el HTML filtrado por clasificación
        reporte_html.exportar_html(ruta_html, clasificacion_usuario)
        # Enviar el archivo HTML como descarga
        return send_file(ruta_html, as_attachment=True)

    else:
        # Si el formato no es válido, devolver un error 404
        abort(404)

@app.route('/editar_reclamo/<int:reclamo_id>', methods=['GET', 'POST'])
@login_required
def editar_reclamo(reclamo_id):
    modelo_reclamo = repo_reclamos.obtener_registro_por_filtro(filtro="id", valor=reclamo_id)
    accion = request.form.get("accion")
    if request.method == 'POST':

        nuevo_dpto = request.form.get("nuevo_dpto")
        nuevo_contenido = request.form.get('descripcion')
        imagen = request.files.get('imagen')

        if nuevo_dpto:

            modelo_reclamo.clasificacion = nuevo_dpto.lower()

            repo_reclamos.actualizar_reclamo(modelo_reclamo)

            flash('Reclamo derivado correctamente','success')

            return redirect(url_for('mis_reclamos'))
        try:
            nueva_clasificacion = clf.clasificar([nuevo_contenido])[0]
        except Exception as e:
            flash(f"Error al clasificar el contenido: {e}", "danger")
            return render_template("editar_reclamo.html", reclamo=modelo_reclamo)

        modelo_reclamo.contenido = nuevo_contenido
        modelo_reclamo.clasificacion = nueva_clasificacion

        try:
            repo_reclamos.modificar_registro_orm(repo_reclamos.mapear_reclamo_a_modelo(modelo_reclamo))

            if imagen and imagen.filename:
                try:
                    gestor_imagenes_reclamos.guardar_imagen(reclamo_id=reclamo_id, imagen=imagen)
                except Exception as e:
                    flash(f"Error al guardar la imagen: {e}", "warning")

            flash("Reclamo actualizado correctamente.", "success")
            return redirect(url_for('mis_reclamos'))

        except Exception as e:
            flash(f"Error al actualizar el reclamo: {e}", "danger")

    return render_template("editar_reclamo.html", reclamo=modelo_reclamo)

@app.route("/manejar_reclamos", methods=["GET", "POST"])
@login_required
def manejo_reclamos():
    rol = current_user.rol
    if rol not in ['1', '2', '3', '4']:
        flash("No tienes permisos para acceder.", "danger")
        return redirect(url_for('index'))

    reclamos = repo_reclamos.obtener_todos_los_registros(usuario_id=current_user.id)
    selected_id = None

    if request.method == "POST":
        selected_id = request.form.get('reclamo_id')
        accion = request.form.get('accion')
        reclamo = repo_reclamos.obtener_registro_por_filtro(filtro="id", valor=selected_id)
        try:
            if accion == "resolver":
                gestor_reclamos.actualizar_estado_reclamo(reclamo=reclamo, usuario=current_user, accion="resolver")
                flash("Reclamo resuelto exitosamente.", "success")
            elif accion == "actualizar":
                gestor_reclamos.actualizar_estado_reclamo(reclamo=reclamo, usuario=current_user, accion="actualizar")
                flash("Reclamo actualizado exitosamente.", "success")
            elif accion == "eliminar":
                gestor_reclamos.invalidar_reclamo(usuario=current_user, reclamo_id=selected_id)
                gestor_imagenes_reclamos.eliminar_imagen(reclamo_id=selected_id)
                flash("Reclamo eliminado exitosamente.", "success")
        except Exception as e:
            flash(f"Error al procesar el reclamo: {e}", "danger")

        dpto = current_user.rol_to_dpto

        reclamos = repo_reclamos.obtener_registros_por_filtros(filtro="clasificacion",valor=dpto)

    return render_template(
        'manejo_reclamos.html',
        reclamos=reclamos,
        usuario=current_user,
        selected_id=selected_id,
        date=date
    )

@app.route("/descargar_reporte_pdf")
def descargar_pdf():
    return send_from_directory(
        directory='data',
        path="salida_reporte_pdf",
        as_attachment=True
    )

@login_manager.user_loader
def load_user(user_id):
    usuario = repo_usuarios.obtener_registro_por_filtro(campo='id', valor=user_id)
    if usuario:
        return FlaskLoginUser(usuario)
    return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
