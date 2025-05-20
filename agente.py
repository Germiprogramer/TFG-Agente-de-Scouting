
from langchain_experimental.utilities import PythonREPL
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents import create_csv_agent
import os
from dotenv import load_dotenv
from mplsoccer import PyPizza
import matplotlib.pyplot as plt
import pandas as pd
def pizza_radar_jugador(player_name, df_percentils, df_total):

    # Diccionario de etiquetas por rol
    etiquetas_posiciones = {
        "goalkeeper": ["Goalkeeper"],
        "center_back": ['Center Back', 'Right Center Back', 'Left Center Back'],
        "side_back": ['Left Back', 'Right Back', 'Right Wing Back', 'Left Wing Back'],
        "defensive_midfield": ['Right Defensive Midfield', 'Center Defensive Midfield', 'Left Defensive Midfield'],
        "center_midfield": ['Right Center Midfield', 'Center Midfield', 'Left Center Midfield'],
        "offensive_midfield": ['Left Attacking Midfield', 'Center Attacking Midfield', 'Right Attacking Midfield'],
        "winger": ['Left Wing', 'Left Midfield', 'Right Wing', 'Right Midfield'],
        "striker": ['Center Forward', 'Secondary Striker', 'Left Center Forward', 'Right Center Forward', "striker"]
    }

        # Mapear cada tipo de posición a columnas y etiquetas del radar
    radar_config = {
        "goalkeeper": (
            ["saves_per90", "save_percentage", "xg_against_minus_goals_conceded_per90",
            "keeper_sweeper_per90", "penalty_save_percentage", "aerial_dominance_index_per90",
             "pass_completion_rate"],
            ["Paradas /90", "Porcentaje paradas", "xG - Goles /90", "Sweeper /90", "Penaltis detenidos %",
            "Dominio aéreo", "Precisión pase %"]
        ),
        "center_back": (
            ["tackles_successful_per90", "interceptions_per90", "clearances_per90",
            "blocks_per90", "times_dribbled_past_per90", "progressive_passes_per90",
            "duel_success_rate", "goals_scored_per90"],
            ["Tackles exitosos /90", "Intercepciones /90", "Despejes /90", "Bloqueos /90", "Regates sufridos /90",
            "Pases progresivos /90", "Duelos ganados %", "Goles /90"]
        ),
        "side_back": (
            ["interception_success_rate", "pressures_per90", "duels_won_per90", "tackles_successful_per90",
            "progressive_carries_per90", "chances_created_per90", "goals_scored_per90", "fouls_committed_per90"],
            ["Intercepciones %", "Presiones /90", "Duelos ganados /90", "Tackles exitosos /90",
            "Conducciones progresivas /90", "Ocasiones creadas /90", "Goles /90", "Faltas cometidas /90"]
        ),
        "defensive_midfield": (
            ["ball_recoveries_per90", "duels_won_per90", "duel_success_rate", "interceptions_per90",
            "pass_completion_rate", "progressive_passes_per90", "chances_created_per90", "fouls_committed_per90"],
            ["Recuperaciones /90", "Duelos ganados /90", "Duelos ganados %", "Intercepciones /90",
            "Precisión pase %", "Pases progresivos /90", "Ocasiones creadas /90", "Faltas cometidas /90"]
        ),
        "center_midfield": (
            ["duels_won_per90", "pressures_per90", "dribble_success_rate", "pass_completion_rate",
            "progressive_passes_per90", "chances_created_per90", "goal_assists_per90", "goals_scored_per90"],
            ["Duelos ganados /90", "Presiones /90", "Éxito regate %", "Precisión pase %",
            "Pases progresivos /90", "Ocasiones creadas /90", "Asistencias /90", "Goles /90"]
        ),
        "offensive_midfield": (
            ["pass_completion_rate", "goal_assists_per90", "chances_created_per90", "dribbles_completed_per90",
            "dribble_success_rate", "progressive_passes_per90", "fouls_won_per90", "goals_scored_per90"],
            ["Precisión pase %", "Asistencias /90", "Ocasiones creadas /90", "Regates completados /90",
            "Éxito regate %", "Pases progresivos /90", "Faltas recibidas /90", "Goles /90"]
        ),
        "winger": (
            ["dribbles_completed_per90", "dribble_success_rate", "progressive_carries_per90", "chances_created_per90",
            "goal_assists_per90", "goals_scored_per90", "goals_minus_xg_per90", "fouls_won_per90"],
            ["Regates completados /90", "Éxito regate %", "Conducciones progresivas /90", "Ocasiones creadas /90",
            "Asistencias /90", "Goles /90", "Goles - xG /90", "Faltas recibidas /90"]
        ),
        "striker": (
            ["goals_scored_per90", "goals_minus_xg_per90", "headed_shot_duel_rate", "dribbles_completed_per90",
            "chances_created_per90", "goal_assists_per90", "pass_completion_rate", "fouls_won_per90"],
            ["Goles /90", "Goles - xG /90", "Duelos aéreos %", "Regates completados /90", "Ocasiones creadas /90",
            "Asistencias /90", "Precisión pase %", "Faltas recibidas /90"]
        )
    }

    # Obtener fila del jugador
    row = df_total[df_total["player_name"] == player_name].iloc[0]
    rol = row["main_position"]
    team = row["team"]
    rating = round(float(row["rating"]), 2) if str(row["rating"]).replace('.', '', 1).isdigit() else "S.V"
    market_value = row["value_eur"] / 1000000


    # Determinar rol del jugador
    if rol not in radar_config:
        raise ValueError(f"No se ha definido radar para la posición: {rol}")

    columnas, labels = radar_config[rol]

    # Extraer percentiles del DataFrame de percentiles
    valores = df_percentils[df_percentils["player_name"] == player_name][columnas].iloc[0].tolist()
    valores = [round(v, 2) for v in valores]

    # Colores
    slice_colors = ["#1A78CF"] * 3 + ["#FF9300"] * 3 + ["#D70232"] * (len(valores) - 6)
    text_colors = ["#F2F2F2"] * 3 + ["#000000"] * 3 + ["#F2F2F2"] * (len(valores) - 6)

    # Crear radar
    baker = PyPizza(
        params=labels,
        background_color="#EBEBE9",
        straight_line_color="#EBEBE9",
        straight_line_lw=1,
        last_circle_lw=0,
        other_circle_lw=0,
        inner_circle_size=20
    )

    fig, ax = baker.make_pizza(
        valores,
        figsize=(8, 8),
        color_blank_space="same",
        slice_colors=slice_colors,
        value_colors=text_colors,
        param_location=110
    )

    # Título y rating en el centro
    fig.text(0.5, 0.97, f"{player_name} - {team}", size=18, weight='bold', ha='center')
    fig.text(0.5, 0.94, f"Market value: {market_value} M€", size=12, weight='semibold', ha='center')
    fig.text(0.5125, 0.485, f"{rating}", size=18, weight='bold', ha='center')

    st.pyplot(fig)


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
