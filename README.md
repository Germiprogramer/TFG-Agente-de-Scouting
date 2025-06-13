# ⚽ TFG - Agente de Scouting Inteligente
Como parte de un Trabajo de Fin de Grado, en este repositorio se muestra el desarrollo de un agente de inteligencia artificial capaz de asistir en tareas de **scouting deportivo**, automatizando el análisis de jugadores a partir de datos objetivos. El sistema permite realizar consultas personalizadas en lenguaje natural y obtener respuestas basadas en estadísticas avanzadas y visualizaciones gráficas.

El proyecto se basa en dos fuentes de datos principales:

- **StatsBomb Open Data**, una plataforma especializada que proporciona datos detallados de eventos de partidos (pases, tiros, duelos, etc.) para diferentes competiciones de fútbol profesional. Se adquieren mediante su repositorio público **statsbombpy**.
- **FIFA (Kaggle)**, un conjunto de datos que complementa el análisis con información económica aproximada sobre jugadores y clubes, como salarios, valores de mercado y presupuestos.

A partir de estas fuentes, se construye una base de datos estructurada que sirve como núcleo para el funcionamiento del agente inteligente, orientado a facilitar la detección de talento en el fútbol profesional.

### 📁 Carpetas principales

- **`datos/`**  
  Archivos preliminares y resultados intermedios generales producidos durante las etapas de análisis hasta la construcción de la base de datos.

- **`evaluacion_agente/`**  
  Incluye el *ground truth* y los resultados de la evaluación del rendimiento del agente.

- **`funciones_analisis/`**  
  Carpeta que incluye las funciones que se han utilizado en los distintos cuadernos. Están agrupadas por funciones generales, extracción de estadísticas, normalización y funcionalidades del agente.

- **`imagenes/`**  
  Visualizaciones empleadas tanto en el desarrollo del documento escrito del trabajo como en la interfaz del agente.

- **`notebook/`**  
  Notebooks de desarrollo que muestran paso a paso las actividades del proyecto. Esta carpeta se divide en los siguientes archivos y subdirectorios:

  1. `Limpieza inicial.ipynb`: carga de datos originales y primera depuración.  
  2. `Extracción de métricas.ipynb`: cálculo de las métricas de rendimiento de jugadores.  
  3. `Cálculo del rating.ipynb`: elaboración del rating y de la normalización de las estadísticas.  
  4. `Limpieza previa al almacenamiento.ipynb`: limpieza de datos final antes de la carga en base de datos.  
  5. `Almacenamiento.ipynb`: exportación de los datos a PostgreSQL.  
  6. `Evaluación agente.ipynb`: pruebas funcionales del agente con consultas simuladas.  
     `graficos.ipynb`: creación de visualizaciones utilizadas en la interfaz y el documento.

  - **`intento_ratings/`**  
    Primeros experimentos realizados con modelos de regresión para estimar el rating de los jugadores.

  - **`modelos_de_agente/`**  
    Archivos auxiliares utilizados durante los primeros intentos de elaboración del agente inteligente.

  - **`notebook_auxiliares/`**  
    Cuadernos complementarios desarrollados durante el proyecto, sin relevancia directa en la versión final.

- **`style/`**  
  Contiene un archivo CSS para aplicar estilo a la interfaz construida con Streamlit.

---

### 📄 Archivos principales

- **`agente_sql.py`**  
  Lo respectivo al desarrollo del agente, incluyendo la función para lanzar la aplicación con Streamlit, que se ejecuta desde `main.py`.

- **`main.py`**  
  Archivo de ejecución del agente.
