from datetime import datetime, timedelta
from modules.modelos import ModeloReclamo
from sqlalchemy import func
from modules.config import crear_engine
from modules.repositorio import RepositorioReclamosSQLAlchemy

engine, Session = crear_engine()

session = Session()

"""func es un objeto que provee SQLAlchemy para usar funciones SQL como COUNT(), AVG(), SUM(), MAX(), etc., dentro de tus consultas ORM."""
from sqlalchemy import func
from datetime import datetime, timedelta

class GeneradorReportes:
    def __init__(self, repositorio_reclamos: RepositorioReclamosSQLAlchemy):
        self.repositorio_reclamos = repositorio_reclamos

    def cantidad_total_reclamos(self):
        return self.repositorio_reclamos.session.query(ModeloReclamo).count()

    def cantidad_reclamos_por_estado(self):
        query = self.repositorio_reclamos.session.query(
            ModeloReclamo.estado, 
            func.count(ModeloReclamo.id)
        ).group_by(ModeloReclamo.estado).all()
        return dict(query)

    def cantidad_reclamos_por_departamento(self):
        query = self.repositorio_reclamos.session.query(
            ModeloReclamo.departamento,
            func.count(ModeloReclamo.id)
        ).group_by(ModeloReclamo.departamento).all()
        return dict(query)

    def cantidad_reclamos_por_clasificacion(self):
        query = self.repositorio_reclamos.session.query(
            ModeloReclamo.clasificacion,
            func.count(ModeloReclamo.id)
        ).group_by(ModeloReclamo.clasificacion).all()
        return dict(query)

    def cantidad_promedio_adherentes(self):
        query = self.repositorio_reclamos.session.query(
            func.avg(ModeloReclamo.cantidad_adherentes)
        ).scalar()
        return query or 0

    def reclamos_recientes(self, dias=7):
        fecha_limite = datetime.utcnow() - timedelta(days=dias)
        reclamos = self.repositorio_reclamos.session.query(ModeloReclamo).filter(
            ModeloReclamo.fecha_hora >= fecha_limite
        ).all()
        return reclamos

    def reclamos_por_usuario(self, usuario_id):
        reclamos = self.repositorio_reclamos.session.query(ModeloReclamo).filter_by(
            usuario_id=usuario_id
        ).all()
        return reclamos
    
    def cantidad_reclamos_por_estado_filtrado(self, clasificacion):    
        query = self.repositorio_reclamos.session.query(
            ModeloReclamo.estado,
            func.count(ModeloReclamo.id)
        ).filter_by(clasificacion=clasificacion).group_by(ModeloReclamo.estado).all()
        return dict(query)

    def reclamos_recientes_filtrado(self, clasificacion, dias=7):
        fecha_limite = datetime.utcnow() - timedelta(days=dias)
        return self.repositorio_reclamos.session.query(ModeloReclamo).filter(
            ModeloReclamo.fecha_hora >= fecha_limite,
            ModeloReclamo.clasificacion == clasificacion
        ).all()


if __name__ == '__main__':
    
    # Crear repositorio con la sesión
    repo_reclamos = RepositorioReclamosSQLAlchemy(session)

    # Instanciar el generador de reportes
    generador = GeneradorReportes(repo_reclamos)

    # Ejecutar algunos métodos de análisis
    print("Cantidad total de reclamos:", generador.cantidad_total_reclamos())
    
    # Si agregaste más métodos, prueba otros acá
    # print("Reclamos por estado pendiente:", generador.reclamos_por_estado("pendiente"))