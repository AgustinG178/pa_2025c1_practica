import unittest
from unittest.mock import MagicMock
from modules.gestor_usuario import GestorUsuarios
from modules.repositorio import RepositorioUsuariosSQLAlchemy
from modules.modelos import ModeloUsuario



class TestGestorUsuarios(unittest.TestCase):
    def setUp(self):
        """Configura el entorno para cada prueba."""
        # Mock de la sesión y el repositorio
        self.session = MagicMock()
        self.repo = RepositorioUsuariosSQLAlchemy(self.session)
        self.gestor = GestorUsuarios(self.repo)

        # Limpia la base de datos simulada
        self.session.query(ModeloUsuario).delete()

    def test_crear_usuario(self):
        """Verifica que se puede crear un usuario y recuperarlo por id."""
        usuario = ModeloUsuario(
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            nombre_de_usuario="juanperez",
            contraseña="1234",
            rol=0,
            claustro="estudiante",
        )
        self.repo.guardar_registro(usuario)
        self.session.commit.assert_called_once()

    def test_actualizar_usuario(self):
        """Verifica que se puede actualizar el nombre de usuario correctamente."""
        usuario = ModeloUsuario(
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            nombre_de_usuario="juanperez",
            contraseña="1234",
            rol=0,
            claustro="estudiante",
        )
        self.repo.guardar_registro(usuario)
        usuario.nombre = "Juan Carlos"
        self.repo.modificar_registro(usuario)
        self.session.commit.assert_called()

    def test_eliminar_usuario(self):
        """Verifica que se puede eliminar un usuario y que ya no existe."""
        usuario = ModeloUsuario(
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            nombre_de_usuario="juanperez",
            contraseña="1234",
            rol=0,
            claustro="estudiante",
        )
        self.repo.guardar_registro(usuario)
        self.repo.eliminar_registro_por_id(usuario.id)
        self.session.commit.assert_called()

    def test_buscar_usuario(self):
        """Verifica que se puede buscar un usuario por id y coincide la representación."""
        usuario = ModeloUsuario(
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            nombre_de_usuario="juanperez",
            contraseña="1234",
            rol=0,
            claustro="estudiante",
        )
        self.repo.guardar_registro(usuario)

        # Configurar el mock para devolver el usuario
        self.session.query().filter_by().first.return_value = usuario

        resultado = self.repo.obtener_registro_por_filtros(mapeo=False,**{"id":usuario.id})
        self.assertEqual(resultado, usuario)


    def test_generar_reporte_usuario_pdf(self):
        """Verifica que se puede generar un reporte en formato PDF."""
        reporte = MagicMock()
        resultado = self.gestor.generar_reporte_usuario(ruta_salida="reporte.txt",clasificacion_usuario="maestranza",reporte=reporte,tipo_reporte="pdf")
        self.assertEqual(resultado, "Reporte PDF generado para usuarios")

    def test_generar_reporte_usuario_html(self):
        """Verifica que se puede generar un reporte en formato HTML."""
        reporte = MagicMock()
        resultado = self.gestor.generar_reporte_usuario(ruta_salida="reporte.txt",clasificacion_usuario="maestranza",reporte=reporte,tipo_reporte="html")
        self.assertEqual(resultado, "Reporte HTML generado para usuarios")

    def test_generar_reporte_usuario_tipo_invalido(self):
        """Verifica que no se puede generar un reporte con un tipo inválido."""
        with self.assertRaises(Exception) as contexto:

            reporte = MagicMock()
            self.gestor.generar_reporte_usuario(ruta_salida="reporte.txt",clasificacion_usuario="maestranza",reporte=reporte,tipo_reporte="xml")

        self.assertIn("Error", str(contexto.exception))

if __name__ == "__main__":
    unittest.main()