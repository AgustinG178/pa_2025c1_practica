from modules.repositorio import RepositorioReclamosSQLAlchemy
from modules.reclamo import Reclamo
from modules.config import crear_engine
from datetime import datetime
from modules.login import FlaskLoginUser
from modules.modelos import ModeloUsuario
from datetime import date
from modules.text_vectorizer import TextVectorizer

class GestorReclamo:

    """
    La clase gestor reclamo establece una relacion entre el modelo de negocio con la capa de dominio, sin interaccionar (directamente) con la base de datos a la hora de, por ejemplo, eliminar un reclamo.
    Sus metodos son practicamente los mismos que los del repositorio.
    """

    def __init__(self, repositorio_reclamo: RepositorioReclamosSQLAlchemy):
        self.repositorio_reclamo = repositorio_reclamo

    def crear_reclamo(self, usuario:FlaskLoginUser, descripcion: str, clasificacion: str):
        # acepta cualquier objeto con atributo id
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
        Se devuelve un reclamo accediendo a este con su id
        """
        try:

            return self.repositorio_reclamo.obtener_registro_por_filtro(filtro="id",valor=reclamo_id)
    
        except Exception as e:
            
            print(f"Error: {e} a la hora de devolver el reclamo")
            
    def buscar_reclamos_por_filtro(self, filtro=None, valor=None, mapeo=True):

        """
        Se devuelven todos los reclamos que correspondan con los filtros ingresados.
        """
        if filtro and valor:
            try:

                return self.repositorio_reclamo.obtener_registros_por_filtro(filtro=filtro, valor=valor, mapeo=mapeo)
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
    
    def buscar_reclamos_similares(self, descripcion: str, clasificacion: str, top_n: int = 15):
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np
        """
        Retorna los reclamos más similares al texto dado usando similitud de coseno (es una medida que calcula el ángulo entre dos vectores para determinar cuán similares son en dirección).
        """
        """El percentil 70 se adapta automáticamente a la distribución actual de las similitudes. Si en un caso las similitudes son muy altas (por ejemplo, todos los reclamos son parecidos), el umbral sube. Si son muy bajas, baja. Esto evita falsos positivos o negativos.
        la decision de usar el percentil 70 es arbitraria, pero se basa en la idea de que queremos capturar una buena cantidad de similitudes sin incluir demasiados casos marginales. pero dado que la base de datos es arbitraria, puede que en algunos casos no funcione como se espera. o que no aparezcan demasiados reclamos similares bajo el contexto del reclamo ingresado.
        """
        reclamos_existentes = self.repositorio_reclamo.obtener_todos_los_registros()
        if clasificacion:
            reclamos_existentes = [r for r in reclamos_existentes if r.clasificacion == clasificacion]

        if not reclamos_existentes:
            return []

        textos = [r.contenido for r in reclamos_existentes]
        vectorizer = TextVectorizer()
        vectorizer.fit(textos + [descripcion])  # Entrenamos incluyendo el nuevo texto

        vectores_existentes = vectorizer.transform(textos)
        vector_nuevo = vectorizer.transform([descripcion])

        similitudes = cosine_similarity(vector_nuevo, vectores_existentes)[0]
        indices_similares = np.argsort(similitudes)[::-1][:top_n]

        umbral_dinamico = np.percentile(similitudes, 70)
        similares = [reclamos_existentes[i] for i in indices_similares if similitudes[i] > umbral_dinamico]
        
        similares.pop(0)  # Eliminar el reclamo mismo, dado que al estar en la base de datos, siempre será el más similar a sí mismo.
        
        return similares

    def actualizar_estado_reclamo(self, usuario: FlaskLoginUser, reclamo: Reclamo, accion: str, tiempo_estimado: int = None):
        if int(usuario.rol) in [2, 3, 4]:
            try:
                reclamo_a_modificar = self.repositorio_reclamo.obtener_registro_por_filtro(filtro="id", valor=reclamo.id, mapeo=False)
                if accion == "resolver":
                    reclamo_a_modificar.estado = "resuelto"
                    reclamo_a_modificar.tiempo_estimado = None
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
        
    def agregar_adherente(self, reclamo_id, usuario: ModeloUsuario):
        """
        Agrega un adherente a un reclamo existente.
        """
        #Devolvemos el reclamo como modelo para poder trabajar con su atributo usuarios
        reclamo_a_adherir = self.repositorio_reclamo.obtener_registro_por_filtro(filtro="id", valor=reclamo_id,mapeo=False)

        if reclamo_a_adherir is None:
            raise ValueError(f"El reclamo con ID {reclamo_id} no existe.")
        if usuario in reclamo_a_adherir.usuarios:
            raise ValueError("El usuario ya está adherido a este reclamo.")

        reclamo_a_adherir.cantidad_adherentes += 1

        try:
            reclamo_a_adherir.usuarios.append(usuario)
            self.repositorio_reclamo.session.commit()
        except Exception as e:
            print(f"No fue posible adherir al usuario, error {e}")
        
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

if __name__ == "__main__":  # pragma: no cover
    """
    Evalúa el recall del modelo y el balanceo de clases (51.56%, 31.25%, 17.19%). 
    Aunque hay leve desbalance, no impacta críticamente porque el sistema se usa en 
    un entorno cerrado, con datos en constante actualización y sin requerimientos 
    de recall alto. Se incluye por fuera del alcance formal del curso, como mejora exploratoria.
    """

    from collections import Counter
    from modules.config import crear_engine

    engine, Session = crear_engine()
    session = Session()
    repositorio = RepositorioReclamosSQLAlchemy(session)

    pruebas = repositorio.obtener_todos_los_registros()

    gestor = GestorReclamo(repositorio)

    total_vp = 0
    total_fn = 0
    contador_clases = Counter()

    for prueba in pruebas:
        descripcion = prueba.contenido
        clasificacion = prueba.clasificacion
        contador_clases[clasificacion] += 1

        similares_reales = set(r.id for r in gestor.repositorio_reclamo.buscar_similares(clasificacion, prueba.id))
        similares_predichos = gestor.buscar_reclamos_similares(descripcion, clasificacion)
        ids_predichos = set(r.id for r in similares_predichos)

        vp = len(ids_predichos.intersection(similares_reales))
        fn = len(similares_reales - ids_predichos)

        total_vp += vp
        total_fn += fn

        # print(f"Para '{descripcion}': VP={vp}, FN={fn}")

    recall = total_vp / (total_vp + total_fn) if (total_vp + total_fn) > 0 else 0
    print(f"\nRecall global del modelo: {recall:.2f}")

    total = sum(contador_clases.values())
    print("\nDistribución de clases:")
    for clasificacion, cantidad in contador_clases.items():
        porcentaje = (cantidad / total) * 100
        print(f"  {clasificacion}: {cantidad} ({porcentaje:.2f}%)")

    max_porcentaje = max((cantidad / total) * 100 for cantidad in contador_clases.values())
    min_porcentaje = min((cantidad / total) * 100 for cantidad in contador_clases.values())

    if max_porcentaje - min_porcentaje > 40:
        print("\n La base de datos está DESBALANCEADA.")
    else:
        print("\n La base de datos está relativamente balanceada.")
        print("\nPara mejorar el modelo, considera ajustar los parámetros de búsqueda o aumentar la diversidad de los datos de entrenamiento.")




