from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, DeclarativeBase
from datetime import datetime

"""
relationship() crea una relación entre dos clases en SQLAlchemy, como por ejemplo uno-a-muchos o muchos-a-muchos.  
Permite acceder desde un objeto a los objetos relacionados en otra tabla, como `usuario.reclamos` o `reclamo.usuario`.
"""
# Base de datos base para los modelos
class Base(DeclarativeBase):
    """
    DeclarativeBase es la clase base moderna para todos los modelos de SQLAlchemy.
    Esta clase base actúa como el punto de partida para todos los modelos ORM y contiene la metadata que describe las tablas asociadas.

    Todos los modelos que representan tablas en la base de datos deben heredar de esta clase.
    """
    pass

# Tabla intermedia para la relación muchos-a-muchos entre usuarios y reclamos
usuario_reclamo = Table(
    'usuario_reclamo', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.id'), primary_key=True),
    Column('reclamo_id', Integer, ForeignKey('reclamos.id'), primary_key=True)
)

class ModeloUsuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String, unique=True)
    nombre_de_usuario = Column(String, unique=True)
    contraseña = Column(String)
    rol = Column(String)
    claustro = Column(String)

    # Relación muchos a muchos con ModeloReclamo
    reclamos = relationship(
        "ModeloReclamo",
        secondary="usuario_reclamo",
        back_populates="usuarios"
    )
    
    def __str__(self):  
        return f"Usuario: Nombre = {self.nombre}, Apellido = {self.apellido}, Email = {self.email}, Nombre_de_usuario = {self.nombre_de_usuario}, Rol = {self.rol}"

    def __init__(self, nombre, apellido, email, nombre_de_usuario, contraseña, rol, claustro):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.nombre_de_usuario = nombre_de_usuario
        self.contraseña = contraseña
        self.rol = rol
        self.claustro = claustro
        
@property
def adherentes_ids(self):
    return [usuario.id for usuario in self.usuarios]

class ModeloReclamo(Base):
    __tablename__ = 'reclamos'

    id = Column(Integer, primary_key=True)
    estado = Column(String, default="pendiente")
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    contenido = Column(String)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    clasificacion = Column(String)
    cantidad_adherentes = Column(Integer, default=1) #Se contabiliza como adherente el usuario que crea el reclamo
    tiempo_estimado = Column(Integer,default=None) #Solo se cambia cuando el reclamo pasa de pendiente -->en proceso
    resuelto_en = Column(Integer,default=None) #Representa la cantidad de días que se tardó en resolver un reclamo
    
    ''' Relación muchos a muchos con Usuario
    Una relación muchos a muchos en SQL permite que múltiples registros de una tabla se asocien con múltiples registros de otra tabla. 
    Esto se implementa mediante una tabla intermedia que contiene claves foráneas de ambas tablas relacionadas. 
    Esta estructura facilita modelar relaciones complejas, como estudiantes inscritos en varios cursos o productos en múltiples órdenes. 
    '''

    usuarios = relationship(
        "ModeloUsuario",
        secondary="usuario_reclamo",
        back_populates="reclamos"
    )


    reclamos_usuarios = Table(
        'reclamos_usuarios',
        Base.metadata,
        Column('reclamo_id', Integer, ForeignKey('reclamos.id')),
        Column('usuario_id', Integer, ForeignKey('usuarios.id'))
    )

    def __str__(self):
        return f"Reclamo: ID = {self.id}, Estado = {self.estado}, Fecha y hora = {self.fecha_hora}, Contenido = {self.contenido}, Usuario ID = {self.usuario_id}, Clasificación = {self.clasificacion}, Tiempo estimado = {self.tiempo_estimado}, Resuelto en = {self.resuelto_en}"


if __name__ == "__main__":
    usuario_1 = ModeloUsuario(nombre="nico",apellido="ramirez",email="nico@gmail.com",nombre_de_usuario="nicora",contraseña=1234,rol=0,claustro="estudiante")
    usuario_2 = ModeloUsuario(nombre="agus",apellido="ramirez",email="agus@gmail.com",nombre_de_usuario="agusra",contraseña=1234,rol=0,claustro="estudiante")

    reclamo_prueba = ModeloReclamo(id=1,contenido="prueba",clasificacion="maestranza",usuario_id=usuario_1.id)

    
    reclamo_prueba.usuarios.append(usuario_2)

    print(reclamo_prueba.usuarios[0].nombre)