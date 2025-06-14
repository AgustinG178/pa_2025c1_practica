import unittest
from datetime import datetime
from modules.reclamo import Reclamo
from modules.gestor_reclamos import GestorReclamo
from modules.usuarios import Usuario
from modules.repositorio import RepositorioReclamosSQLAlchemy, RepositorioUsuariosSQLAlchemy
from modules.config import crear_engine

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
        """Verifica la representación oficial (__repr__) del objeto Reclamo."""
        esperado = ("Reclamo(estado=pendiente, fecha_hora=2025-06-09 15:30:00, contenido=El equipo no funciona, "
                    "clasificacion=hardware, usuario_id=123)")  # Elimina departamento
        self.assertEqual(repr(self.reclamo), esperado)

    def test_str(self):
        """Verifica la representación informal (__str__) del objeto Reclamo."""
        esperado = ("Reclamo: El equipo no funciona | Estado: pendiente | Fecha: 2025-06-09 15:30:00 | "
                    "Clasificación: hardware | Usuario ID: 123")  # Elimina departamento
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

class TestGestorReclamosExtra(unittest.TestCase):
    """Tests para casos de error en la gestión de reclamos."""

    @classmethod
    def setUpClass(cls):
        engine, Session = crear_engine()
        cls.session = Session()
        cls.repo_reclamos = RepositorioReclamosSQLAlchemy(cls.session)
        cls.repo_usuarios = RepositorioUsuariosSQLAlchemy(cls.session)
        cls.gestor = GestorReclamo(cls.repo_reclamos)

    def setUp(self):
        self.session.query(self.repo_reclamos.modelo).delete()
        self.session.commit()

    def test_agregar_adherente_reclamo_no_existente(self):
        """Verifica que agregar un adherente a un reclamo inexistente lanza ValueError."""
        usuario = Usuario(nombre="A", apellido="B", email="a@b.com", nombre_de_usuario="ab", contraseña="123", rol=0, claustro=0, id=1)
        with self.assertRaises(ValueError):
            self.gestor.agregar_adherente(999, usuario)

    def test_buscar_reclamos_por_usuario_tipo_error(self):
        """Verifica que buscar reclamos con un tipo incorrecto lanza TypeError."""
        with self.assertRaises(TypeError):
            self.gestor.buscar_reclamos_por_usuario("no es usuario")

if __name__ == "__main__": #pragma: no cover
    unittest.main()
