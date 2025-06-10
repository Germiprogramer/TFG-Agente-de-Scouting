# ⚽ TFG - Agente de Scouting Inteligente

Este Trabajo de Fin de Grado tiene como objetivo el desarrollo de un agente de inteligencia artificial capaz de asistir en tareas de **scouting deportivo**, automatizando el análisis de jugadores a partir de datos objetivos. El sistema permite realizar consultas personalizadas en lenguaje natural y obtener respuestas basadas en estadísticas avanzadas y visualizaciones gráficas.

El proyecto se basa en dos fuentes de datos principales:

- **StatsBomb Open Data**, una plataforma especializada que proporciona datos detallados de eventos de partidos (pases, tiros, duelos, etc.) para diferentes competiciones de fútbol profesional. Se adquieren mediante su repositorio público **statsbombpy**.
- **FIFA (Kaggle)**, un conjunto de datos que complementa el análisis con información económica aproximada sobre jugadores y clubes, como salarios, valores de mercado y presupuestos.

A partir de estas fuentes, se construye una base de datos estructurada que sirve como núcleo para el funcionamiento del agente inteligente, orientado a facilitar la detección de talento en el fútbol profesional.


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
  Contiene los notebooks que documentan paso a paso todo el proceso de desarrollo, divididos en subcarpetas.

  Pipeline principal del proyecto, estructurado en fases claras:
  
  1. `Limpieza inicial.ipynb`: carga de datos originales y depuración básica.  
  2. `Extracción de métricas.ipynb`: cálculo de estadísticas para evaluar el rendimiento.  
  3. `Cálculo del rating.ipynb`: generación de la puntuación final de cada jugador.  
  4. `Limpieza previa al almacenamiento.ipynb`: ajustes antes de migrar los datos.  
  5. `Almacenamiento.ipynb`: creación del esquema y exportación a PostgreSQL.  
  6. `Evaluación agente.ipynb`: testeo del agente con consultas de ejemplo.

  Además, se incluye **`graficos.ipynb`**, un cuaderno dedicado exclusivamente a la generación de gráficos para enriquecer tanto el agente como el documento del proyecto.

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
