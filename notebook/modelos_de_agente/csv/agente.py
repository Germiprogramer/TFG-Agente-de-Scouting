import sys
import os

# Ruta al directorio raíz del proyecto (ajústala si es necesario)
ruta_raiz = os.path.abspath(r"C:\Users\Germán Llorente\Desktop\germiprogramer\TFG-Agente-de-Scouting")

if ruta_raiz not in sys.path:
    sys.path.append(ruta_raiz)

import importlib
import funciones_analisis.funcionalidades_agente

importlib.reload(funciones_analisis.funcionalidades_agente)

from funciones_analisis.funcionalidades_agente import *
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents import create_csv_agent
import os
from dotenv import load_dotenv
from mplsoccer import PyPizza
import pandas as pd

load_dotenv()

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Agente de Scouting", layout="centered")
st.title("⚽ Agente Inteligente de Jugadores")

# --- CARGA DE ARCHIVO CSV ---
csv_file = "datos/datos_jugadores_v4/jugadores_total.csv"

df_total = pd.read_csv("datos/datos_jugadores_v4/jugadores_total.csv")
df_mezcla = pd.read_csv("datos/normalizaciones_posicion/mezcla/mezcla_total.csv")

# --- DEFINICIÓN DEL PREFIX PERSONALIZADO ---
prefix = """
Eres un agente experto en análisis de jugadores de fútbol. Solo puedes usar el DataFrame `df` que contiene columnas como 'player_name', 'team', 'value_eur', 'goals_per90', etc.

**Solo puedes utilizar los datos que están dentro de ese DataFrame.**
**No debes usar conocimiento externo.**
No debes mencionar a jugadores que no estén en el DataFrame.

Guía de traducción para interpretar posiciones (columna main_position):
- portero → goalkeeper
- lateral → left back, right back
- defensa central → center back
- mediocentro defensivo → defensive midfield
- mediocentro → center midfield
- mediocentro ofensivo → offensive midfield
- extremo → winger
- delantero → striker

⚠️ No debes usar información externa, solo el DataFrame.

Cuando te pregunten, debes:
- Mostrar como respuesta final solo una tabla con las columnas `player_name`, `team`, `value_eur` y aquellas relacionadas con la pregunta (por ejemplo `goals_per90` si se pregunta por goles).
"""

# --- CARGA DEL LLM Y AGENTE ---
@st.cache_resource
def cargar_agente():
    llm = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=300)
    agent = create_csv_agent(
        llm,
        csv_file,
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

st.header("Radar de jugador")
player_input = st.text_input("Introduce el nombre exacto del jugador")
if player_input:
    try:
        pizza_radar_jugador(player_input, df_percentils=df_mezcla, df_total=df_total)
    except Exception as e:
        st.error(str(e))
