# TFG-Agente-de-Scouting

📂 Estructura del repositorio
El repositorio está organizado en diferentes carpetas, cada una con un propósito específico dentro del flujo de trabajo del proyecto. A continuación se describe la función de cada componente:

🔧 Carpetas principales
datos/
Contiene los archivos de entrada y resultados intermedios generados durante el proceso de análisis y construcción de la base de datos.

evaluacion_agente/
Incluye scripts y recursos utilizados para validar el rendimiento del agente, comparando los resultados obtenidos frente a respuestas esperadas.

funciones_analisis/
Módulo que agrupa las funciones personalizadas en Python encargadas de extraer estadísticas avanzadas a partir de los datos de eventos de partidos.

imagenes/
Recursos gráficos y visualizaciones utilizadas en el desarrollo del TFG o en la interfaz del agente.

notebook/
Contiene los notebooks que documentan paso a paso todo el proceso de desarrollo. Está dividido en tres subcarpetas:

intento_ratings/: primeros experimentos con modelos de regresión para calcular el rating de los jugadores.

modelos_de_agente/csv/: datos de ejemplo y archivos de apoyo usados para pruebas del agente.

notebook_auxiliares/: pipeline principal del proyecto, dividido en fases claramente identificadas:

1. Limpieza inicial.ipynb: carga de datos originales y depuración básica.

2. Extracción de métricas.ipynb: aplicación de funciones estadísticas para generar variables de rendimiento.

3. Cálculo del rating.ipynb: generación de la valoración final de cada jugador según su posición.

4. Limpieza previa al almacenamiento.ipynb: preparación final antes de migrar los datos a SQL.

5. Almacenamiento.ipynb: creación del esquema de base de datos y exportación a PostgreSQL.

6. Evaluación agente.ipynb: testeo del agente con un conjunto de consultas de prueba.

graficos.ipynb: generación de gráficos radar y visualizaciones de plantilla.

style/
Archivos de estilo (CSS) aplicados a la interfaz desarrollada en Streamlit.

🧠 Archivos principales
agente_sql.py
Script que define la lógica del agente inteligente basado en LangChain y su conexión con la base de datos SQL.

main.py
Punto de entrada de la aplicación Streamlit. Permite lanzar la interfaz de usuario para consultar al agente.
