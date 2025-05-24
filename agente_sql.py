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
engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5432/scouting_jugadores")

# Crear objeto SQLDatabase
sql_db = SQLDatabase(engine)

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
- Mostrar como respuesta final solo una tabla con las columnas `player_name`, `team`, `value_eur` y aquellas relacionadas con la pregunta (por ejemplo `goals_scored_per90` si se pregunta por goles).
"""


# --- CARGA DEL LLM Y AGENTE ---
@st.cache_resource
def cargar_agente():
    llm = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=300)
    agent = create_sql_agent(
    llm=llm,
    db=sql_db,
    verbose=False,
    agent_type="openai-functions",
    prefix=prefix
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
            except Exception as e:
                st.error(f"❌ Ha ocurrido un error: {e}")
    else:
        st.warning("⚠️ Introduce una consulta válida.")


