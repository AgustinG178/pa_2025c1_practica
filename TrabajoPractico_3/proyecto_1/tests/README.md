## **Cómo ejecutar los tests con [pytest](vscode-file://vscode-app/c:/Users/agugr/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) y generar un reporte de cobertura**

Para ejecutar los tests y generar un reporte de cobertura de código, sigue estos pasos:

**Ejecutar los tests con [pytest](vscode-file://vscode-app/c:/Users/agugr/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) y calcular la cobertura:**

**pytest** **--cov**

## **Por qué [pytest](vscode-file://vscode-app/c:/Users/agugr/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) genera warnings y por qué no es relevante resolverlos en este contexto**

Durante la ejecución de las pruebas con [pytest](vscode-file://vscode-app/c:/Users/agugr/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html), se generan ciertos **warnings** relacionados con dependencias externas y configuraciones específicas del entorno. A continuación, se explican las causas de estos warnings y por qué no es necesario resolverlos en el contexto actual del programa:

---

### **1. Warnings relacionados con `Flask-Session`**

* **Causa:**
  * Los warnings indican que ciertas configuraciones de `Flask-Session`, como `SESSION_FILE_DIR` y `FileSystemSessionInterface`, están marcadas como obsoletas y serán eliminadas en futuras versiones.
  * Estos warnings son generados por la biblioteca `Flask-Session` y no por el código del programa.
* **Por qué no es relevante resolverlo:**
  * El programa actual funciona correctamente con la versión de `Flask-Session` instalada.
  * Estos cambios solo serán necesarios si se actualiza a una versión futura de `Flask-Session`. Dado que el programa cumple con los requerimientos actuales, no es necesario realizar ajustes inmediatos.

---

### **2. Warnings relacionados con `ResourceWarning: unclosed database`**

* **Causa:**
  * Estos warnings ocurren porque algunas conexiones a la base de datos SQLite no se están cerrando explícitamente en las pruebas.
  * Esto no afecta el funcionamiento del programa en un entorno de producción, ya que las conexiones se manejan correctamente en el flujo normal de ejecución.
* **Por qué no es relevante resolverlo:**
  * Los warnings solo aparecen en el entorno de pruebas y no afectan el comportamiento del programa en producción.
  * Resolver estos warnings requeriría ajustes en las pruebas unitarias, pero no aportaría mejoras significativas al programa en sí.

---

### **3. Warnings relacionados con [datetime.datetime.utcnow()](vscode-file://vscode-app/c:/Users/agugr/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)**

* **Causa:**

  * El uso de [datetime.datetime.utcnow()](vscode-file://vscode-app/c:/Users/agugr/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) genera un warning porque está marcado como obsoleto en versiones futuras de Python. Se recomienda usar objetos con zona horaria (`timezone-aware`), como [datetime.now(timezone.utc)](vscode-file://vscode-app/c:/Users/agugr/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html).
* **Por qué no es relevante resolverlo:**

  * El programa actual utiliza [datetime.datetime.utcnow()](vscode-file://vscode-app/c:/Users/agugr/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) de manera funcional y cumple con los requerimientos.
  * Cambiar a [datetime.now(timezone.utc)](vscode-file://vscode-app/c:/Users/agugr/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) no afecta el comportamiento del programa en su estado actual y solo sería necesario si se actualiza a una versión futura de Python.

  ## ¿como solucionarlos?
* Hay 2 formas para capturar warnings generados por pytest,

  * 1) La primera es actulizando el codigo de bibliotecas externas
    2) Pytest provee una guia de como implementar el modulo `warnings` para poder capturar dichas advetencias y que no generar problemas a la hora de ejecutar las pruebas
       enlace provisto por pytest: [https://docs.pytest.org/en/stable/how-to/capture-warnings.html](https://docs.pytest.org/en/stable/how-to/capture-warnings.html)
