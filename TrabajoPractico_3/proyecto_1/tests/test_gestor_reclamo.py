import unittest
from modules.repositorio import RepositorioReclamosSQLAlchemy
from modules.usuarios import Usuario
from modules.reclamo import Reclamo
from modules.config import crear_engine
from modules.modelos import ModeloUsuario, ModeloReclamo
from modules.gestor_reclamos import GestorReclamo 


class ClasificadorMock:
    def clasificar(self, texto):
        return "soporte"  # Respuesta fija para test # pragma: no cover

class TestGestorReclamo(unittest.TestCase):
    """Tests para la gestión de reclamos con GestorReclamo."""

    @classmethod
    def setUpClass(cls):
        engine, Session = crear_engine()
        cls.session = Session()
        cls.session.query(ModeloUsuario).delete()
        cls.session.commit()

        ModeloUsuario.metadata.create_all(engine)
        ModeloReclamo.metadata.create_all(engine)

        cls.repositorio = RepositorioReclamosSQLAlchemy(cls.session)
        cls.clasificador = ClasificadorMock()
        cls.gestor = GestorReclamo(cls.repositorio, cls.clasificador)

        cls.usuario_modelo = ModeloUsuario(
            nombre="Admin",
            apellido="User",
            email="admin@example.com",
            nombre_de_usuario="admin",
            contraseña="admin",
            rol="Secretario Tecnico",
            claustro="ing"
        )
        cls.session.add(cls.usuario_modelo)
        cls.session.commit()
        cls.usuario = Usuario(
            id=cls.usuario_modelo.id,
            nombre=cls.usuario_modelo.nombre,
            apellido=cls.usuario_modelo.apellido,
            email=cls.usuario_modelo.email,
            nombre_de_usuario=cls.usuario_modelo.nombre_de_usuario,
            contraseña=cls.usuario_modelo.contraseña,
            rol=cls.usuario_modelo.rol,
            claustro=cls.usuario_modelo.claustro
        )

    def tearDown(self):
        self.session.query(ModeloReclamo).delete()
        self.session.commit()

    def test_crear_reclamo_valido(self):
        """Verifica que se puede crear un reclamo válido y se asignan los atributos correctamente."""
        reclamo = self.gestor.crear_reclamo(
            self.usuario,
            descripcion="El proyector no enciende",
            departamento="Maestranza",
            clasificacion="soporte"
        )
        self.assertEqual(reclamo.estado, "pendiente")
        self.assertEqual(reclamo.usuario_id, self.usuario.id)

    def test_eliminar_reclamo(self):
        """Verifica que se puede eliminar un reclamo y que ya no existe en el repositorio."""
        reclamo = self.gestor.crear_reclamo(
            self.usuario,
            descripcion="Teclado roto",
            departamento="IT",
            clasificacion="soporte"
        )
        modelo = self.repositorio.mapear_reclamo_a_modelo(reclamo)
        self.repositorio.guardar_registro(modelo)
        reclamo_id = modelo.id

        mensaje = self.gestor.eliminar_reclamo(self.usuario, reclamo_id)
        self.assertEqual(mensaje, f"El reclamo de id:{reclamo_id} se ha eliminado correctamente.")
        self.assertIsNone(self.repositorio.obtener_registro_por_filtro("id", reclamo_id))

    def agregar_adherente(self, id_reclamo, usuario_modelo):
        """Agrega un adherente a un reclamo para pruebas de duplicados."""
        reclamo = self.repositorio.obtener_por_id(id_reclamo)
        if usuario_modelo in reclamo.usuarios:
            raise ValueError("El usuario ya está adherido a este reclamo.") #pragma: no cover
        reclamo.usuarios.append(usuario_modelo)
        self.repositorio.actualizar_reclamo(reclamo)


    def test_agregar_adherente_valido(self):
        """Verifica que se puede agregar un adherente a un reclamo correctamente."""
        # Creo un reclamo primero
        reclamo = self.gestor.crear_reclamo(
            self.usuario,
            descripcion="Internet caído",
            departamento="IT",
            clasificacion="soporte"
        )
        modelo = self.repositorio.mapear_reclamo_a_modelo(reclamo)
        self.repositorio.guardar_registro(modelo)

        # Creo usuario dummy para adherente
        otro_usuario_modelo = ModeloUsuario(
            nombre="Otro",
            apellido="Usuario",
            email="otro@example.com",
            nombre_de_usuario="otro",
            contraseña="1234",
            rol="Usuario",
            claustro="ing"
        )
        self.session.add(otro_usuario_modelo)
        self.session.commit()

        try:
            # Agrego adherente
            self.gestor.agregar_adherente(modelo.id, otro_usuario_modelo)

            # Verifico que se haya agregado correctamente
            reclamo_actualizado = self.repositorio.obtener_registro_por_filtro("id", modelo.id, mapeado=False)
            self.assertEqual(reclamo_actualizado.cantidad_adherentes, 1)

        finally:
            # Limpio el usuario dummy para que no quede en la BD
            self.session.delete(otro_usuario_modelo)
            self.session.commit()


    def test_agregar_adherente_duplicado(self):
        """Verifica que no se puede agregar dos veces el mismo adherente a un reclamo."""
        reclamo = self.gestor.crear_reclamo(
            self.usuario,
            descripcion="Sin señal WiFi",
            departamento="IT",
            clasificacion="soporte"
        )
        modelo = self.repositorio.mapear_reclamo_a_modelo(reclamo)
        self.repositorio.guardar_registro(modelo)

        # Primer agregado, debería funcionar
        self.agregar_adherente(modelo.id, self.usuario_modelo)

        # Segundo agregado, debería lanzar excepción
        with self.assertRaises(ValueError):
            self.gestor.agregar_adherente(modelo.id, self.usuario_modelo)

    def test_crear_reclamo(self):
        """Verifica que se puede crear un reclamo."""
        reclamo = self.gestor.crear_reclamo(
            descripcion="El proyector no funciona",
            departamento="soporte informático",
            clasificacion="hardware"
        )
        self.assertIsInstance(reclamo, ModeloReclamo)

if __name__ == "__main__": #pragma: no cover
    unittest.main()

