from modules.repositorio import RepositorioReclamosSQLAlchemy, RepositorioUsuariosSQLAlchemy
from modules.reclamo import Reclamo
from modules.config import crear_engine
from datetime import datetime, UTC
from modules.login import FlaskLoginUser
from modules.modelos import ModeloReclamo,ModeloUsuario
import random
from datetime import date

#session = crear_engine()
#repositorio_reclamo = RepositorioReclamosSQLAlchemy(session)

class GestorReclamo:

    """
    La clase gestor reclamo establece una relacion entre el modelo de negocio con la capa de dominio, sin interaccionar (directamente) con la base de datos
    a la hora de, por ejemplo, eliminar un reclamo.
    Sus metodos son practicamente los mismos que los del repositorio.
    """

    def __init__(self, repositorio_reclamo: RepositorioReclamosSQLAlchemy):
        self.repositorio_reclamo = repositorio_reclamo

    def crear_reclamo(self, usuario:FlaskLoginUser, descripcion: str, clasificacion: str):
        # acepta cualquier objeto con atributo id, por ejemplo
        if not hasattr(usuario, 'id') or not descripcion:
            raise ValueError("Verificar que los datos ingresados sean correctos")
        p_reclamo = Reclamo(
            estado="pendiente",
            fecha_hora=datetime.now(),
            usuario_id=usuario.id,
            contenido=descripcion,
            clasificacion=clasificacion
        )
        return p_reclamo
    
    def guardar_reclamo(self,reclamo:Reclamo):

        if isinstance(reclamo,Reclamo):

            modelo_reclamo = self.repositorio_reclamo.mapear_reclamo_a_modelo(reclamo=reclamo)
            self.repositorio_reclamo.guardar_registro(modelo_reclamo=modelo_reclamo)

    def devolver_reclamo(self,reclamo_id) ->Reclamo:

        """
        Se devuelve un reclamo accediendo a  este con su id
        """
        try:

            return self.repositorio_reclamo.obtener_registro_por_filtro(filtro="id",valor=reclamo_id)
    
        except Exception as e:
            
            print(f"Error: {e} a la hora de devolver el reclamo")
            
    def buscar_reclamos_por_filtro(self, filtro=None, valor=None):

        """
        Se devuelven todos los reclamos que correspondan con los filtros ingresados.
        """
        if filtro and valor:
            try:

                return self.repositorio_reclamo.obtener_registros_por_filtro(filtro=filtro, valor=valor)
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
                reclamo_a_modificar = self.repositorio_reclamo.obtener_registro_por_filtro(filtro="id", valor=reclamo.id)

                if accion == "resolver":
                    reclamo_a_modificar.estado = "resuelto"
                    # Se resuelve el reclamo directamente, sin pasarlo de pendiente --> proceso
                    if reclamo_a_modificar.tiempo_estimado is None:
                        dias = 0
                        reclamo_a_modificar.resuelto_en = dias
                        self.repositorio_reclamo.modificar_registro(reclamo_a_modificar=reclamo_a_modificar)
                        return
                    
                    if hasattr(reclamo, 'fecha_hora') and isinstance(reclamo.fecha_hora, datetime):
                        dias = (date.today() - reclamo.fecha_hora.date()).days
                    else:
                        dias = None  
                    reclamo_a_modificar.resuelto_en = dias
                    self.repositorio_reclamo.modificar_registro(reclamo_a_modificar=reclamo_a_modificar)
                    print(f"[DEBUG] Reclamo actualizado: {reclamo_a_modificar} correctamente")
                    return
                elif accion == "actualizar":
                    

                    reclamo_a_modificar.estado = "en proceso"
                    reclamo_a_modificar.tiempo_estimado = tiempo_estimado
                    self.repositorio_reclamo.modificar_registro(reclamo_a_modificar=reclamo_a_modificar)
                    print(f"[DEBUG] Reclamo actualizado: {reclamo_a_modificar} correctamente")
                    return
                

            except Exception as e:
                print(f"[DEBUG] Error {e} al actualizar estado del reclamo")
                return

        raise PermissionError("El usuario no posee los permisos para realizar dicha modificación")

    def invalidar_reclamo(self,reclamo_id: int):
        """
        Se elimina un reclamo (accediendo a este con su id) asociado a un usuario.
        """

        try:

            self.repositorio_reclamo.eliminar_registro_por_id(reclamo_id)


            return f"El reclamo de id:{reclamo_id} se ha eliminado correctamente."

        except AttributeError:
            return f"El reclamo no existe y/o la id: {reclamo_id} no es correcta"
             
    def agregar_adherente(self, reclamo_id, usuario:ModeloUsuario):
        
        reclamo_a_adherir = self.repositorio_reclamo.obtener_registro_por_filtro(filtro="id", valor=reclamo_id)

        modelo_reclamo_adherir = self.repositorio_reclamo.mapear_reclamo_a_modelo(reclamo=reclamo_a_adherir)

        if reclamo_a_adherir is None:
            raise ValueError(f"El reclamo con ID {reclamo_id} no existe.")
        if usuario in modelo_reclamo_adherir.usuarios:
            raise ValueError("El usuario ya está adherido a este reclamo.")
        
        reclamo_a_adherir.cantidad_adherentes += 1
        
        
        modelo_reclamo_adherir.usuarios.append(usuario)
        self.repositorio_reclamo.commit()

    def obtener_ultimos_reclamos(self,cantidad:int):
        """
        Se devuelven los ultimos n reclamos de la base de datos 
        """

        print("[DEBUG] Tipo de self.repositorio_reclamo:", type(self.repositorio_reclamo))
        if isinstance(cantidad,int):

            return self.repositorio_reclamo.obtener_ultimos_reclamos(limit=cantidad)

    def modificar_reclamo(self,reclamo_modificado:Reclamo):

        if isinstance(reclamo_modificado,Reclamo):

            self.repositorio_reclamo.modificar_registro(reclamo_a_modificar=reclamo_modificado)

if __name__ == "__main__": #pragma: no cover

    from modules.config import crear_engine
    from modules.modelos import ModeloUsuario, ModeloReclamo

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
    usuario = repo_usuarios.obtener_registro_por_filtros(nombre_de_usuario = "esteban")
    print("[DEBUG] Usuario creado:", usuario)
    #session.add(usuario)
    print("[DEBUG] Usuario agregado a la sesión.")
    #session.commit()  # para que usuario.id se genere
    #print("[DEBUG] Usuario presente en la base de datos con ID:", usuario.id)

    reclamo = Reclamo(
        estado="pendiente",
        fecha_hora=datetime.now(),
        contenido="Reclamo prueba",
        clasificacion="soporte informático",
        usuario_id=usuario.id
    )
    modelo_r = repositorio_reclamos.mapear_reclamo_a_modelo(reclamo)
    repositorio_reclamos.guardar_registro(modelo_r)
    print("[DEBUG] Reclamo creado:", modelo_r)
    print("[DEBUG] Reclamo guardado en la base de datos con ID:", modelo_r.id) #pragma: no cover 

    # 4. Probar agregar adherente
    #resultado = gestor.agregar_adherente(modelo_r.id, usuario)
    #print(resultado)

    # Opcional: verificar si el usuario está adherido realmente
    reclamo_actualizado = session.query(ModeloReclamo).filter_by(id=modelo_r.id).first()
    assert reclamo_actualizado.cantidad_adherentes > 0, "El reclamo no tiene adherentes."
    print("Prueba OK, usuario adherido al reclamo.")


    ultimos_reclamos = gestor_reclamo.obtener_ultimos_reclamos(cantidad=4)
    
    for reclamo in ultimos_reclamos:
        print(reclamo)
    # except Exception as e:
    #     print("Error al agregar adherente:", e)



