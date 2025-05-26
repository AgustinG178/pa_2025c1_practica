# Sistema de Reclamos FIUNER

Esta es una aplicación web construida con el framework [Flask](https://flask.palletsprojects.com/). Permite a los usuarios de la Facultad de Ingeniería de la UNER registrar, gestionar y hacer seguimiento de reclamos relacionados con distintos departamentos. El sistema ofrece funcionalidades de registro, inicio de sesión, creación y visualización de reclamos, así como diferentes roles de usuario (Usuario Final, Secretario Técnico, Jefe de Departamento) para una gestión adecuada de los reclamos.

## 🏗Arquitectura General

El proyecto está organizado siguiendo el patrón Modelo-Vista-Controlador (MVC):

- **Modelos:** Definen las clases principales del sistema, como Usuario, Reclamo y sus roles (Usuario Final, Secretario Técnico, Jefe de Departamento). Los modelos gestionan la lógica de negocio y la interacción con la base de datos mediante SQLAlchemy.
- **Vistas:** Son las rutas y plantillas de Flask que gestionan la interacción con el usuario, mostrando formularios, listados de reclamos y paneles según el rol.
- **Controladores:** Son las funciones que reciben las solicitudes del usuario, procesan la lógica necesaria y devuelven una respuesta adecuada.

El código está dividido en módulos para separar la lógica de usuarios, reclamos y autenticación. Cada rol de usuario tiene permisos y vistas específicas para sus tareas. El diagrama de relaciones entre clases se encuentra en la carpeta [docs].

## 📑Dependencias

1. ***Python 3.13.2***
2. ***Flask***
3. ***SQLalchemy***
4. ***flask***
5. ***flask_login***
6. ***flask_session***
7. ***flask_bootstrap***
8. ***sqlalchemy***
9. ***sqlalchemy.orm***
10. ***sqlalchemy.ext.declarative***
11. ***datetime***
12. ***functools***
13. ***werkzeug.security***
14. ***abc***

## 🚀Cómo Ejecutar el Proyecto
1. **Clonar o descargar** el repositorio.

2. **Crear** un entorno virtual.

3. **Instalar las dependencias**:

   En la terminal escriba los siguientes comandos en orden:

      1) ./venv/Scrpt/Activate

            (para saber que se activo el entorno se visualizara al principio de la ruta de direccion un mensaje en verde que diga .venv)

      2) pip install -r requirements.txt

         **El archivo `requirements.txt` se encuentran en la carpeta [deps](./deps) del proyecto.**

4. Dirigirse al archivo [Server](server.py) y ejecutarlo

      Aparecera un mensaje en la terminal, con el CTRL apretado hacer click en el link que diga **127.0.0.1:5000**


## 💻Uso de la aplicación

Explica la funcionalidad de tu aplicación:  
- Cómo se navega por las rutas o URLs.
- Si requiere autenticación, describe el flujo de login o registro.

**Ejemplo**:
- **Ruta principal** (`/`): muestra la página de inicio.
- **Ruta de usuario** (`/user/<id>`): muestra información del usuario.!

## 🙎‍♀️🙎‍♂️Autores

- Grioni Agustín
- Ramirez Nicolas
