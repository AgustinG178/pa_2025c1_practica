import unittest
from datetime import datetime
from modules.reclamo import Reclamo

class TestReclamo(unittest.TestCase):
    """Tests para la clase Reclamo."""

    def setUp(self):
        """Configura un reclamo de ejemplo para los tests."""
        self.fecha = datetime(2025, 6, 9, 15, 30)
        self.reclamo = Reclamo(
            estado="pendiente",
            fecha_hora=self.fecha,
            contenido="El equipo no funciona",
            departamento="soporte informático",
            clasificacion="hardware",
            usuario_id=123
        )

    def test_atributos_iniciales(self):
        """Verifica que los atributos se asignan correctamente al crear el reclamo."""
        self.assertEqual(self.reclamo.estado, "pendiente")
        self.assertEqual(self.reclamo.fecha_hora, self.fecha)
        self.assertEqual(self.reclamo.contenido, "El equipo no funciona")
        self.assertEqual(self.reclamo.departamento, "soporte informático")
        self.assertEqual(self.reclamo.clasificacion, "hardware")
        self.assertEqual(self.reclamo.usuario_id, 123)
        self.assertIsNone(self.reclamo.id)

    def test_cambiar_estado(self):
        """Verifica que cambiar_estado actualiza el estado correctamente."""
        self.reclamo.cambiar_estado("resuelto")
        self.assertEqual(self.reclamo.estado, "resuelto")

    def test_repr(self):
        """Verifica la representación oficial (__repr__) del objeto."""
        esperado = ("Reclamo(estado=pendiente, fecha_hora=2025-06-09 15:30:00, contenido=El equipo no funciona, "
                    "departamento=soporte informático, clasificacion=hardware, usuario_id=123)")
        self.assertEqual(repr(self.reclamo), esperado)

    def test_str(self):
        """Verifica la representación informal (__str__) del objeto."""
        esperado = ("Reclamo: El equipo no funciona | Estado: pendiente | Fecha: 2025-06-09 15:30:00 | "
                    "Departamento: soporte informático | Clasificación: hardware | Usuario ID: 123")
        self.assertEqual(str(self.reclamo), esperado)

    def test_id_opcional(self):
        """Verifica que se puede asignar un id opcional al crear un reclamo."""
        reclamo_con_id = Reclamo(
            estado="pendiente",
            fecha_hora=self.fecha,
            contenido="Problema con la red",
            departamento="soporte informático",
            clasificacion="red",
            usuario_id=456,
            id=42
        )
        self.assertEqual(reclamo_con_id.id, 42)

if __name__ == "__main__":
    unittest.main()
