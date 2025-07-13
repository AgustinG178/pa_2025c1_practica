from modules.repositorio import RepositorioReclamosSQLAlchemy,RepositorioUsuariosSQLAlchemy
from modules.reclamo import Reclamo
from datetime import datetime
from modules.login import FlaskLoginUser
from modules.modelos import ModeloReclamo
from datetime import date
from modules.gestor_imagen_reclamo import GestorImagenReclamo
from werkzeug.datastructures import FileStorage

class GestorReclamo:

    """
    La clase gestor reclamo establece una relacion entre el modelo de negocio con la capa de dominio, sin interaccionar (directamente) con la base de datos
    a la hora de, por ejemplo, eliminar un reclamo.
    Sus metodos son practicamente los mismos que los del repositorio.
    """

    def __init__(self, repositorio_reclamo: RepositorioReclamosSQLAlchemy):
        self.repositorio_reclamo = repositorio_reclamo


    def crear_reclamo(self, usuario:FlaskLoginUser, descripcion: str,clasificador):
        """
        Se crea un reclamo en base a la descripción dada, el parámetro clasificador es el propio clasificador brindado por la cátedra
        """
        clasificacion = clasificador.clasificar([descripcion])[0]
  
        if not hasattr(usuario, 'id') or not descripcion:
            raise ValueError("Verificar que los datos ingresados sean correctos")
        
        
        p_reclamo = Reclamo(
            estado="pendiente",
            fecha_hora=datetime.now(),
            usuario_id=usuario.id,
            contenido=descripcion,
            clasificacion=clasificacion
        )

        #Ahora guardamos la imagen en caso que exista
        
        print(f"[DEBUG] Reclamo creado: {p_reclamo.usuario_id}")
        return p_reclamo
    
    def guardar_reclamo(self,p_reclamo:Reclamo):
        if isinstance(p_reclamo,Reclamo):

            modelo_reclamo = self.repositorio_reclamo.map_entidad_a_modelo(reclamo=p_reclamo)

            self.repositorio_reclamo.guardar_registro(modelo_reclamo=modelo_reclamo)

    def buscar_reclamo_por_filtro(self,filtro,valor) ->Reclamo:

        """
        Se devuelve un reclamo accediendo a este mediante un filtro
        """
        try:

            return self.repositorio_reclamo.obtener_registro_por_filtros(**{filtro:valor})
    
        except Exception as e:
            
            print(f"Error: {e} a la hora de devolver el reclamo")
            
    def buscar_reclamos_por_filtro(self,mapeo=True, filtro=None, valor=None):

        """
        Se devuelven todos los reclamos que correspondan con el filtro ingresado.
        """
        if filtro and valor:
            try:

                return self.repositorio_reclamo.obtener_registros_por_filtro(filtro=filtro, valor=valor,mapeo=mapeo)
            except Exception as e:
                raise e  # Lanza el error en vez de retornarlo
       
    def devolver_reclamos_base(self,usuario:FlaskLoginUser):

        """
        Se devuelven todos los reclamos de la base de datos, solo si el usuario es un sec. tecnico
        """

        usuario.__dict__

        if int(usuario.rol) == 1:
            return self.repositorio_reclamo.obtener_todos_los_registros()
        
        raise PermissionError(f"El usuario {usuario.nombre_de_usuario} no posee los permisos para realizar dicha petición")
    
    def buscar_reclamos_similares(self,clasificacion:str,reclamo_id:int):
        """
        Se devuelven todos los reclamos similares asociados a uno creado
        """

        if clasificacion and reclamo_id:
            try:

                return self.repositorio_reclamo.buscar_similares(clasificacion=clasificacion,reclamo_id=reclamo_id)
            except Exception as e:

                print(f"Error: {e} al intentar buscar similares")

        raise ValueError("Verifique los datos ingresados")

    def actualizar_estado_reclamo(self, usuario: FlaskLoginUser, reclamo: Reclamo,accion:str,tiempo_estimado:int=None):

        """
        Se actualiza el estado de un reclamo, solo lo es capaz de realizarlo un Jefe de Departamento
        """

        if int(usuario.rol) in [2,3,4]:  #Los roles estan definidos en FlaskLoginUser
            try:
                reclamo_a_modificar = self.repositorio_reclamo.obtener_registro_por_filtros(**{"id":reclamo.id})

                if accion == "resolver":
                    reclamo_a_modificar.estado = "resuelto"
                    # Se resuelve el reclamo directamente, sin pasarlo de pendiente --> proceso
                    if reclamo_a_modificar.tiempo_estimado is None:
                        dias = 0
                        reclamo_a_modificar.resuelto_en = dias
                        reclamo_a_modificar.tiempo_estimado = None
                        self.repositorio_reclamo.modificar_registro(reclamo_a_modificar=reclamo_a_modificar)
                        return
                    
                    if hasattr(reclamo, 'fecha_hora') and isinstance(reclamo.fecha_hora, datetime):
                        dias = (date.today() - reclamo.fecha_hora.date()).days
                    else:
                        dias = None  
                    reclamo_a_modificar.resuelto_en = dias
                    reclamo_a_modificar.resuelto_en = dias

                    self.repositorio_reclamo.modificar_registro(reclamo_a_modificar=reclamo_a_modificar)
                    return
                
                elif accion == "actualizar":
                    

                    reclamo_a_modificar.estado = "en proceso"
                    reclamo_a_modificar.tiempo_estimado = int(tiempo_estimado)
                    self.repositorio_reclamo.modificar_registro(reclamo_a_modificar=reclamo_a_modificar)
                    return
                
            except Exception as e:
                return

        raise PermissionError("El usuario no posee los permisos para realizar dicha modificación")

    def invalidar_reclamo(self,reclamo_id: int,gestor_imagen:GestorImagenReclamo):
        """
        Se elimina un reclamo (accediendo a este con su id) asociado a un usuario.
        También se elimina, en caso que exista, la imagen asociada a dicho reclamo
        """

        try:

            self.repositorio_reclamo.eliminar_registro_por_id(reclamo_id)


            gestor_imagen.eliminar_imagen(reclamo_id=reclamo_id)

            return f"El reclamo de id:{reclamo_id} se ha eliminado correctamente."

        except AttributeError:
            return f"El reclamo no existe y/o la id: {reclamo_id} no es correcta"
        

        
    def agregar_adherente(self, reclamo_id, usuario: FlaskLoginUser,repositorio_usuarios:RepositorioUsuariosSQLAlchemy):
        #Devolvemos el reclamo como modelo para poder trabajar con su atributo usuarios
        reclamo_a_adherir = self.repositorio_reclamo.obtener_registro_por_filtros(mapeo=False,**{"id":reclamo_id})

        if reclamo_a_adherir is None:
            raise ValueError(f"El reclamo con ID {reclamo_id} no existe.")
        if usuario in reclamo_a_adherir.usuarios:
            raise ValueError("El usuario ya está adherido a este reclamo.")

        reclamo_a_adherir.cantidad_adherentes += 1
        #devolvemos el modelo usuario del usuario actual

        modelo_usuario = repositorio_usuarios.obtener_registro_por_filtros(**{"id":usuario.id})


        try:
            reclamo_a_adherir.usuarios.append(modelo_usuario)
            self.repositorio_reclamo.commit()

        except Exception as e:
            print(f"No fue posible adherir al usuario, error {e}")

        
    def modificar_reclamo(self,reclamo_id,clasificador=None,gestor_imagen:GestorImagenReclamo=None,nuevo_contenido=None,nuevo_dpto=None, imagen:FileStorage=None):

        """
        Se modifica un reclamo, si se ingresa un nuevo departamento significa que fue derivado, caso contrario simplemente se actualiza su contenido y clasificacion
        """
        reclamo_a_modificar = self.repositorio_reclamo.obtener_registro_por_filtros(**{"id":reclamo_id})

        if nuevo_dpto:


            reclamo_a_modificar.clasificacion = nuevo_dpto

            self.repositorio_reclamo.modificar_registro(reclamo_a_modificar=reclamo_a_modificar)

            print(f"El reclamo de id {reclamo_id} ha sido correctamente derivado al departamento {nuevo_dpto}")
            return

        if nuevo_contenido:

            reclamo_a_modificar.contenido = nuevo_contenido
            reclamo_a_modificar.clasificacion = clasificador.clasificar([nuevo_contenido])[0]


            self.repositorio_reclamo.modificar_registro(reclamo_a_modificar=reclamo_a_modificar)

            print(f"El reclamo de id {reclamo_id} ha sido modificado correctamente")

            if imagen and imagen.filename:
                gestor_imagen.guardar_imagen(reclamo_id=reclamo_id,imagen=imagen)

            return
        raise ValueError("El nuevo contenido no puede ser una cadena vacia.")
    
    def ultimo_reclamo_creado_por_usuario(self,usuario:FlaskLoginUser):
        """
        Devuelve el último reclamo creado por el usuario
        """

        return self.repositorio_reclamo.ultimo_reclamo_creado_por_usuario(usuario_id=usuario.id)
    
    def añadir_imagen_reclamo(self, gestor_imagen:GestorImagenReclamo ,reclamo_id,imagen: FileStorage = None):

        if imagen and imagen.filename:
            try:

                gestor_imagen.guardar_imagen(reclamo_id=reclamo_id,imagen=imagen)

            except Exception as e:
                print(f"Error {e} al tratar de guardar la imagen del reclamo id {reclamo_id}")

        print(f"No hay ninguna imagen asociada al reclamo de id {reclamo_id}")

        
if __name__ == "__main__": #pragma: no cover
    from modules.config import crear_engine
    from modules.modelos import ModeloReclamo
    from modules.repositorio import RepositorioReclamosSQLAlchemy,RepositorioUsuariosSQLAlchemy
    # 1. Crear engine y session (usa tu configuración real o una in-memory SQLite)
    engine, Session = crear_engine()  
    session = Session()

    # 2. Crear repositorio y gestor
    #repositorio = RepositorioReclamosSQLAlchemy(session)
    
    

    #gestor = GestorReclamo(repositorio, clasificador)
    repo_usuarios = RepositorioUsuariosSQLAlchemy(session)
    repositorio_reclamos = RepositorioReclamosSQLAlchemy(session)

    gestor_reclamo =GestorReclamo(repositorio_reclamo=repositorio_reclamos)
    # 3. Crear usuario y reclamo en DB para la prueba

    usuario_1 =  repo_usuarios.obtener_registro_por_filtro(campo = "nombre_de_usuario" , valor = "esteban")
    usuario_2 =  repo_usuarios.obtener_registro_por_filtro(campo = "nombre_de_usuario" , valor = "nicora")

    print("[DEBUG] Usuario creado:", usuario_1)
    #session.add(usuario)
    print("[DEBUG] Usuario agregado a la sesión.")
    #session.commit()  # para que usuario.id se genere
    #print("[DEBUG] Usuario presente en la base de datos con ID:", usuario.id)

    reclamo = Reclamo(
        estado="pendiente",
        fecha_hora=datetime.now(),
        contenido="Reclamo prueba",
        clasificacion="soporte informático",
        usuario_id=usuario_1.id
    )
    modelo_r = repositorio_reclamos.mapear_reclamo_a_modelo(reclamo)
    repositorio_reclamos.guardar_registro(modelo_r)
    print("[DEBUG] Reclamo creado:", modelo_r)
    print("[DEBUG] Reclamo guardado en la base de datos con ID:", modelo_r.id)

    # Recuperar el reclamo desde la sesión para trabajar con relaciones
    modelo_r_db = session.query(ModeloReclamo).filter_by(id=modelo_r.id).first()

    # Probar agregar adherente
    modelo_usuario = repo_usuarios.buscar_usuario(nombre_de_usuario=usuario_2.nombre_de_usuario)
    resultado = gestor_reclamo.agregar_adherente(modelo_r_db.id, modelo_usuario)

    # Volver a consultar para ver los usuarios adheridos
    reclamo_actualizado = session.query(ModeloReclamo).filter_by(id=modelo_r.id).first()
    print([u.nombre_de_usuario for u in reclamo_actualizado.usuarios])




