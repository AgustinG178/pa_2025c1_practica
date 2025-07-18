import unittest
import os
from PIL import Image
from modules.gestor_imagen_reclamo import GestorImagenReclamoPng

class TestGestorImagenReclamoPng(unittest.TestCase):
    def setUp(self):
        # Arrange: Configuración inicial para los tests
        self.gestor = GestorImagenReclamoPng(direccion="static/Imagenes Reclamos")
        self.reclamo_id = "test123"

        # Crear directorio si no existe
        os.makedirs("static/Imagenes Reclamos", exist_ok=True)

        # Crear imagen temporal en memoria
        self.imagen_prueba = "test_image.png"
        imagen = Image.new("RGB", (10, 10), color="red")
        imagen.save(self.imagen_prueba)

    def test_guardar_imagen(self):
        """Verifica que se puede guardar una imagen."""
        # Arrange: Imagen de prueba creada en setUp

        # Act: Guardar la imagen
        self.gestor.guardar_imagen(self.reclamo_id, self.imagen_prueba)

        # Assert: Verificar que la imagen se guardó correctamente
        ruta_esperada = os.path.join("static/Imagenes Reclamos", f"{self.reclamo_id}.png")
        self.assertTrue(os.path.exists(ruta_esperada))

    def test_eliminar_imagen(self):
        """Verifica que se puede eliminar una imagen."""
        # Arrange: Guardar la imagen antes de eliminarla
        self.gestor.guardar_imagen(self.reclamo_id, self.imagen_prueba)
        ruta_esperada = os.path.join("static/Imagenes Reclamos", f"{self.reclamo_id}.png")
        self.assertTrue(os.path.exists(ruta_esperada))

        # Act: Eliminar la imagen
        self.gestor.eliminar_imagen(self.reclamo_id)

        # Assert: Verificar que la imagen fue eliminada
        self.assertFalse(os.path.exists(ruta_esperada))

    def tearDown(self):
        # Cleanup: Eliminar archivos residuales
        ruta_imagen_guardada = os.path.join("static/Imagenes Reclamos", f"{self.reclamo_id}.png")
        if os.path.exists(ruta_imagen_guardada):
            os.remove(ruta_imagen_guardada)
        if os.path.exists(self.imagen_prueba):
            os.remove(self.imagen_prueba)

if __name__ == "__main__":
    unittest.main()
