# ⚽ TFG - Agente de Scouting Inteligente

## Estructura del repositorio

El repositorio está organizado en diferentes carpetas, cada una con un propósito específico dentro del flujo de trabajo del proyecto. A continuación, se detalla la función de cada componente:

---

### Carpetas principales

- **`datos/`**  
  Contiene los archivos de entrada y resultados intermedios generados durante el proceso de análisis y construcción de la base de datos.

- **`evaluacion_agente/`**  
  Scripts y recursos utilizados para validar el rendimiento del agente, comparando los resultados obtenidos frente a las respuestas esperadas.

- **`funciones_analisis/`**  
  Módulo que agrupa funciones personalizadas en Python para extraer estadísticas avanzadas a partir de los datos de eventos de partidos.

- **`imagenes/`**  
  Recursos gráficos y visualizaciones utilizadas en el desarrollo del TFG o en la interfaz del agente.

- **`notebook/`**  
  Contiene los notebooks que documentan paso a paso todo el proceso de desarrollo, divididos en tres subcarpetas:

  Pipeline principal del proyecto, estructurado en fases claras:
    1. `Limpieza inicial.ipynb`: carga de datos originales y depuración básica.  
    2. `Extracción de métricas.ipynb`: cálculo de estadísticas para evaluar el rendimiento.  
    3. `Cálculo del rating.ipynb`: generación de la puntuación final de cada jugador.  
    4. `Limpieza previa al almacenamiento.ipynb`: ajustes antes de migrar los datos.  
    5. `Almacenamiento.ipynb`: creación del esquema y exportación a PostgreSQL.  
    6. `Evaluación agente.ipynb`: testeo del agente con consultas de ejemplo.  
    7. `graficos.ipynb`: generación de gráficos radar y visualizaciones por plantilla.

  - **`intento_ratings/`**  
    Primeros experimentos con modelos de regresión para calcular el rating de los jugadores.

  - **`modelos_de_agente/csv/`**  
    Datos de ejemplo y archivos de apoyo usados en las pruebas del agente.

  - **`notebook_auxiliares/`**
    Otros cuadernos con lo que se desarrollaron partes del proyecto, pero sin relevancia excesiva.  
    

- **`style/`**  
  Archivos CSS aplicados a la interfaz desarrollada con Streamlit.

---

### Archivos principales

- **`agente_sql.py`**  
  Define la lógica del agente inteligente basado en LangChain y su conexión con la base de datos relacional (SQL).

- **`main.py`**  
  Punto de entrada de la aplicación. Ejecuta la interfaz de usuario en Streamlit para interactuar con el agente.
