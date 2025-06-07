from modules.BaseDeDatos import BaseDatos
from modules.repositorio import RepositorioUsuariosSQLAlchemy, RepositorioReclamosSQLAlchemy
from modules.gestor_usuario import GestorUsuarios
from modules.gestor_reclamos import GestorReclamo
from modules.classifier import Clasificador
from modules.preprocesamiento import ProcesadorArchivo
from modules.config import crear_engine
from random import choice
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
base_datos = BaseDatos("sqlite:///data/base_datos.db")
base_datos.conectar()
engine, Session = crear_engine()
session = Session()

repo_usuarios = RepositorioUsuariosSQLAlchemy(session)
repo_reclamos = RepositorioReclamosSQLAlchemy(session)

gestor_usuarios = GestorUsuarios(repo_usuarios)
procesador = ProcesadorArchivo("modules/clasificador_de_reclamos/data/frases.json")
X, y = procesador.datosEntrenamiento

clf = Clasificador(X, y)
clf._entrenar_clasificador()

gestor_reclamos = GestorReclamo(repo_reclamos, clf)

# ─── Precarga ──────────────────────────────────────────────────────────────────
usuarios_info = [
    {"nombre": "Ana", "apellido": "García", "email": "ana@example.com", "usuario": "ana"},
    {"nombre": "Juan", "apellido": "Pérez", "email": "juan@example.com", "usuario": "juan"},
    {"nombre": "Laura", "apellido": "López", "email": "laura@example.com", "usuario": "laura"},
    {"nombre": "Carlos", "apellido": "Martínez", "email": "carlos@example.com", "usuario": "carlos"},
]

reclamos_info = [
    "Hay goteras en el techo del aula 4",
    "No funciona la calefacción en la biblioteca",
    "Falta iluminación en el pasillo del modulo 2",
    "El baño al lado del departamento de electronica está fuera de servicio",
    "Problemas con la conexión WiFi en los laboratorios",
    "Falta insumos en el laboratorio de química",
    "El proyector del aula 2 no funciona",
    "Fuga de agua en el baño del decanato",
    "El ascensor de la bilbioteca no funciona desde hace semanas",
    "Reclamo por ruido constante durante clases en el horario de fiosologia",
    "El aire acondicionado del aula magna no enfría adecuadamente",
    "El campus no está funcionando correctamente",
    "El sistema de reservas de aulas no permite reservar el aula 3",
    "El servicio de limpieza no está cumpliendo con los horarios establecidos",
    "El servicio de cafetería no está funcionando correctamente",
    "Los buzcochos del kiosco estan muy caros y no son de buena calidad",
    "La cantina no me acepta pagar despues de las 13 hs"
]

# ─── Script Principal ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Crear usuarios
    for u in usuarios_info:
        try:
            gestor_usuarios.registrar_nuevo_usuario(
                nombre=u["nombre"],
                apellido=u["apellido"],
                email=u["email"],
                nombre_de_usuario=u["usuario"],
                password="1234",  # Contraseña simple para testing
                claustro=0,
                rol=0,
                id=None
            )
            print(f"✔ Usuario creado: {u['usuario']}")
        except Exception as e:
            print(f"✖ Usuario '{u['usuario']}' ya existe o error: {e}")

    # Obtener usuario para asignar a los reclamos
# Obtener todos los usuarios disponibles
usuarios_db = [repo_usuarios.obtener_registro_por_filtro("nombre_de_usuario", u["usuario"]) for u in usuarios_info]
usuarios_db = [u for u in usuarios_db if u is not None]

if not usuarios_db:
    print("✖ No se encontraron usuarios válidos para asignar reclamos.")
else:
    for desc in reclamos_info:
        try:
            usuario_aleatorio = choice(usuarios_db)
            clasificacion = clf.clasificar([desc])[0]
            reclamo = gestor_reclamos.crear_reclamo(
                usuario=usuario_aleatorio,
                descripcion=desc,
                departamento="Mantenimiento",
                clasificacion=str(clasificacion)
            )
            modelo = repo_reclamos.mapear_reclamo_a_modelo(reclamo)
            repo_reclamos.guardar_registro(modelo)
            print(f"✔ Reclamo creado para {usuario_aleatorio.nombre_de_usuario}: {desc}")
        except Exception as e:
            print(f"✖ Error creando reclamo '{desc}': {e}")

