import unittest
from modules.repositorio_ABC import Repositorio

class TestRepositorioAbstracto(unittest.TestCase):

    def test_no_se_puede_instanciar(self):
        # Arrange & Act & Assert
        with self.assertRaises(TypeError):
            repo = Repositorio()  # No debe poder instanciar porque es abstracta

    def test_subclase_incompleta(self):
        # Arrange
        class RepoIncompleto(Repositorio):
            def guardar_registro(self, entidad):
                pass  # Método incompleto, faltan otros métodos abstractos

        # Act & Assert
        with self.assertRaises(TypeError):
            repo = RepoIncompleto()  # Falla por métodos abstractos no implementados

    def test_subclase_completa(self):
        # Arrange
        class RepoCompleto(Repositorio):
            def guardar_registro(self, entidad):
                pass
            def obtener_todos_los_registros(self):
                return []
            def modificar_registro(self, entidad_modificada):
                pass
            def obtener_registro_por_filtro(self, filtro, valor):
                return None
            def eliminar_registro_por_id(self, id):
                pass

        # Act
        repo = RepoCompleto()
        # Assert
        self.assertIsInstance(repo, RepoCompleto)


if __name__ == "__main__":
    unittest.main()

