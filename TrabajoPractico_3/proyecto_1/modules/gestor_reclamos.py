from modules.repositorio import RepositorioReclamosSQLAlchemy, RepositorioUsuariosSQLAlchemy
from modules.usuarios import Usuario
from modules.reclamo import Reclamo
from modules.config import crear_engine
from datetime import datetime, UTC
from modules.clasificador_de_reclamos.modules.classifier import Clasificador
from modules.modelos import ModeloUsuario, ModeloReclamo
import random
from datetime import date

session = crear_engine()
repositorio_reclamo = RepositorioReclamosSQLAlchemy(session)

class GestorReclamo:

    """
    La clase gestor reclamo establece una relacion entre el modelo de negocio con la capa de dominio, sin interaccionar (directamente) con la base de datos
    a la hora de, por ejemplo, eliminar un reclamo.
    Sus metodos son practicamente los mismos que los del repositorio.
    """

    def __init__(self, repositorio_reclamo: RepositorioReclamosSQLAlchemy, clasificador: Clasificador):
        self.repositorio_reclamo = repositorio_reclamo
        self.clasificador = clasificador

    def crear_reclamo(self, usuario, descripcion: str, departamento: str, clasificacion: str):
        # acepta cualquier objeto con atributo id, por ejemplo
        if not hasattr(usuario, 'id') or not descripcion or not departamento:
            raise ValueError("Verificar que los datos ingresados sean correctos")
        p_reclamo = Reclamo(
            estado="pendiente",
            fecha_hora=datetime.now(),
            usuario_id=usuario.id,
            contenido=descripcion,
            departamento=departamento,
            clasificacion=clasificacion
        )
        return p_reclamo
    
    def buscar_reclamos_por_usuario(self, usuario: Usuario):
        """
        Se buscan y devuelven todos los reclamos asociados a un usuario
        """
        if isinstance(usuario, Usuario):

            try:

                reclamos = self.repositorio_reclamo.obtener_todos_los_registros(usuario_id=usuario.id)


                return reclamos

            except AttributeError:
                return "El usuario no posee reclamos asociados"

        raise TypeError("El usuario no es una instancia de la clase Usuario")

    def actualizar_estado_reclamo(self, usuario: Usuario, reclamo: Reclamo,accion:str):

        """
        Se actualiza el estado de un reclamo, solo lo es capaz de realizarlo un Secretario Tecnico o un Jefe de Departamento
        """

        if int(usuario.rol) in [1,2,3,4]:  #Los roles estan definidos en FlaskLoginUser
            try:
                reclamo_a_modificar = self.repositorio_reclamo.obtener_registro_por_filtro(filtro="id", valor=reclamo.id)

                if accion == "resolver":
                    reclamo_a_modificar.estado = "resuelto"

                    dias = (date.today() - reclamo.fecha_hora.date()).days

                    reclamo_a_modificar.resuelto_en = dias
                    self.repositorio_reclamo.actualizar_reclamo(reclamo=reclamo_a_modificar)

                    print(f"[DEBUG] Reclamo actualizado: {reclamo_a_modificar} correctamente")
                    return
                
                elif accion == "actualizar":
                    reclamo_a_modificar.estado = "en proceso"
                    reclamo_a_modificar.tiempo_estimado = random.randint(1,15) #Tiempo aleatorio estimado entre 1 y 15 días desde la fecha en que se creo
                    self.repositorio_reclamo.actualizar_reclamo(reclamo=reclamo_a_modificar)
                    print(f"[DEBUG] Reclamo actualizado: {reclamo_a_modificar} correctamente")
                    return
            except AttributeError:
                print(f"[DEBUG] El reclamo con id {reclamo.id} no existe o no es correcto")
                return

        raise PermissionError("El usuario no posee los permisos para realizar dicha modificación")

    def invalidar_reclamo(self, usuario: Usuario, reclamo_id: int):
        """
        Se elimina un reclamo (accediendo a este con su id) asociado a un usuario, realizando sus  pertinentes verificaciones.
        """
        if int(usuario.rol) in [1,2,3,4]:  #Los roles estan definidos en FlaskLoginUser

            try:

                self.repositorio_reclamo.eliminar_registro_por_id(reclamo_id)


                return f"El reclamo de id:{reclamo_id} se ha eliminado correctamente."

            except AttributeError:
                return f"El reclamo no existe y/o la id: {reclamo_id} no es correcta"

        raise PermissionError("El usuario no posee los permisos para realizar dicha modificacion.")

    def agregar_adherente(self, reclamo_id, usuario: Usuario):
        
        reclamo_a_adherir = self.repositorio_reclamo.obtener_registro_por_filtro(filtro="id", valor=reclamo_id, mapeado=False)
        if reclamo_a_adherir is None:
            raise ValueError(f"El reclamo con ID {reclamo_id} no existe.")
        if usuario in reclamo_a_adherir.usuarios:
            raise ValueError("El usuario ya está adherido a este reclamo.")
        reclamo_a_adherir.cantidad_adherentes += 1
        reclamo_a_adherir.usuarios.append(usuario.id)
        self.repositorio_reclamo.commit()
    
if __name__ == "__main__": #pragma: no cover

    from modules.config import crear_engine
    from modules.modelos import ModeloUsuario, ModeloReclamo
    from modules.clasificador_de_reclamos.modules.preprocesamiento import ProcesadorArchivo

    # 1. Crear engine y session (usa tu configuración real o una in-memory SQLite)
    engine, Session = crear_engine()  
    session = Session()

    # 2. Crear repositorio y gestor
    repositorio = RepositorioReclamosSQLAlchemy(session)
    procesador = ProcesadorArchivo("modules/clasificador_de_reclamos/data/frases.json")
    X, y = procesador.datosEntrenamiento
    clasificador = Clasificador(X, y)
    clasificador._entrenar_clasificador()

    gestor = GestorReclamo(repositorio, clasificador)
    repo_usuarios = RepositorioUsuariosSQLAlchemy(session)
    repositorio_reclamos = RepositorioReclamosSQLAlchemy(session)

    # 3. Crear usuario y reclamo en DB para la prueba
    usuario = repo_usuarios.obtener_registro_por_filtros(nombre="Laura", apellido = "Garcia", email="LauraGarcia@example.com",nombre_de_usuario='Laurita777', contraseña='1234', rol=0, claustro="estudiante")
    print("[DEBUG] Usuario creado:", usuario)
    #session.add(usuario)
    print("[DEBUG] Usuario agregado a la sesión.")
    #session.commit()  # para que usuario.id se genere
    print("[DEBUG] Usuario presente en la base de datos con ID:", usuario.id)

    reclamo = Reclamo(
        estado="pendiente",
        fecha_hora=datetime.now(),
        contenido="Reclamo prueba",
        departamento="Servicio Técnico",
        clasificacion="soporte informático",
        usuario_id=usuario.id
    )
    modelo_r = repositorio_reclamos.mapear_reclamo_a_modelo(reclamo)
    repositorio_reclamos.guardar_registro(modelo_r)
    print("[DEBUG] Reclamo creado:", modelo_r)
    print("[DEBUG] Reclamo guardado en la base de datos con ID:", modelo_r.id) #pragma: no cover 

    # 4. Probar agregar adherente
    resultado = gestor.agregar_adherente(modelo_r.id, usuario)
    print(resultado)

    # Opcional: verificar si el usuario está adherido realmente
    reclamo_actualizado = session.query(ModeloReclamo).filter_by(id=modelo_r.id).first()
    assert reclamo_actualizado.cantidad_adherentes > 0, "El reclamo no tiene adherentes."
    print("Prueba OK, usuario adherido al reclamo.")

    # except Exception as e:
    #     print("Error al agregar adherente:", e)



