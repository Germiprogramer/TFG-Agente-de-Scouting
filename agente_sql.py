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

def load_css(path):
    with open(path, encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def cargar_agente():
    engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5432/scouting")
    sql_db = SQLDatabase(engine)

    def draw_radar_tool(player_name: str):
        draw_radar_from_sql(player_name)
        return ""

    tools = [
        Tool(
            name="generate_player_radar",
            func=draw_radar_tool,
            description="Generates a radar chart of player performance based on the player's exact name"
        )
    ]

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=1000)
    agent = create_sql_agent(
        llm=llm,
        db=sql_db,
        verbose=True,
        extra_tools=tools,
        agent_type="openai-functions",
        prefix=prefix2
    )
    return agent, engine

def lanzar_app():
    st.set_page_config(page_title="Football Scouting Agent", layout="wide")
    load_css("style/style.css")

    st.markdown("<h1 style='text-align: center;'>⚽ Intelligent Football Scouting Agent</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Ask questions, explore player data, and visualize performance with AI-powered radar charts.</p>", unsafe_allow_html=True)
    st.markdown("---")

    agent, engine = cargar_agente()

    tab_label = st.radio(
        "Navigation",
        ["📘 How to Use", "🧠 Ask the Agent", "🏆 Competitions & Squads"],
        horizontal=True
    )

    if tab_label == "📘 How to Use":
        st.header("🔍 What can you do?")
        st.markdown("""
        Use this app to explore player statistics from a football scouting database. Ask questions in natural language, and the agent will:
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
            - Use full player names (e.g. "Markel Susaeta Laskurain").
            - Try different positions like "striker", "winger", "center back".
            - Focus on per90 metrics for performance comparisons.
            """)
        st.image("imagenes/player_stats.png", caption="Available stats", use_container_width=True)

    elif tab_label == "🧠 Ask the Agent":
        st.header("💬 Ask Your Question")
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

    elif tab_label == "🏆 Competitions & Squads":
        st.header("🏟️ Explore Squads by Competition")

        with engine.connect() as conn:
            result = conn.execute(text("SELECT DISTINCT competition FROM teams ORDER BY competition"))
            competiciones = [row[0] for row in result if row[0] is not None]

        if competiciones:
            competicion_seleccionada = st.selectbox("Select a competition", competiciones)

            query_equipos = text("SELECT team_id, team FROM teams WHERE competition = :comp ORDER BY team")
            with engine.connect() as conn:
                equipos = pd.read_sql(query_equipos, conn, params={"comp": competicion_seleccionada})

            if not equipos.empty:
                equipo_seleccionado = st.selectbox("Select a team", equipos["team"])
                st.markdown(f"### 📋 Squad rating for **{equipo_seleccionado}**")
                try:
                    generar_grafico_equipo_streamlit(equipo_seleccionado, engine)
                except Exception as e:
                    st.error(f"❌ Could not generate squad graphic: {e}")
            else:
                st.warning("⚠️ No teams found for this competition.")
        else:
            st.warning("⚠️ No competitions available in the database.")