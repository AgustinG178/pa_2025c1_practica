# Archivo de test para realizar pruebas unitarias del modulo1
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.usuarios import Usuario
from modules.modelos import Base
from modules.repositorio import RepositorioUsuariosSQLAlchemy,RepositorioReclamosSQLAlchemy
from modules.gestor_reclamos import GestorReclamo
from modules.gestor_usuario import GestorUsuarios
from modules.reclamo import Reclamo
from modules.config import crear_engine


class TestGestorUsuarios(unittest.TestCase):
    """Tests para la gestión de usuarios."""

    @classmethod
    def setUpClass(cls):
        engine, Session = crear_engine()
        cls.session = Session()
        cls.repo_usuarios = RepositorioUsuariosSQLAlchemy(cls.session)
        cls.gestor_usuario = GestorUsuarios(cls.repo_usuarios)

    def setUp(self):
        self.session.query(self.repo_usuarios.modelo).delete()
        self.session.commit()

    def test_crear_usuario(self):
        """Verifica que se puede crear un usuario y recuperarlo por id."""

        self.gestor_usuario.registrar_nuevo_usuario(
            nombre="Juan", apellido="Perez", email="juan@gmail.com",
            nombre_de_usuario="juanperez", password="1234", rol=0, claustro=0, id=1
        )

        usuario_db = self.repo_usuarios.obtener_registro_por_filtro(campo="id", valor=1)

        self.assertIsInstance(usuario_db, Usuario)
        
    def test_autenticar_usuario(self):
        """Verifica que se puede autenticar un usuario con nombre y contraseña correctos."""
        self.gestor_usuario.registrar_nuevo_usuario(nombre="Juan", apellido="Perez", email="pere@gmail.com", nombre_de_usuario="juanperez", password="1234", rol=0, claustro=0,id=1)

        usuario_autenticado = self.gestor_usuario.autenticar_usuario(nombre_de_usuario="juanperez",password="1234")

        #Esperamos que usuario auntenticado sea una instancia de Usuario

        self.assertIsInstance(usuario_autenticado,Usuario)

    def test_actualizar_usuario(self):
        """Verifica que se puede actualizar el nombre de usuario correctamente."""

        self.gestor_usuario.registrar_nuevo_usuario(nombre="Juan", apellido="Perez", email="juanpe@gmail.com", nombre_de_usuario="juanperez", password="1234", rol=0, claustro=0,id=1)

        usuario_bd = self.repo_usuarios.obtener_registro_por_filtro(campo="id",valor=1)

        nuevo_nombre = "juanperez_modificado"
        #Actualizamos mediante un setter el nombre de usuario
        usuario_bd.nombre_de_usuario = nuevo_nombre

        self.gestor_usuario.actualizar_usuario(usuario_bd)

        usuario_bd_modificado = self.repo_usuarios.obtener_registro_por_filtro(campo="id",valor=1)
        #Verificamos que el nombre de usuario se haya actualizado correctamente
        self.assertEqual(usuario_bd.nombre_de_usuario, nuevo_nombre)

    def test_eliminar_usuario(self):
        """Verifica que se puede eliminar un usuario y que ya no existe."""
        self.gestor_usuario.registrar_nuevo_usuario(nombre="Juan", apellido="Perez", email="", nombre_de_usuario="juanperez", password="1234", rol=0, claustro=0,id=1)
        usuario_bd = self.repo_usuarios.obtener_registro_por_filtro(campo="id",valor=1)

        self.gestor_usuario.eliminar_usuario(usuario_bd.id)

        usuario_eliminado = self.repo_usuarios.obtener_registro_por_filtro(campo="id",valor=1)

        self.assertIsNone(usuario_eliminado)

    def test_buscar_usuario(self):
        """Verifica que se puede buscar un usuario por id y coincide la representación."""

        self.gestor_usuario.registrar_nuevo_usuario(nombre="Juan", apellido="Perez", email="", nombre_de_usuario="juanperez", password="1234", rol=0, claustro=0,id=1)
        usuario_bd = self.repo_usuarios.obtener_registro_por_filtro(campo="id",valor=1)

        usuario_metodo_buscar = self.gestor_usuario.buscar_usuario(filtro="id",valor=usuario_bd.id)

        self.assertEqual(usuario_metodo_buscar, usuario_bd.__str__())

    @classmethod
    def setUpClass(cls):
        engine, Session = crear_engine()
        cls.session = Session()
        cls.repo = RepositorioUsuariosSQLAlchemy(cls.session)
        cls.gestor = GestorUsuarios(cls.repo)

    def setUp(self):
        self.session.query(self.repo.modelo).delete()
        self.session.commit()

    def test_actualizar_usuario_sin_id(self):
        """Verifica que no se puede actualizar un usuario sin id."""
        usuario = Usuario(nombre="A", apellido="B", email="a@b.com", nombre_de_usuario="ab", contraseña="123", rol=0, claustro=0)
        with self.assertRaises(ValueError):
            self.gestor.actualizar_usuario(usuario)

    def test_eliminar_usuario_no_existente(self):
        """Verifica que no se puede eliminar un usuario inexistente."""
        with self.assertRaises(ValueError):
            self.gestor.eliminar_usuario(999)

    def test_buscar_usuario_no_existente(self):
        """Verifica que buscar un usuario inexistente lanza ValueError."""
        with self.assertRaises(ValueError):
            self.gestor.buscar_usuario("id", 999)

if __name__ == '__main__':
    unittest.main()