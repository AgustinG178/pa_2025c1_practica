# Archivo de test para realizar pruebas unitarias del modulo1
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,session
from modules.usuarios import UsuarioFinal
from modules.modelos import Base,Usuario,Reclamo,Departamento
from modules.repositorio import RepositorioUsuariosSQLAlchemy,RepositorioReclamosSQLAlchemy

class TestRepositorios(unittest.TestCase):

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
    def tearDown(self):

        """
        Luego de cada test, se cierra la base de datos
        """
        self.session.close()

        self.engine.dispose()
    
    def test_guardar_usuario(self):

        """
        Se testea el funcionamiento del repositorio "RepositorioUsuariosSQLAlchemy" para guardar un usuario
        """
        p_usuario = UsuarioFinal(nombre="Juan", email="juan@gmai.com", contraseña="juan123", apellido="pereira", nombre_de_usuario="juanpe124",claustro="estudiante",rol=None)

        usuario_tabla = p_usuario.map_to_modelo_bd()

        self.repo_usuarios.guardar_registro(usuario=usuario_tabla)

        usuario_base_datos = self.session.query(Usuario).filter_by(nombre_de_usuario="juanpe124").first()

        self.assertIsNotNone(usuario_base_datos)
        self.assertEqual(usuario_base_datos.email, "juan@gmai.com")

    def test_guardar_reclamo(self):
                
        """
        Se testea el funcionamiento del repositorio "RepositorioReclamosSQLAlchemy" para guardar un reclamo
        """


        p_usuario = UsuarioFinal(nombre="Juan", email="juan@gmai.com", contraseña="juan123", apellido="pereira", nombre_de_usuario="juanpe124",claustro="estudiante",rol=None)

        usuario_tabla = p_usuario.map_to_modelo_bd()

        dpto_prueba = Departamento(nombre="matematica",jefe=usuario_tabla.id)

        p_reclamo = Reclamo(contenido="hahahahaha",usuario_id=usuario_tabla.id,departamento_id=dpto_prueba.id)

        self.repo_reclamos.guardar_registro(reclamo=p_reclamo)

        reclamo_base_datos = self.session.query(Reclamo).filter_by(id=p_reclamo.id).first()
        self.assertIsNotNone(p_reclamo)

        self.assertEqual(reclamo_base_datos.id,p_reclamo.id)

    def test_obtener_todos_los_registros(self):

        """
        Se prueba el metodo obtener_todos_los_registros de usuarios y reclamos
        """

        p_usuario = UsuarioFinal(nombre="Juan", email="juan@gmai.com", contraseña="juan123", apellido="pereira", nombre_de_usuario="juanpe124",claustro="estudiante",rol=None)

        usuario_tabla = p_usuario.map_to_modelo_bd()

        dpto_prueba = Departamento(nombre="matematica",jefe=usuario_tabla.id)

        p_reclamo = Reclamo(contenido="hahahahaha",usuario_id=usuario_tabla.id,departamento_id=dpto_prueba.id)
        
        

        self.repo_usuarios.guardar_registro(usuario=usuario_tabla)

        self.repo_reclamos.guardar_registro(reclamo=p_reclamo)

        reclamos_base_totales = self.repo_reclamos.obtener_todos_los_registros()

        usuarios_base_totales = self.repo_usuarios.obtener_todos_los_registros()

        #Se prueba no solo que se devuelva una lista, sino que se devuelva correctamente el reclamo/usuario
        self.assertIsInstance(reclamos_base_totales,list)
        self.assertEqual(reclamos_base_totales[0].id,p_reclamo.id)

        self.assertIsInstance(usuarios_base_totales,list)
        self.assertEqual(usuarios_base_totales[0].nombre,"Juan")

    def test_obtener_registro_por_filtro(self):

        """
        Se prueba el funcionamiento del método para obtener un usuario o reclamo mediante un filtro  (id,nombre,etc)
        """
        p_usuario = UsuarioFinal(nombre="Juan", email="juan@gmai.com", contraseña="juan123", apellido="pereira", nombre_de_usuario="juanpe124",claustro="estudiante",rol=None)

        usuario_tabla = p_usuario.map_to_modelo_bd()

        dpto_prueba = Departamento(nombre="matematica",jefe=usuario_tabla.id)

        p_reclamo = Reclamo(contenido="hahahahaha",usuario_id=usuario_tabla.id,departamento_id=dpto_prueba.id)
        
        self.repo_usuarios.guardar_registro(usuario=usuario_tabla)

        self.repo_reclamos.guardar_registro(reclamo=p_reclamo)

        reclamo_base_filtro = self.session.query(Reclamo).filter_by(usuario_id=usuario_tabla.id).first()

        #probamos el método para los reclamos

        reclamo_metodo_filtro_repo = self.repo_reclamos.obtener_registro_por_filtro("usuario_id",usuario_tabla.id)

        self.assertEqual(reclamo_base_filtro,reclamo_metodo_filtro_repo)
         
        #Probamos el método para los usuarios

        usuario_base_filtro = self.session.query(Usuario).filter_by(nombre = usuario_tabla.nombre).first()
        usuario_metodo_filtro_repo = self.repo_usuarios.obtener_registro_por_filtro("nombre",usuario_tabla.nombre)

        self.assertEqual(usuario_base_filtro,usuario_metodo_filtro_repo)

    def test_eliminar_registro_por_id(self):

        """
        Se prueba el método para eliminar registro por id tanto para usuarios como para reclamos
        """
        p_usuario = UsuarioFinal(nombre="Juan", email="juan@gmai.com", contraseña="juan123", apellido="pereira", nombre_de_usuario="juanpe124",claustro="estudiante",rol=None)

        usuario_tabla = p_usuario.map_to_modelo_bd()

        dpto_prueba = Departamento(nombre="matematica",jefe=usuario_tabla.id)

        p_reclamo = Reclamo(contenido="hahahahaha",usuario_id=usuario_tabla.id,departamento_id=dpto_prueba.id)
        
        self.repo_usuarios.guardar_registro(usuario=usuario_tabla)

        self.repo_reclamos.guardar_registro(reclamo=p_reclamo)

        #Prueba para reclamos
        self.repo_reclamos.eliminar_registro_por_id(id=p_reclamo.id)

        #Como no hay reclamos, el return de obtener_todos_los_registros será una lista vacia

        lista_reclamos = self.repo_reclamos.obtener_todos_los_registros()

        self.assertNotIn(p_reclamo,lista_reclamos)

        #Realizamos lo mismo para usuarios
        
        self.repo_usuarios.eliminar_registro_por_id(id=usuario_tabla.id)

        lista_usuarios = self.repo_usuarios.obtener_todos_los_registros()

        self.assertNotIn(usuario_tabla,lista_usuarios)
        
    def test_modificar_registro(self):

        """
        Se prueba el método modificar_registro tanto para el repositorio usuario como para repositorio reclamos
        """

        p_usuario = UsuarioFinal(nombre="Juan", email="juan@gmai.com", contraseña="juan123", apellido="pereira", nombre_de_usuario="juanpe124",claustro="estudiante",rol=None)

        usuario_tabla = p_usuario.map_to_modelo_bd()

        dpto_prueba = Departamento(nombre="matematica",jefe=usuario_tabla.id)

        p_reclamo = Reclamo(contenido="hahahahaha",usuario_id=usuario_tabla.id,departamento_id=dpto_prueba.id)
        
        self.repo_usuarios.guardar_registro(usuario=usuario_tabla)

        self.repo_reclamos.guardar_registro(reclamo=p_reclamo)

        usuario_modificado = UsuarioFinal(nombre="Juan", email="juan@hotmail.com", contraseña="juan123", apellido="pereira", nombre_de_usuario="juanpe124",claustro="estudiante",rol=None)

        usuario_modificado_tabla = usuario_modificado.map_to_modelo_bd()

        usuario_modificado_tabla.id = usuario_tabla.id #Debemos asegurarnos que el usuario modificado posee el mismo id que el usuario inicial, caso contrario

        self.repo_usuarios.modificar_registro(usuario_modificado=usuario_modificado_tabla)

        #usuario_repo teoricamente es la entidad con el email modificado, de así serlo el test debería ser positivo
        usuario_repo = self.session.query(Usuario).filter_by(nombre="Juan").first()


        self.assertEqual(usuario_repo.email,usuario_modificado_tabla.email)
        
        #Realizamos la misma lógica pero para reclamos

        reclamo_modificado = Reclamo(contenido="hahahahaha",usuario_id=usuario_tabla.id,departamento_id=dpto_prueba.id)

        reclamo_modificado.id,reclamo_modificado.estado = p_reclamo.id, "resuelto"

        self.repo_reclamos.modificar_registro(reclamo_modificado=reclamo_modificado)

        reclamo_bd = self.session.query(Reclamo).filter_by(usuario_id=usuario_tabla.id).first()


        self.assertEqual(reclamo_bd.estado,reclamo_modificado.estado)

    def test_actualizar_reclamo(self):

        p_usuario = UsuarioFinal(nombre="Juan", email="juan@gmai.com", contraseña="juan123", apellido="pereira", nombre_de_usuario="juanpe124",claustro="estudiante",rol=None)

        usuario_tabla = p_usuario.map_to_modelo_bd()

        dpto_prueba = Departamento(nombre="matematica",jefe=usuario_tabla.id)

        p_reclamo = Reclamo(contenido="hahahahaha",usuario_id=usuario_tabla.id,departamento_id=dpto_prueba.id)
        
        self.repo_usuarios.guardar_registro(usuario=usuario_tabla)

        self.repo_reclamos.guardar_registro(reclamo=p_reclamo)

        p_reclamo.estado = "resuelto"

        self.repo_reclamos.actualizar_reclamo(reclamo=p_reclamo)
        

        self.assertEqual(p_reclamo,"resuelto")

if __name__ == "__main__":
    unittest.main()