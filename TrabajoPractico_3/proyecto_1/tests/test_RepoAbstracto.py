import unittest
from modules.repositorio_ABC import Repositorio

class TestRepositorioAbstracto(unittest.TestCase):

    def test_no_se_puede_instanciar(self):
        with self.assertRaises(TypeError):
            repo = Repositorio()  # No debe poder instanciar porque es abstracta

    def test_subclase_incompleta(self):
        class RepoIncompleto(Repositorio):
            def guardar_registro(self, entidad):
                pass #pragma: no cover

        with self.assertRaises(TypeError):
            repo = RepoIncompleto()  # Falla por métodos abstractos no implementados

    def test_subclase_completa(self):
        class RepoCompleto(Repositorio):
            def guardar_registro(self, entidad):
                pass #pragma: no cover
            def obtener_todos_los_registros(self):
                return [] #pragma: no cover
            def modificar_registro(self, entidad_modificada):
                pass #pragma: no cover
            def obtener_registro_por_filtro(self, filtro, valor):
                return None #pragma: no cover
            def eliminar_registro_por_id(self, id):
                pass #pragma: no cover

        # Esta sí debe instanciar sin problemas
        repo = RepoCompleto()
        self.assertIsInstance(repo, RepoCompleto)


if __name__ == "__main__": #pragma: no cover
    unittest.main()
