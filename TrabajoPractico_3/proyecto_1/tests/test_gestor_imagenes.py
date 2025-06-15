import unittest
import os
from PIL import Image
from modules.gestor_imagen_reclamo import GestorImagenReclamoPng

class TestGestorImagenReclamoPng(unittest.TestCase):

    def setUp(self):
        self.gestor = GestorImagenReclamoPng(direccion="static/Imagenes Reclamos")
        self.reclamo_id = "test123"

        # Crear directorio si no existe
        os.makedirs("static/Imagenes Reclamos", exist_ok=True)

        # Crear imagen temporal en memoria
        self.imagen_prueba = "test_image.png"
        imagen = Image.new("RGB", (10, 10), color="red")
        imagen.save(self.imagen_prueba)

    def test_guardar_imagen(self):
        self.gestor.guardar_imagen(self.reclamo_id, self.imagen_prueba)
        ruta_esperada = os.path.join("static/Imagenes Reclamos", f"{self.reclamo_id}.png")
        self.assertTrue(os.path.exists(ruta_esperada))

    def test_eliminar_imagen(self):
        # Primero guardamos la imagen
        self.gestor.guardar_imagen(self.reclamo_id, self.imagen_prueba)
        ruta_esperada = os.path.join("static/Imagenes Reclamos", f"{self.reclamo_id}.png")
        self.assertTrue(os.path.exists(ruta_esperada))

        # Luego la eliminamos
        self.gestor.eliminar_imagen(self.reclamo_id)
        self.assertFalse(os.path.exists(ruta_esperada))

    def tearDown(self):
        # Eliminar archivos residuales
        ruta_imagen_guardada = os.path.join("static/Imagenes Reclamos", f"{self.reclamo_id}.png")
        if os.path.exists(ruta_imagen_guardada):
            os.remove(ruta_imagen_guardada)
        if os.path.exists(self.imagen_prueba):
            os.remove(self.imagen_prueba)

if __name__ == "__main__":
    unittest.main()
