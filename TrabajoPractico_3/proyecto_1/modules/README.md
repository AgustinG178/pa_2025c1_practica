
# Módulos del Sistema de Gestión de Reclamos

Este directorio contiene los módulos principales del sistema de atención y seguimiento de reclamos para la Facultad de Ingeniería de la UNER. Aquí se implementa la lógica de negocio, acceso a datos, generación de reportes, gráficos y el clasificador de reclamos.

---

## Estructura de carpetas

- **config.py**: Configuración de la base de datos y la aplicación Flask.
- **modelos.py**: Definición de los modelos ORM (usuarios, reclamos, etc.).
- **repositorio.py / repositorio_ABC.py**: Repositorios para acceso y manipulación de datos.
- **gestor_usuario.py / gestor_reclamos.py / gestor_base_datos.py**: Lógica de negocio para usuarios, reclamos y base de datos.
- **graficos.py**: Generación de gráficos estadísticos (torta, histograma, nube de palabras).
- **reportes.py**: Generación de reportes en PDF y HTML.
- **monticulos.py**: Implementación de montículos para cálculo eficiente de medianas.
- **classifier.py / clasificador_de_reclamos/**: Clasificador automático de reclamos usando machine learning.
- **usuarios.py / reclamo.py**: Clases de dominio para usuarios y reclamos.
- **gestor_imagen_reclamo.py**: Gestión de imágenes asociadas a reclamos.
- **login.py**: Lógica de autenticación y manejo de sesiones.
- **text_vectorizer.py**: Utilidades para procesamiento de texto y vectorización.

## Dependencias necesarias

Instala las siguientes dependencias para ejecutar los módulos correctamente:

- [Flask](https://flask.palletsprojects.com/)
- [Flask-Login](https://flask-login.readthedocs.io/)
- [Flask-Session](https://pythonhosted.org/Flask-Session/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Jinja2](https://jinja.palletsprojects.com/)
- [reportlab](https://www.reportlab.com/dev/docs/)
- [wordcloud](https://github.com/amueller/word_cloud)
- [nltk](https://www.nltk.org/)
- [scikit-learn](https://scikit-learn.org/)
- [numpy](https://numpy.org/)
- [cachelib](https://github.com/pallets/cachelib)
- [pytest](https://docs.pytest.org/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)

Puedes instalar todas las dependencias con:

```bash
pip install -r requirements.txt
```
