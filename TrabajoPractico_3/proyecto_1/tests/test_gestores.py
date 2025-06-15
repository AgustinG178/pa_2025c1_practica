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


class TestGestorReclamos(unittest.TestCase):
    """Tests para la gestión de reclamos y usuarios."""

    def setUp(self):
        """
        Se crea una base de datos de solo para pruebas
        """
        self.engine = create_engine('sqlite:///:memory:')

        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)

        self.session = self.Session()

        self.repo_usuarios = RepositorioUsuariosSQLAlchemy(self.session)

        self.repo_reclamos = RepositorioReclamosSQLAlchemy(self.session)

        self.gestor_usuario = GestorUsuarios(self.repo_usuarios)

        self.gestor_reclamo = GestorReclamo(self.repo_reclamos)  


    def tearDown(self):

        """
        Luego de cada test, se cierra la base de datos
        """
        self.session.close()

        self.engine.dispose()
    
    def test_crear_reclamo(self):
        """Verifica que se puede crear un reclamo y que es instancia de Reclamo."""
        usuario = Usuario(nombre="Juan", apellido="Perez",id=1, email="", nombre_de_usuario="juanperez", contraseña="1234", rol=0, claustro=0)

        p_reclamo = self.gestor_reclamo.crear_reclamo(usuario=usuario,descripcion= "reclamo de prueba",departamento="dpto de prueba",clasificacion="maestranza")

        self.assertIsInstance(p_reclamo, Reclamo)

    def test_buscar_reclamo_por_usuario(self):
        """Verifica que se puede buscar un reclamo por usuario y coincide el contenido."""
        usuario = Usuario(nombre="Juan", apellido="Perez",id=1, email="", nombre_de_usuario="juanperez", contraseña="1234", rol=0, claustro=0)

        self.repo_usuarios.guardar_registro(self.repo_usuarios._map_entidad_a_modelo(usuario))

        p_reclamo = self.gestor_reclamo.crear_reclamo(usuario=usuario,descripcion= "reclamo de prueba",departamento="dpto de prueba",clasificacion="maestranza")

        self.repo_reclamos.guardar_registro(self.repo_reclamos.mapear_reclamo_a_modelo(p_reclamo))
        
        reclamo_base_usuario = self.gestor_reclamo.buscar_reclamos_por_usuario(usuario)[0]

        self.assertEqual(p_reclamo.contenido, reclamo_base_usuario.contenido)

    def test_actualizar_estado_reclamo(self):
        """Verifica que se puede actualizar el estado de un reclamo a 'resuelto'."""
        usuario = Usuario(nombre="Juan", apellido="Perez", email="",id=1, nombre_de_usuario="juanperez", contraseña="1234", rol=0, claustro=0)

        self.repo_usuarios.guardar_registro(self.repo_usuarios._map_entidad_a_modelo(usuario))

        p_reclamo = self.gestor_reclamo.crear_reclamo(usuario=usuario,descripcion= "reclamo de prueba",departamento="dpto de prueba",clasificacion="maestranza")

        # Guardar el reclamo y obtener el modelo guardado
        modelo_reclamo = self.repo_reclamos.mapear_reclamo_a_modelo(p_reclamo)
        self.repo_reclamos.guardar_registro(modelo_reclamo)

        # Obtener el reclamo guardado (con id asignado)
        reclamo_guardado = self.repo_reclamos.obtener_registro_por_filtro(filtro="usuario_id", valor=usuario.id)
        print(f"[DEBUG] Reclamo guardado: {reclamo_guardado.id}")


        # Actualizar el estado del reclamo
        self.gestor_reclamo.actualizar_estado_reclamo(reclamo=reclamo_guardado, usuario=usuario)

        # Recuperar el reclamo actualizado por id
        reclamo_actualizado = self.repo_reclamos.obtener_registro_por_filtro(filtro="id", valor=reclamo_guardado.id)
        print(f"[DEBUG] Reclamo actualizado: {reclamo_actualizado.id}. Estado: {reclamo_actualizado.estado}")
        self.assertEqual(reclamo_actualizado.estado, "resuelto")


    def test_eliminar_reclamo_por_id(self):
        """Verifica que se puede eliminar un reclamo por id y que ya no existe."""
        usuario = Usuario(nombre="Juan", apellido="Perez", email="",id=1, nombre_de_usuario="juanperez", contraseña="1234", rol=0, claustro=0)

        self.repo_usuarios.guardar_registro(self.repo_usuarios._map_entidad_a_modelo(usuario))

        p_reclamo = self.gestor_reclamo.crear_reclamo(usuario=usuario,descripcion= "reclamo de prueba",departamento="dpto de prueba",clasificacion="maestranza")

        modelo_reclamo = self.repo_reclamos.mapear_reclamo_a_modelo(p_reclamo)
        self.repo_reclamos.guardar_registro(modelo_reclamo)

        # Obtener el reclamo guardado (con id asignado)
        reclamo_guardado = self.repo_reclamos.obtener_registro_por_filtro(filtro="usuario_id", valor=usuario.id)

        # Eliminar el reclamo por id
        self.repo_reclamos.eliminar_registro_por_id(reclamo_guardado.id)

        # Verificar que el reclamo ya no existe
        reclamo_eliminado = self.repo_reclamos.obtener_registro_por_filtro(filtro="id", valor=reclamo_guardado.id)
        self.assertIsNone(reclamo_eliminado)

    def test_agregar_adherente(self):
        """Verifica que se puede agregar un adherente y se actualiza la cantidad."""
        p_usuario_1 = Usuario(nombre="Juan", apellido="Perez", email="perer@gmail.com",id=1, nombre_de_usuario="juanperez", contraseña="1234", rol=0, claustro=0)
        p_usuario_2 = Usuario(nombre="Ana", apellido="Lopez", email="ana@gmail.com",id=2, nombre_de_usuario="analopez", contraseña="1234", rol=0, claustro=0)

        self.repo_usuarios.guardar_registro(self.repo_usuarios._map_entidad_a_modelo(p_usuario_1))  
        self.repo_usuarios.guardar_registro(self.repo_usuarios._map_entidad_a_modelo(p_usuario_2))

        p_reclamo = self.gestor_reclamo.crear_reclamo(usuario=p_usuario_1, descripcion="reclamo de prueba", departamento="dpto de prueba", clasificacion="maestranza")

        self.repo_reclamos.guardar_registro(self.repo_reclamos.mapear_reclamo_a_modelo(p_reclamo))

        #Agregamos a p_usuario_2 como adherente al reclamo
        self.repo_reclamos.guardar_registro(self.repo_reclamos.mapear_reclamo_a_modelo(p_reclamo))

  
        reclamo_guardado = self.repo_reclamos.obtener_registro_por_filtro(filtro="usuario_id", valor=p_usuario_1.id)

        self.gestor_reclamo.agregar_adherente(reclamo_id=reclamo_guardado.id, usuario=p_usuario_2)

        reclamo_actualizado = self.repo_reclamos.obtener_registro_por_filtro(filtro="id", valor=reclamo_guardado.id)
        self.assertEqual(reclamo_actualizado.cantidad_adherentes, 2)

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

class TestGestorUsuariosExtra(unittest.TestCase):
    """Tests para casos de error en la gestión de usuarios."""

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