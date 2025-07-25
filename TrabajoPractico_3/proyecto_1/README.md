# Sistema de Reclamos FIUNER

Esta es una aplicación web construida con el framework [Flask](https://flask.palletsprojects.com/). Permite a los usuarios de la Facultad de Ingeniería de la UNER registrar, gestionar y hacer seguimiento de reclamos relacionados con distintos departamentos. El sistema ofrece funcionalidades de registro, inicio de sesión, creación y visualización de reclamos, así como diferentes roles de usuario (Usuario Final, Secretario Técnico, Jefe de Departamento) para una gestión adecuada de los reclamos.

## 🏗Arquitectura General

El proyecto está organizado siguiendo el patrón Modelo-Vista-Controlador (MVC):

- **Modelos:** Definen las clases principales del sistema, como Usuario, Reclamo y sus roles (Usuario Final, Secretario Técnico, Jefe de Departamento). Los modelos gestionan la lógica de negocio y la interacción con la base de datos mediante SQLAlchemy.
- **Vistas:** Son las rutas y plantillas de Flask que gestionan la interacción con el usuario, mostrando formularios, listados de reclamos y paneles según el rol.
- **Controladores:** Son las funciones que reciben las solicitudes del usuario, procesan la lógica necesaria y devuelven una respuesta adecuada.

El código está dividido en módulos para separar la lógica de usuarios, reclamos y autenticación. Cada rol de usuario tiene permisos y vistas específicas para sus tareas. El diagrama de relaciones entre clases se encuentra en la carpeta [docs].

## 📑Dependencias

1. Flask
2. Flask-Login
3. Flask-Session
4. SQLAlchemy
5. Jinja2
6. reportlab
7. wordcloud
8. nltk
9. scikit-learn
10. numpy
11. cachelib
12. pytest
13. pytest-cov

## 🚀Cómo Ejecutar el Proyecto

1. **Clonar o descargar** el repositorio.
2. **Crear** un entorno virtual.
3. **Instalar las dependencias**:

   En la terminal escriba los siguientes comandos en orden:

   1) ./venv/Scrpt/Activate

      (para saber que se activo el entorno se visualizara al principio de la ruta de direccion un mensaje en verde que diga .venv)
   2) pip install -r requirements.txt

      **El archivo `requirements.txt` se encuentran en la carpeta [deps](./deps) del proyecto.**
   3) Dirigirse al archivo [Server](server.py) y ejecutarlo

   Aparecera un mensaje en la terminal, con el CTRL apretado hacer click en el link que diga **127.0.0.1:5000**

## 💻Uso de la aplicación

La aplicación permite a los usuarios registrarse e iniciar sesión para acceder a las funcionalidades según su rol. Una vez autenticados, pueden crear y visualizar reclamos, y los roles administrativos pueden gestionarlos.

- **Ruta principal** (`/`): Muestra la página de inicio y acceso al sistema.
- **(`/iniciar_sesion`)**: Permite a los usuarios iniciar sesión.
- **(`/registrarse`)**: Permite a los nuevos usuarios registrarse.
- **(`/mis_reclamos`)**: Muestra el listado de reclamos del usuario autenticado.
- **(`/crear_reclamos`)**: Permite crear un nuevo reclamo.
- **(`/analitica_reclamos`)**: Panel de control para Jefe de Departamento y Secretario Técnico, donde pueden gestionar reclamos.
- **(`/logout`)**: Cierra la sesión del usuario.
- **`(/inicio_usuario)`**: Muestra la pagina de inicio para usuarios logueados junto ocn los botones de acceso a las demas rutas dependiendo del rol del usuario
- **`(/adherirse)`**: endpoint que muestra reclamos para adherirse luego de crear un reclamo
- **`(/listar_reclamos)`**: muestra todos los reclamos pendientes del sistema
- **`(/editar_reclamo)`**: permite editar un reclamo ya creado o adherirle una imagen
- **`(/manejo_reclamos)`**: dashboard para los jefes y el secretario tecnico para resolver reclamos
- **`(/ayuda)`**: manual de uso de la web para el usuario

Para acceder a la mayoría de los endpoints es necesario estar autenticado. El flujo típico es: registro → inicio de sesión → acceso a funcionalidades según el rol.

## 🙎‍♀️🙎‍♂️Autores

- Grioni Agustín
- Ramirez Nicolas
