#Se encargará de guardar la imagen asociada a un reclamo, la misma  se guardará en ./static/Imagenes Reclamos
#La imagen tendrá como nombre el id del reclamo y extensión .png con posibilidad de ampliar el formato a jpg u otro formato
from abc import ABC, abstractmethod
from PIL import Image
import os

class GestorImagenReclamo(ABC):
    """
    Clase abstracta para gestionar imágenes asociadas a reclamos.
    Define métodos para guardar y eliminar imágenes.
    """

    @abstractmethod

    def guardar_imagen(self, reclamo_id, imagen):
        """
        Guarda una imagen asociada a un reclamo.
        
        :param reclamo_id: ID del reclamo al que se asocia la imagen.
        :param imagen: Imagen a guardar (puede ser un archivo o un objeto de imagen).
        """
        pass

    @abstractmethod
    def eliminar_imagen(self, reclamo_id):
        """
        Elimina la imagen asociada a un reclamo.
        
        :param reclamo_id: ID del reclamo cuya imagen se desea eliminar.
        """
        pass

class GestorImagenReclamoPng(GestorImagenReclamo):
    def __init__(self,direccion= "static/Imagenes Reclamos"):
        self.__direccion_archivo = direccion
        
    def guardar_imagen(self,reclamo_id, imagen):
            """
            Se guarda la imagen en formato PNG y el nombre es la id del reclamo
            """
            if imagen:
                
                try:
                    imagen_pillow = Image.open(imagen)
                    
                    ruta = os.path.join(self.__direccion_archivo,f"{reclamo_id}.png")
                    imagen_pillow.save(ruta,format="PNG")
                    return
                except Exception as e:
                    
                    print(f"Error al guardar la imagen: {e}")
                    return None
            
            
            raise ValueError(f"La imagen  asociada al reclamo {reclamo_id} no se guardo.")

    def eliminar_imagen(self, reclamo_id):
        """
        Se elimina una imagen asociada a un reclamo (por ejemplo, cuando damos por invalido y lo eliminamos)
        """
        try:

            ruta = os.path.join(self.__direccion_archivo,f"{reclamo_id}.png")
            os.remove(ruta)
            print(f"Se removió correctamente la imagen asociada al reclamo {reclamo_id}")

        except Exception as e:

            print(f"Error al elimar la imagen: {e}")