from flask import render_template, flash, request, redirect, url_for, send_file, abort
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

base_datos = GestorBaseDatos("sqlite:///docs/base_datos.db")
base_datos.conectar()

engine, Session = crear_engine()  # Session es el sessionmaker
sqlalchemy_session = Session() # sqlalchemy_session es una instancia de Session

repo_usuarios = RepositorioUsuariosSQLAlchemy(sqlalchemy_session)
repo_reclamos = RepositorioReclamosSQLAlchemy(sqlalchemy_session)
gestor_usuarios = GestorUsuarios(repo_usuarios)
gestor_login = GestorLogin(repo_usuarios)
gestor_imagenes_reclamos = GestorImagenReclamoPng()
reportes = GeneradorReportes(repo_reclamos)

with open('./data/claims_clf.pkl', 'rb') as archivo:
  
  clf  = pickle.load(archivo)

gestor_reclamos = GestorReclamo(repo_reclamos)

@app.route('/')
def index():
    ultimos = repo_reclamos.obtener_ultimos_reclamos(limit=4)
    return render_template('inicio.html')

@app.route('/inicio')
def inicio():
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
        reclamos = gestor_reclamos.devolver_reclamos_base(usuario=current_user)

    else:
        reclamos = gestor_reclamos.buscar_reclamos_por_filtro(filtro="usuario_id",valor=current_user.id)
        
    return render_template('mis_reclamos.html', usuario=current_user, reclamos=reclamos, os=os)

@app.route('/crear_reclamos', methods=['GET', 'POST'])
@login_required
def crear_reclamos():
    if request.method == 'POST':
        descripcion = request.form.get('descripcion')
        imagen = request.files.get('imagen')
        try:
            clasificacion_predicha = clf.clasificar([descripcion])[0]
            reclamo = gestor_reclamos.crear_reclamo(
                usuario=current_user,
                descripcion=descripcion,
                clasificacion=str(clasificacion_predicha)
            )

            gestor_reclamos.guardar_reclamo(reclamo=reclamo)
            
            #Ahora tomamos el reclamo de la bd para utilizar su id, es el ultimo creado

            reclamo_creado = gestor_reclamos.obtener_ultimos_reclamos(cantidad=1)[0]


            reclamos_similares = gestor_reclamos.buscar_reclamos_similares(descripcion=descripcion,clasificacion=clasificacion_predicha)

            if imagen and imagen.filename:
                gestor_imagenes_reclamos.guardar_imagen(reclamo_id=reclamo_creado.id, imagen=imagen)
                return render_template('ultimo_reclamo.html', reclamo=reclamo_creado, similares=reclamos_similares)

            return render_template('ultimo_reclamo.html', reclamo=reclamo_creado, similares=reclamos_similares)
        except Exception as e:
            flash(f'Error al crear el reclamo: {e}', 'danger')

    return render_template('crear_reclamo.html')

@app.route('/adherirse/<int:reclamo_id_adherido>', methods=['POST'])
@login_required
def adherirse(reclamo_id_adherido):
    usuario_actual = current_user
    accion = request.form.get('accion')
    reclamo_id_adherido = reclamo_id_adherido
    reclamo_id_creado = request.form.get('reclamo_id_creado')

    if accion == "confirmar":
        flash("Reclamo creado exitosamente.", "success")
    elif accion == "adherir":
        try:
            usuario_a_adherirse = gestor_usuarios.buscar_usuario(filtro="id",valor=current_user.id,mapeo=False)
            gestor_reclamos.agregar_adherente(usuario=usuario_a_adherirse,reclamo_id=reclamo_id_adherido)
            # Eliminar imagen solo si existe el archivo

            ruta_imagen = os.path.join('static', 'Imagenes Reclamos', f"{reclamo_id_creado}.png")

            if os.path.exists(ruta_imagen):
                gestor_imagenes_reclamos.eliminar_imagen(reclamo_id=reclamo_id_creado)

            gestor_reclamos.guardar_reclamo(reclamo_id=reclamo_id_creado)

            flash("Te adheriste al reclamo correctamente.", "success")
        except ValueError as e:
            flash(str(e), "warning")
        except Exception as e:
            flash("Te adheriste al reclamo correctamente.", "success")
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
    """
    Genera la analítica de reclamos según el rol del usuario.
    """
    clasificacion_map = {
        "2": "soporte informático",
        "3": "secretaría técnica",
        "4": "maestranza"
    }

    rol = str(current_user.rol)
    clasificacion_usuario = clasificacion_map.get(rol)
    es_secretario = rol == "1"

    if es_secretario:
        reclamos = repo_reclamos.obtener_todos_los_registros()
    elif clasificacion_usuario:
        reclamos = repo_reclamos.obtener_registros_por_filtro(filtro="clasificacion", valor=clasificacion_usuario)
    else:
        reclamos = []

    cantidad_total = len(reclamos)
    promedio_adherentes = round(
        sum(r.cantidad_adherentes for r in reclamos if r.cantidad_adherentes) / cantidad_total, 2
    ) if cantidad_total > 0 else 0
    tiempos_resolucion = [r.resuelto_en for r in reclamos if r.resuelto_en]

    if tiempos_resolucion:
        monticulo = MonticuloMediana(tiempos_resolucion)
        mediana = monticulo.obtener_mediana()
    else:
        mediana = 0

    graficadora = Graficadora(
        generador_reportes=GeneradorReportes(repo_reclamos),
        graficadora_torta=GraficadoraTorta(),
        graficadora_histograma=GraficadoraHistograma(),
        graficadora_nube=GraficadoraNubePalabras()
    )

    rutas = graficadora.graficar_todo(
        reclamos=reclamos,
        clasificacion=clasificacion_usuario,
        es_secretario_tecnico=es_secretario
    )

    return render_template(
        'analitica_reclamos.html',
        cantidad_total=cantidad_total,
        promedio_adherentes=promedio_adherentes,
        mediana=mediana,
        ruta_nube=rutas.get("nube_palabras"),
        ruta_histograma=rutas.get("histograma"),
        ruta_torta=rutas.get("torta"),
        departamento_usuario=clasificacion_usuario or "Todos",
        reclamos=reclamos
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

    rol_usuario = current_user.rol
    clasificacion_usuario = clasificacion_map.get(rol_usuario)

    if not clasificacion_usuario:
        abort(403)  # Prohibido si el rol no está mapeado

    generador = GeneradorReportes(repo_reclamos)

    if formato == 'pdf':
        ruta_pdf = 'static/reporte_departamento.pdf'
        reporte_pdf = ReportePDF(generador)
        reporte_pdf.generar(ruta_pdf, clasificacion_usuario)
        return send_file(ruta_pdf, as_attachment=True)

    elif formato == 'html':
        ruta_html = 'static/reporte_departamento.html'
        reporte_html = ReporteHTML(generador)
        reporte_html.generar(ruta_html, clasificacion_usuario)
        return send_file(ruta_html, as_attachment=True)

    else:
        abort(404)

@app.route('/editar_reclamo/<int:reclamo_id>', methods=['GET', 'POST'])
@login_required
def editar_reclamo(reclamo_id):

    reclamo = gestor_reclamos.devolver_reclamo(reclamo_id=reclamo_id)
    print(type(reclamo))

    accion = request.form.get("accion")
    nuevo_dpto = request.form.get("nuevo_dpto")
    nuevo_contenido = request.form.get('descripcion')
    imagen = request.files.get('imagen')

    if request.method == 'POST':

        

        if nuevo_dpto:

            reclamo.clasificacion = nuevo_dpto.lower()

            gestor_reclamos.modificar_reclamo(reclamo_modificado=reclamo)


            flash('Reclamo derivado correctamente','success')

            return redirect(url_for('mis_reclamos'))
        

        elif nuevo_contenido:

            try:

                nueva_clasificacion = clf.clasificar([nuevo_contenido])[0]
                reclamo.contenido = nuevo_contenido
                reclamo.clasificacion = nueva_clasificacion

                gestor_reclamos.modificar_reclamo(reclamo_modificado=reclamo)

                if imagen and imagen.filename:
                    try:
                        gestor_imagenes_reclamos.guardar_imagen(reclamo_id=reclamo_id, imagen=imagen)
                    except Exception as e:
                        flash(f"Error al guardar la imagen: {e}", "warning")


                flash("Reclamo actualizado correctamente.", "success")
                return redirect(url_for('mis_reclamos'))
            
            except Exception as e:
                flash(f"Error al modificar el reclamo: {e}", "danger")


    return render_template("editar_reclamo.html", reclamo=reclamo)

@app.route("/manejar_reclamos", methods=["GET", "POST"])
@login_required
def manejo_reclamos():
    
    rol_to_dpto = {
        "2": "soporte informático",
        "3": "secretaría técnica",
        "4": "maestranza"
    }
    
    rol = current_user.rol
    dpto = current_user.rol_to_dpto()

    if rol not in ['1', '2', '3', '4']:
        flash("No tienes permisos para acceder.", "danger")
        return redirect(url_for('index'))

    reclamos = gestor_reclamos.buscar_reclamos_por_filtro(filtro="clasificacion",valor=dpto)
    selected_id = None

    if request.method == "POST":
        selected_id = request.form.get('reclamo_id')
        accion = request.form.get('accion')
        tiempo_estimado = request.form.get('tiempo_estimado')
        reclamo = gestor_reclamos.devolver_reclamo(reclamo_id=selected_id)

        

        try:
            if accion == "resolver":
                gestor_reclamos.actualizar_estado_reclamo(reclamo=reclamo, usuario=current_user, accion="resolver")
                flash("Reclamo resuelto exitosamente.", "success")
                
            elif accion == "actualizar" and tiempo_estimado:
                if reclamo.estado == "en proceso":
                    flash("El reclamo ya se encuentra en proceso","danger")
                else:

                    gestor_reclamos.actualizar_estado_reclamo(reclamo=reclamo, usuario=current_user, accion="actualizar",tiempo_estimado=tiempo_estimado)
                    flash("Reclamo actualizado exitosamente.", "success")
            elif accion == "actualizar" and not tiempo_estimado:
                flash("El tiempo estimado es obligatorio para pasar un reclamo de pendiente --> en proceso","danger")

            elif accion == "invalidar":
                gestor_reclamos.invalidar_reclamo( reclamo_id=selected_id)
                import os
                ruta_imagen = os.path.join('static', 'Imagenes Reclamos', f"{selected_id}.png")
                if os.path.exists(ruta_imagen):
                    gestor_imagenes_reclamos.eliminar_imagen(reclamo_id=selected_id)
                flash("Reclamo eliminado exitosamente.", "success")


        except Exception as e:
            flash(f"Error al procesar el reclamo: {e}", "danger")

        try:
            reclamos = gestor_reclamos.buscar_reclamos_por_filtro(filtro="clasificacion", valor=dpto)
        except Exception as e:
            flash("Hubo un error al obtener los reclamos: " + str(e), "danger")
            reclamos = []

    return render_template(
        'manejo_reclamos.html',
        reclamos=reclamos,
        usuario=current_user,
        selected_id=selected_id,
        date=date
    )
    
@app.route('/ayuda')
@login_required
def ayuda():
    """
    Muestra una página de ayuda con un tutorial o guía de uso del sistema.
    """
    return render_template('ayuda.html', current_user=current_user)

@login_manager.user_loader

def load_user(user_id):
    usuario = gestor_usuarios.buscar_usuario(filtro="id",valor=user_id)
    if usuario:
        return FlaskLoginUser(usuario)
    return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
