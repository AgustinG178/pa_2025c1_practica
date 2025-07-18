from modules.gestor_base_datos import GestorBaseDatos
from modules.repositorio import RepositorioUsuariosSQLAlchemy, RepositorioReclamosSQLAlchemy
from modules.gestor_usuario import GestorUsuarios
from modules.gestor_reclamos import GestorReclamo
from modules.config import crear_engine
from random import choice, randint, sample
from datetime import datetime, timedelta
"""
poblar_base.py

Script para poblar la base de datos con usuarios y reclamos de prueba.

Crea automáticamente:
- 4 usuarios de ejemplo
- 10 reclamos asociados a los usuarios

Útil para desarrollo y pruebas rápidas sin necesidad de ingresar datos manualmente.

Ejecutar con:
    python poblar_base.py

Solo para uso en entorno de desarrollo.
"""

# ─── Conexión ───────────────────────────────────────────────────────────────────
base_datos = GestorBaseDatos("sqlite:///docs/base_datos.db")
base_datos.conectar()
engine, Session = crear_engine()
session = Session()

repo_usuarios = RepositorioUsuariosSQLAlchemy(session)
repo_reclamos = RepositorioReclamosSQLAlchemy(session)

gestor_usuarios = GestorUsuarios(repo_usuarios)

gestor_reclamos = GestorReclamo(repo_reclamos)

import pickle

with open('./data/claims_clf.pkl', 'rb') as archivo:
  
  clf  = pickle.load(archivo)

# ─── Precarga ──────────────────────────────────────────────────────────────────
usuarios_info = [
    # Usuario 1: Estudiante
    {"nombre": "Esteban", "apellido": "Gómez", "email": "esteban@example.com", "usuario": "esteban", "rol": 0, "claustro": "Estudiante"},
    # Usuario 2: Soporte Informático (Docente)
    {"nombre": "Soledad", "apellido": "Ruiz", "email": "soporte@fiuner.edu.ar", "usuario": "soporte", "rol": 2, "claustro": "Docente"},
    # Usuario 3: Secretaría Técnica (Docente)
    {"nombre": "Sergio", "apellido": "Tech", "email": "secretaria@fiuner.edu.ar", "usuario": "secretaria", "rol": 3, "claustro": "Docente"},
    # Usuario 4: Maestranza (Docente)
    {"nombre": "Marta", "apellido": "Limpieza", "email": "maestranza@fiuner.edu.ar", "usuario": "maestranza", "rol": 4, "claustro": "Docente"},
    # Usuario 5: Sec. Técnico (PAYS)
    {"nombre": "Pablo", "apellido": "Ayudante", "email": "pays@fiuner.edu.ar", "usuario": "pays", "rol": 1, "claustro": "PAYS"},
]

reclamos_info = [
    "Hay goteras en el techo del aula 4",
    "No funciona la calefacción en la biblioteca",
    "Falta iluminación en el pasillo del módulo 2",
    "El baño al lado del departamento de electrónica está fuera de servicio",
    "Fuga de agua en el baño del decanato",
    "El ascensor de la biblioteca no funciona desde hace semanas",
    "Reclamo por ruido constante durante clases en el horario de fisiología",
    "El aire acondicionado del aula magna no enfría adecuadamente",
    "El sistema de ventilación del laboratorio de física está roto",
    "Una ventana del aula 6 está rota desde hace una semana",
    "Hay humedad en las paredes del aula 1",
    "El piso del pasillo principal está flojo y puede causar caídas",
    "El portón trasero no cierra bien y queda abierto durante la noche",
    "Las luces del estacionamiento no prenden de noche",
    "Faltan sillas en el aula 8",
    "Problemas con la conexión WiFi en los laboratorios",
    "El campus virtual no está funcionando correctamente",
    "No puedo acceder al sistema SIU Guaraní",
    "Los proyectores no funcionan en el aula 2 ni el aula magna",
    "El sistema de reservas de aulas no permite reservar el aula 3",
    "Los equipos del laboratorio de informática no encienden",
    "La impresora del departamento de alumnos no imprime",
    "El escáner de la biblioteca no está disponible",
    "No funciona el sistema de acceso con tarjetas",
    "Las computadoras del aula 10 están muy lentas",
    "No puedo entrar a mi correo institucional",
    "Fallo en la red Ethernet en el edificio de química",
    "El sistema de carga de notas no guarda los cambios",
    "No se puede acceder al servicio de VPN",
    "Faltan insumos en el laboratorio de química",
    "El servicio de limpieza no cumple con los horarios establecidos",
    "El servicio de cafetería no está funcionando correctamente",
    "Los bizcochos del kiosco están muy caros y no son de buena calidad",
    "La cantina no acepta pagos después de las 13 hs",
    "No hay papel higiénico en los baños del segundo piso",
    "Las máquinas expendedoras están vacías hace días",
    "La atención en el departamento de alumnos es muy lenta",
    "No atienden los teléfonos del departamento de ingeniería",
    "Se necesita personal de limpieza extra durante los exámenes",
    "Los horarios del comedor no se respetan",
    "No hay jabón en los baños del módulo 3",
    "Las fotocopiadoras no tienen tinta",
    "No hay formularios disponibles en ventanilla",
    "Los horarios publicados en la cartelera están desactualizados",
    "El proyector del aula 9 parpadea constantemente",
    "No hay señal de internet en el laboratorio de informática",
    "Las puertas del edificio principal no cierran bien",
    "Falta ventilación adecuada en el gimnasio",
    "Los baños no tienen papel higiénico ni jabón líquido",
    "El sistema de alarma de incendios se activa sin razón",
    "El ascensor del módulo B hace ruidos extraños",
    "Las luces del pasillo del tercer piso están quemadas",
    "No funciona el timbre de la entrada principal",
    "Los enchufes del aula 5 no tienen corriente",
    "El aire acondicionado del laboratorio de química gotea agua",
    "El sistema de reserva de salas a veces no confirma la reserva",
    "El proyector no conecta con la laptop en la sala de profesores",
    "El teclado de la computadora del aula 7 está roto",
    "Hay cables sueltos en el área de laboratorio de física",
    "Las ventanas del aula 3 no se pueden cerrar",
    "Falta iluminación en el estacionamiento trasero",
    "El servicio de limpieza no pasó por el comedor esta semana",
    "No hay jabón en los lavamanos del baño de damas",
    "El sistema de acceso con tarjeta no reconoce algunas credenciales"
]

# ─── Script Principal ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    for u in usuarios_info:
        try:
            rol = u.get("rol", 0)
            claustro = u.get("claustro", "Estudiante")
            
            gestor_usuarios.registrar_nuevo_usuario(
                nombre=u["nombre"],
                apellido=u["apellido"],
                email=u["email"],
                nombre_de_usuario=u["usuario"],
                password="1234",
                rol=rol,
                claustro=claustro,
            )
            print(f"✔ Usuario creado: {u['usuario']}")
        except Exception as e:
            print(f"✖ Usuario '{u['usuario']}' ya existe o error: {e}")

    usuarios_db = repo_usuarios.obtener_todos_los_registros()
    if not usuarios_db:
        print("✖ No se encontraron usuarios válidos para asignar reclamos.")
        exit()

    for i, desc in enumerate(reclamos_info):
        try:
            usuario = choice(usuarios_db)
            clasificacion = clf.clasificar([desc])[0]
            resuelto_en = randint(1, 30) if randint(0, 1) else None
            estado = "resuelto" if resuelto_en is not None else "pendiente"
            fecha_random = datetime.utcnow() - timedelta(days=randint(0, 60))

            reclamo = gestor_reclamos.crear_reclamo(
                usuario=usuario,
                descripcion=desc,
                clasificacion=clasificacion
            )

            modelo = repo_reclamos.mapear_reclamo_a_modelo(reclamo)
            modelo.estado = estado
            modelo.fecha_hora = fecha_random
            modelo.cantidad_adherentes = randint(0,35)
            modelo.tiempo_estimado = randint(1, 10) if estado == "pendiente" else 0
            modelo.resuelto_en = resuelto_en

            # Asignar adherentes aleatorios distintos del creador
            otros_usuarios = [u for u in usuarios_db if u.id != usuario.id]
            adherentes = sample(otros_usuarios, k=randint(0, min(5, len(otros_usuarios))))  # hasta 5 adherentes aleatorios
            modelo.usuarios = adherentes + [usuario]  # agrego creador también para que quede vinculado

            repo_reclamos.guardar_registro(modelo)
            print(f"✔ Reclamo [{estado}] creado para {usuario.nombre_de_usuario} en departamento: {desc} con {len(adherentes)} adherentes")
        except Exception as e:
            print(f"✖ Error creando reclamo '{desc}': {e}")


