from modules.modelos import ModeloReclamo
from modules.config import crear_engine
from datetime import datetime

# Crear engine y session
engine, Session = crear_engine()
session = Session()

# Obtener todos los reclamos resueltos con resuelto_en en None
def actualizar_resueltos():
    reclamos = session.query(ModeloReclamo).filter_by(estado='resuelto').all()
    for reclamo in reclamos:
        if reclamo.resuelto_en is None:
            # Calcular diferencia en días entre fecha actual y fecha de creación
            dias = (datetime.now().date() - reclamo.fecha_hora.date()).days
            reclamo.resuelto_en = dias
            print(f"Actualizando reclamo ID {reclamo.id}: {dias} días")
    session.commit()
    print("Actualización completada.")

if __name__ == "__main__":
    actualizar_resueltos()
