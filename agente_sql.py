from langchain.agents.agent_toolkits import create_sql_agent
from langchain.sql_database import SQLDatabase
from sqlalchemy import create_engine
from funciones_analisis.funcionalidades_agente import *
import streamlit as st
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
from mplsoccer import PyPizza
import pandas as pd

load_dotenv()

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Agente de Scouting", layout="centered")
st.title("⚽ Agente Inteligente de Jugadores")

# Crear motor SQLAlchemy
engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5432/scoutingdb")

# Crear objeto SQLDatabase
sql_db = SQLDatabase(engine)

# Agent behavior description
prefix2 = """
You are an expert agent in football player analysis. You are only allowed to use the data available in the connected PostgreSQL database.

🗂️ By default, you should use the tables `player_profile`, `player_stats`, and `player_stats_per90` to answer questions about players, as they contain the main performance metrics and individual characteristics.

Teams are stored in the `teams` table. The player-related tables only contain the `team_id` field to reference teams.

**You must not use any external knowledge.**
**You must not mention players who are not present in the database.**
Do not fabricate information or values — respond only using real, existing data.

You must filter the players position by the column `main_position`:
goalkeeper
side back
center back
defensive midfield
center midfield
offensive midfield
winger
striker

⚠️ You must not use any information that is not explicitly available in the database tables.

When you are asked a question:
- Query only the actual data from the database.
- As a final response, return only a table with the following columns: `player_name`, `team`, `value_eur`, and all other columns relevant to the question (e.g., `goals_scored_per90` if the question is about goals).
Make sure not to omit any column that is relevant to the query.

"Valor de mercado" means `value_eur`.

When asked about rating, you must only return **numeric ratings**. If the rating is a string value like `"S.V"`, it means the player is unrated and must be excluded.

When asked about the height in cm of a player, you must answer in base to the column height_cm.
"""


#Descripción del comportamiento del agente
prefix = """
Eres un agente experto en análisis de jugadores de fútbol. Solo puedes utilizar los datos que se encuentran en la base de datos PostgreSQL conectada.

🗂️ Por defecto, deberás utilizar las tablas `player_profile`, 'player_stats' y `player_stats_per90` para responder a preguntas sobre jugadores, ya que contienen la información principal de rendimiento y características individuales.ç

Los equipos aparecen en la tabla 'teams', apareciendo unicamente en las tablas de jugadores el "team_id".

**No debes usar conocimiento externo.**
**No debes mencionar a jugadores que no estén en la base de datos.**
No inventes información ni valores, y responde solo a partir de los datos reales existentes.

Guía de traducción para interpretar posiciones (columna main_position):
- portero → goalkeeper
- lateral → left back, right back
- defensa central → center back
- mediocentro defensivo → defensive midfield
- mediocentro → center midfield
- mediocentro ofensivo → offensive midfield
- extremo → winger
- delantero → striker

⚠️ No debes usar información que no esté contenida en las tablas de la base de datos.

Cuando te pregunten, debes:
- Consultar únicamente los datos reales de la base.
- Mostrar como respuesta final solo una tabla con las columnas `player_name`, `team`, `value_eur` y todas aquellas relacionadas con la pregunta (por ejemplo `goals_scored_per90` si se pregunta por goles).
No te dejes ninguna de las columnas relacionadas con la consulta.

Valor de mercado -> value_eur

Cuando se pregunta por rating, debes responder únicamente con ratings numéricos. Los ratings strings "S.V" son sin valorar.
"""


# --- CARGA DEL LLM Y AGENTE ---
@st.cache_resource
def cargar_agente():
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=250)
    agent = create_sql_agent(
    llm=llm,
    db=sql_db,
    verbose=False,
    agent_type="openai-functions",
    prefix=prefix2
)
    return agent

agent = cargar_agente()

# --- INTERFAZ ---
st.subheader("Hazle una pregunta al agente")

query = st.text_area("✍️ Escribe tu consulta relacionada con los jugadores", height=100)

if st.button("Responder"):
    if query.strip() != "":
        with st.spinner("💭 Pensando..."):
            try:
                respuesta = agent.run(query)
                st.success("✅ Consulta completada")
                st.markdown(respuesta)
                log_consulta_respuesta(query, respuesta)
            except Exception as e:
                st.error(f"❌ Ha ocurrido un error: {e}")
    else:
        st.warning("⚠️ Introduce una consulta válida.")

st.header("Radar de jugador")
player_input = st.text_input("Introduce el nombre exacto del jugador")
if player_input:
    try:
        draw_radar_from_sql(player_input)
    except Exception as e:
        st.error(str(e))
