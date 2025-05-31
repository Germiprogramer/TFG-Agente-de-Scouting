from langchain.agents.agent_toolkits import create_sql_agent
from langchain.sql_database import SQLDatabase
from sqlalchemy import create_engine
from funciones_analisis.funcionalidades_agente import *
import streamlit as st
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from mplsoccer import PyPizza
import pandas as pd
from langchain.tools import Tool

load_dotenv()

# --- INTERFAZ STREAMLIT---
st.set_page_config(page_title="Football Scouting Agent", layout="wide")

def load_css(path):
    with open(path) as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

#css_path = pathlib.Path("style/style.css")
#load_css(css_path)

# --- HEADER ---
st.markdown("<h1 style='text-align: center;'>⚽ Intelligent Football Scouting Agent</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Ask questions, explore player data, and visualize performance with AI-powered radar charts.</p>", unsafe_allow_html=True)
st.markdown("---")

# Crear motor SQLAlchemy
engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5432/scouting")

# Crear objeto SQLDatabase
sql_db = SQLDatabase(engine)

# Convertir funcion grafico en tool para el agente
def draw_radar_tool(player_name: str):
    return draw_radar_from_sql(player_name)

tools = [
    Tool(
        name="generate_player_radar",
        func=draw_radar_tool,
        description="Generates a radar chart of player performance based on the player's exact name"
    )
]


# --- CARGA DEL LLM Y AGENTE ---
@st.cache_resource
def cargar_agente():
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=1000)
    agent = create_sql_agent(
    llm=llm,
    db=sql_db,
    verbose=True,
    extra_tools=tools,
    agent_type="openai-functions",
    prefix=prefix2
)
    return agent

agent = cargar_agente()

st.markdown("""
Welcome to the **AI-powered Football Scouting Agent**!  
This tool helps you explore player performance data and visualize key metrics through radar charts.

### 🔍 What can you do here?
You can ask questions about football players' performance using natural language. The agent will query the database, return a summary table, and generate a radar chart for the top player.

### 🧾 Examples of queries you can try:
- "Show me the striker with the most goals per 90 minutes"
- "Who is the best left back in terms of duels won?"
- "Compare central midfielders with the best pass completion rates"
- "Give me the radar for Antoine Griezmann"
""", unsafe_allow_html=True)

# --- TABS ---
tab_info, tab_query, tab_squads = st.tabs(["📘 How to Use", "🧠 Ask the Agent", "🏆 Competitions & Squads"])

with tab_info:
    st.header("🔍 What can you do?")
    st.markdown("""
    You can use this app to explore player statistics from a football scouting database. Ask questions in natural language, and the agent will:
    
    - Query the database
    - Return a summary table with relevant players
    - Generate a **radar chart** for the top player

    **⚠️ Only players with more than 850 minutes played are eligible for radar charts.**
    """)

    st.header("📋 Example Queries")
    st.success('"Show me the striker with the most goals per 90 minutes"')
    st.success('"Who is the best left back in terms of duels won?"')
    st.success('"Give me the radar chart for Antoine Griezmann"')
    st.success('"Compare central midfielders with the best passing accuracy"')

    with st.expander("💡 Tips for better results"):
        st.markdown("""
        - Always use the full player name (e.g. "Markel Susaeta Laskurain")
        - Try different positions like "striker", "winger", "center back"
        - Focus on per90 metrics for performance comparisons
        """)

with tab_query:
    st.header("💬 Ask Your Question")
    st.markdown("Write a query about player performance below and press **Run Analysis**.")
    
    query = st.text_area("📝 Your question", placeholder="e.g. Show me the winger with the most dribbles completed per 90 minutes", height=120)
    
    if st.button("🚀 Run Analysis"):
            if query.strip():
                with st.spinner("🔎 Analyzing..."):
                    try:
                        response = agent.run(query)
                        st.success("✅ Done!")
                        st.markdown(response)
                        log_consulta_txt(query, response)
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            else:
                st.warning("Please enter a question before submitting.")

with tab_squads:
    st.header("🏟️ Explore Squads by Competition")

    # Paso 1: Obtener competiciones únicas
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT competition FROM teams ORDER BY competition"))
        competiciones = [row[0] for row in result if row[0] is not None]

    if competiciones:
        competicion_seleccionada = st.selectbox("Select a competition", competiciones)

        # Paso 2: Equipos dentro de la competición seleccionada
        query_equipos = text("SELECT team_id, team FROM teams WHERE competition = :comp ORDER BY team")
        with engine.connect() as conn:
            equipos = pd.read_sql(query_equipos, conn, params={"comp": competicion_seleccionada})

        if not equipos.empty:
            equipo_seleccionado = st.selectbox("Select a team", equipos["team"])

            # Puedes recuperar el team_id por si lo necesitas más adelante
            team_id = equipos.loc[equipos["team"] == equipo_seleccionado, "team_id"].values[0]

            # Mostrar el gráfico en Streamlit
            st.markdown(f"### 📋 Squad rating for **{equipo_seleccionado}**")
            try:
                generar_grafico_equipo_streamlit(equipo_seleccionado, engine)
            except Exception as e:
                st.error(f"❌ Could not generate squad graphic: {e}")
        else:
            st.warning("⚠️ No teams found for this competition.")
    else:
        st.warning("⚠️ No competitions available in the database.")
