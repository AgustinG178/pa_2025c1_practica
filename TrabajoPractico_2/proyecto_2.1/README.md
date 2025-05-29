
# 📚 Sistema de Información Universitaria

Este proyecto es una aplicación de consola desarrollada en Python para la gestión de la comunidad académica de una facultad. Permite administrar estudiantes, profesores, cursos, departamentos y facultades, simulando un sistema universitario básico.

---

## 🏗️ Arquitectura General

El sistema está organizado en módulos y clases que representan los distintos actores y entidades de una universidad:

- **Estudiante** y **Profesor**: Heredan de la clase abstracta `Persona`.
- **Curso**: Relaciona estudiantes y profesores.
- **Departamento**: Agrupa cursos y profesores, y tiene un director.
- **Facultad**: Contiene departamentos, cursos, estudiantes y profesores.
- **Módulo de archivos**: Permite leer datos iniciales desde archivos `.txt`.

La interacción principal se realiza a través del archivo [`consola.py`](consola.py), que ofrece un menú interactivo para gestionar la información.

---

## 📂 Estructura de Carpetas


---
## ⚙️ Dependencias

- **Python 3.11+**
---
## 🚀 Cómo Ejecutar el Proyecto

1. **Clona o descarga** el repositorio.
2. Asegúrate de tener Python 3.11 o superior.
3. Ejecuta el programa principal desde la terminal:

   ```bash
   python consola.py
   ```

   ## Autores

Grioni, Agustín

Ramirez, Nicolas
