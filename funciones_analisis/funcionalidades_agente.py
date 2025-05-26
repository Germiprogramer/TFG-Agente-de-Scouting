import streamlit as st
from mplsoccer import PyPizza
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
import os

# Conexión a PostgreSQL
engine = create_engine("postgresql+psycopg2://postgres@localhost:5432/scoutingdb")

# Consulta SQL para obtener perfil + estadísticas normalizadas
query_radar = text("""
    SELECT 
        p.player_name,
        p.main_position,
        p.team,
        CASE 
            WHEN p.rating ~ '^\\d+(\\.\\d+)?$' THEN ROUND(p.rating::numeric, 2)
            ELSE NULL
        END AS rating,
        ROUND((p.value_eur / 1000000.0)::numeric, 2) AS market_value,
        n.*
    FROM player_profile p
    LEFT JOIN normalized_stats_position n ON p.player_id = n.player_id
    WHERE p.player_name = :player_name
    LIMIT 1;
""")

# Configuración de radar por posición principal
radar_config = {
    "goalkeeper": (
        ["saves_per90", "save_percentage", "xg_against_minus_goals_conceded_per90",
         "keeper_sweeper_per90", "penalty_save_percentage", "aerial_dominance_index_per90",
         "pass_completion_rate"],
        ["Paradas /90", "Porcentaje paradas", "xG - Goles /90", "Sweeper /90", "Penaltis detenidos %",
         "Dominio aéreo", "Precisión pase %"]
    ),
    "center back": (
        ["tackles_successful_per90", "interceptions_per90", "clearances_per90",
         "blocks_per90", "times_dribbled_past_per90", "progressive_passes_per90",
         "duel_success_rate", "goals_scored_per90"],
        ["Tackles exitosos /90", "Intercepciones /90", "Despejes /90", "Bloqueos /90", "Regates sufridos /90",
         "Pases progresivos /90", "Duelos ganados %", "Goles /90"]
    ),
    "side back": (
        ["interception_success_rate", "pressures_per90", "duels_won_per90", "tackles_successful_per90",
         "progressive_carries_per90", "chances_created_per90", "goals_scored_per90", "fouls_committed_per90"],
        ["Intercepciones %", "Presiones /90", "Duelos ganados /90", "Tackles exitosos /90",
         "Conducciones progresivas /90", "Ocasiones creadas /90", "Goles /90", "Faltas cometidas /90"]
    ),
    "defensive midfield": (
        ["ball_recoveries_per90", "duels_won_per90", "duel_success_rate", "interceptions_per90",
         "pass_completion_rate", "progressive_passes_per90", "chances_created_per90", "fouls_committed_per90"],
        ["Recuperaciones /90", "Duelos ganados /90", "Duelos ganados %", "Intercepciones /90",
         "Precisión pase %", "Pases progresivos /90", "Ocasiones creadas /90", "Faltas cometidas /90"]
    ),
    "center midfield": (
        ["duels_won_per90", "pressures_per90", "dribble_success_rate", "pass_completion_rate",
         "progressive_passes_per90", "chances_created_per90", "goal_assists_per90", "goals_scored_per90"],
        ["Duelos ganados /90", "Presiones /90", "Éxito regate %", "Precisión pase %",
         "Pases progresivos /90", "Ocasiones creadas /90", "Asistencias /90", "Goles /90"]
    ),
    "offensive midfield": (
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

# Obtener datos del jugador
def get_player_data_for_radar(player_name):
    with engine.connect() as conn:
        df = pd.read_sql(query_radar, conn, params={"player_name": player_name})
    if df.empty:
        raise ValueError(f"No se encontró al jugador '{player_name}' en la base de datos.")
    return df.iloc[0]

# Dibujar el gráfico radar
def draw_radar_from_sql(player_name):
    row = get_player_data_for_radar(player_name)
    rol = row["main_position"]

    if rol not in radar_config:
        raise ValueError(f"No hay radar definido para la posición: {rol}")

    columnas, etiquetas = radar_config[rol]
    valores = [round(row[col], 2) if pd.notnull(row[col]) else 0 for col in columnas]

    slice_colors = ["#1A78CF"] * 3 + ["#D70232"] * 1 + ["#FF9300"] * 3 + ["#D70232"] * (len(valores) - 7)
    text_colors = ["#000000"] * len(valores)

    baker = PyPizza(
        params=etiquetas,
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

    fig.text(0.5, 0.97, f"{row['player_name']} - {row['team']}", size=18, weight='bold', ha='center')
    fig.text(0.5, 0.94, f"Market value: {row['market_value']} M€", size=12, weight='semibold', ha='center')
    fig.text(0.5125, 0.485, f"{row['rating']}", size=18, weight='bold', ha='center')

    st.pyplot(fig)

def log_consulta_txt(consulta, respuesta, archivo="agente_log.txt"):
    with open(archivo, "a", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}]\n")
        f.write("📝 Consulta:\n")
        f.write(consulta.strip() + "\n\n")
        f.write("✅ Respuesta:\n")
        f.write(respuesta.strip() + "\n\n")

