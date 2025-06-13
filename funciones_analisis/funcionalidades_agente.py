import streamlit as st
from mplsoccer import PyPizza
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
import os
from PIL import Image, ImageDraw, ImageFont
from matplotlib import font_manager
import io
from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np


# Conexión a PostgreSQL
engine = create_engine("postgresql+psycopg2://postgres@localhost:5432/players_db")

# RADAR DE JUGADORES
# Consulta SQL para obtener perfil + estadísticas normalizadas
query_radar = text("""
    SELECT 
        p.player_name,
        t.team AS team,
        p.main_position,
        s.minutes_played,
        CASE 
            WHEN p.rating ~ '^\\d+(\\.\\d+)?$' THEN ROUND(p.rating::numeric, 2)
            ELSE NULL
        END AS rating,
        ROUND((p.value_eur / 1000000.0)::numeric, 2) AS market_value,
        n.*
    FROM player_profile p
    LEFT JOIN teams t ON p.team_id = t.team_id
    LEFT JOIN player_stats s ON p.player_id = s.player_id
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
        ["Saves /90", "Save %", "xG - Goals /90", "Sweeper /90", "Penalties Saved %",
         "Aerial Dominance", "Pass Accuracy %"]
    ),
    "center back": (
        ["tackles_successful_per90", "interceptions_per90", "clearances_per90",
         "blocks_per90", "times_dribbled_past_per90", "progressive_passes_per90",
         "duel_success_rate", "goals_scored_per90"],
        ["Successful Tackles /90", "Interceptions /90", "Clearances /90", "Blocks /90", "Dribbled Past /90",
         "Progressive Passes /90", "Duels Won %", "Goals /90"]
    ),
    "side back": (
        ["interception_success_rate", "pressures_per90", "duels_won_per90", "tackles_successful_per90",
         "progressive_carries_per90", "chances_created_per90", "goals_scored_per90", "fouls_committed_per90"],
        ["Interception %", "Pressures /90", "Duels Won /90", "Successful Tackles /90",
         "Progressive Carries /90", "Chances Created /90", "Goals /90", "Fouls Committed /90"]
    ),
    "defensive midfield": (
        ["ball_recoveries_per90", "duels_won_per90", "duel_success_rate", "interceptions_per90",
         "pass_completion_rate", "progressive_passes_per90", "chances_created_per90", "fouls_committed_per90"],
        ["Recoveries /90", "Duels Won /90", "Duels Won %", "Interceptions /90",
         "Pass Accuracy %", "Progressive Passes /90", "Chances Created /90", "Fouls Committed /90"]
    ),
    "center midfield": (
        ["duels_won_per90", "pressures_per90", "dribble_success_rate", "pass_completion_rate",
         "progressive_passes_per90", "chances_created_per90", "goal_assists_per90", "goals_scored_per90"],
        ["Duels Won /90", "Pressures /90", "Dribble Success %", "Pass Accuracy %",
         "Progressive Passes /90", "Chances Created /90", "Assists /90", "Goals /90"]
    ),
    "offensive midfield": (
        ["pass_completion_rate", "goal_assists_per90", "chances_created_per90", "dribbles_completed_per90",
         "dribble_success_rate", "progressive_passes_per90", "fouls_won_per90", "goals_scored_per90"],
        ["Pass Accuracy %", "Assists /90", "Chances Created /90", "Completed Dribbles /90",
         "Dribble Success %", "Progressive Passes /90", "Fouls Won /90", "Goals /90"]
    ),
    "winger": (
        ["dribbles_completed_per90", "dribble_success_rate", "progressive_carries_per90", "chances_created_per90",
         "goal_assists_per90", "goals_scored_per90", "goals_minus_xg_per90", "fouls_won_per90"],
        ["Completed Dribbles /90", "Dribble Success %", "Progressive Carries /90", "Chances Created /90",
         "Assists /90", "Goals /90", "Goals - xG /90", "Fouls Won /90"]
    ),
    "striker": (
        ["goals_scored_per90", "goals_minus_xg_per90", "headed_shot_duel_rate", "dribbles_completed_per90",
         "chances_created_per90", "goal_assists_per90", "pass_completion_rate", "fouls_won_per90"],
        ["Goals /90", "Goals - xG /90", "Headed Duel %", "Completed Dribbles /90", "Chances Created /90",
         "Assists /90", "Pass Accuracy %", "Fouls Won /90"]
    )
}

# Obtener datos del jugador
def get_player_data_for_radar(player_name):
    with engine.connect() as conn:
        df = pd.read_sql(query_radar, conn, params={"player_name": player_name})
        df = df.loc[:, ~df.columns.duplicated()]
    if df.empty:
        raise ValueError(f"No se encontró al jugador '{player_name}' en la base de datos.")
    return df.iloc[0]

def draw_radar_from_sql(player_name):
    try:
        row = get_player_data_for_radar(player_name)
    except ValueError as e:
        st.warning(str(e))
        return

    # Verificar minutos jugados
    if pd.isnull(row["minutes_played"]):
        st.warning(f"⏱️ No data available for minutes played for {player_name}.")
        return
    elif row["minutes_played"] < 850:
        st.warning(f"⚠️ {player_name} has only played {int(row['minutes_played'])} minutes, which is below the 850-minute threshold required for a reliable evaluation.")
        return

    rol = row["main_position"]
    if rol not in radar_config:
        st.warning(f"⚠️ No radar configuration available for position: {rol}")
        return

    columnas, etiquetas = radar_config[rol]
    valores = [round(row[col], 2) if pd.notnull(row[col]) else 0 for col in columnas]

    slice_colors = ["#1A78CF"] * 3 + ["#D70232"] * 1 + ["#FF9300"] * 3 + ["#D70232"] * (len(valores) - 7)
    text_colors = ["#000000"] * len(valores)

    baker = PyPizza(
        params=etiquetas,
        background_color="#f5f9ff",
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
    
    #plt.show() 
    
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150)


    #Crear columnas vacías a los lados para centrar
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        st.image(buf, use_container_width=False, width=700)  # ajusta el ancho aquí


# ARCHIVO PARA GUARDAR LAS COSULTAS
def log_consulta_txt(consulta, respuesta, archivo="agente_log.txt"):
    with open(archivo, "a", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}]\n")
        f.write("📝 Consulta:\n")
        f.write(consulta.strip() + "\n\n")
        f.write("✅ Respuesta:\n")
        f.write(respuesta.strip() + "\n\n")


# Descripción del comportamiento del agente
prefix = """
🧠 You are an **expert agent in football player analysis**. You are ONLY allowed to use the data available in the **connected PostgreSQL database**.

📊 By default, you must ALWAYS use the tables `player_profile` and `player_stats` to answer questions about players. The table `player_profile` contains the **individual characteristics** and `player_stats` contains the **main performance metrics**.

🏟️ The table `teams` contains team-level information. Player-related tables only include the `team_id` column, which you must use to JOIN with `teams`.

⚠️ CRITICAL: The column containing the team name is `team` (NOT `team_name`) and is located in the `teams` table.  
🔁 ALWAYS refer to it as `t.team` when using SQL aliases.

📈 You have access to a special function: `generate_player_radar`  
✅ You MUST call this function **after any query that involves one or more players**, even if the user doesn’t explicitly ask for it.  
👉 Select **the best performing player** from the result and run: `generate_player_radar("player_name")`

📝 Then, you MUST display the **written information** (in table format) of **ALL the players** included in the result — not just the selected one for the radar.  
⚠️ The full player data must always be shown **after** the radar chart is generated.

🧩 If a query includes metrics from different tables, you **MUST** join them using `player_id`.

────────────────────────────
🔒 STRICT RULES (DO NOT BREAK):
────────────────────────────

🚫 DO NOT use any external knowledge.  
🚫 DO NOT mention players who are NOT in the database.  
🚫 DO NOT fabricate information or statistics.  
✅ ONLY respond using **real, existing data**.  
📭 If no results are found, return an **empty table** or a clear explanation.  
🚫 DO NOT make any comments about the radar generation, just generate it.  
✅ ALWAYS include the **complete written information of all players returned** by the query in a table format, and place it AFTER the radar.
🚫 DO NOT return players whose `rating` is `'N.R'` — only include players with a **numerical rating**.

────────────────────────────
📌 POSITION FILTERING:
────────────────────────────
Filter players using the column `main_position`, with possible values:  
`goalkeeper`, `side back`, `center back`, `defensive midfield`, `center midfield`, `offensive midfield`, `winger`, `striker`.

────────────────────────────
📋 RESPONSE FORMAT:
────────────────────────────
Your FINAL answer must:
1. First, call `generate_player_radar("player_name")`
2. Then, write the table and explanation with:
   - `player_name`  
   - `team`  
   - `value_eur`  
   - Any other **relevant columns** based on the question (e.g., `goals_scored_per90`, `height_cm`, etc.)

────────────────────────────
📌 EXAMPLE (RADAR FIRST, THEN TEXT):
────────────────────────────
User asks:  
"Find 4 attacking midfielders under 24 years old with the highest number of key passes per 90 minutes (min. 850 minutes played)."

First you generate the radar of the selected player.

✅ Then, your textual response must look like this:

Here are 4 attacking midfielders under 24 years old with the highest number of key passes per 90 minutes:

player_name	team	value_eur	key_passes_per90
Hiroshi Kiyotake	Hannover 96	550000.0	2.43
Nadiem Amiri	Hoffenheim	650000.0	1.87
Riccardo Saponara	Empoli	4600000.0	1.85
Marco Asensio Willemsen	Espanyol	6500000.0	1.66

────────────────────────────
📌 FINAL INSTRUCTIONS:
────────────────────────────

The radar chart MUST appear first.

The full explanation and player table MUST follow the radar.

NEVER omit the textual response, even if the radar is displayed.

🔁 REMEMBER: Be accurate. Do NOT guess. ALWAYS base your answer on the actual database schema and contents.
"""


# GRÁFICO DE PLANTILLAS DE EQUIPO

# Cargar fuentes
dejavu_path = font_manager.findfont("DejaVu Sans")
dejavu_font = ImageFont.truetype(dejavu_path, 18)
dejavu_font_bold = ImageFont.truetype(dejavu_path, 22)
font_title = ImageFont.truetype(dejavu_path, 26)

def generar_grafico_equipo_streamlit(equipo, engine):
    # Consulta SQL
    query = text("""
            SELECT pp.player_name, pp.main_position, pp.rating
            FROM player_profile pp
            JOIN teams t ON pp.team_id = t.team_id
            WHERE t.team = :team
        """)
    with engine.connect() as conn:
        df_equipo = pd.read_sql(query, conn, params={"team": equipo})

    if df_equipo.empty:
        st.warning(f"No data found for team '{equipo}'")
        return

    df_equipo['rating'] = pd.to_numeric(df_equipo['rating'], errors='coerce')
    df_equipo['rating_display'] = df_equipo['rating'].round(0).astype('Int64').astype(str)
    df_equipo.loc[df_equipo['rating'].isna(), 'rating_display'] = 'N.R'

    grouped = dict(sorted(df_equipo.groupby('main_position')))
    positions = list(grouped.keys())
    top_row = positions[:len(positions)//2]
    bottom_row = positions[len(positions)//2:]

    cell_width = 260
    line_height = 22
    player_spacing = 10
    title_height = 60
    header_height = 40
    padding = 20

    def wrap_text(text, font, max_width, draw):
        lines = []
        words = text.split()
        current_line = ""
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if draw.textlength(test_line, font=font) <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    def compute_column_height(group, draw, font, max_width):
        height = header_height
        for _, row in group.iterrows():
            lines = wrap_text(row['player_name'], font, max_width, draw)
            height += line_height * len(lines) + player_spacing
        return height

    draw_test = ImageDraw.Draw(Image.new("RGB", (1,1)))
    max_players_top = max([compute_column_height(grouped[pos], draw_test, dejavu_font, cell_width - 70) for pos in top_row]) if top_row else 0
    max_players_bottom = max([compute_column_height(grouped[pos], draw_test, dejavu_font, cell_width - 70) for pos in bottom_row]) if bottom_row else 0

    width = padding * 2 + max(len(top_row), len(bottom_row)) * cell_width
    height = padding * 3 + title_height + max_players_top + max_players_bottom

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    draw.text((padding, padding), f"{equipo} Squad Ratings", fill="black", font=font_title)

    color_map = {
        'goalkeeper': '#4F81BD',
        'center back': '#4BACC6',
        'side back': '#F79646',
        'center midfield': '#9BBB59',
        'defensive midfield': '#8064A2',
        'attacking midfield': '#C0504D',
        'striker': '#C00000',
        'winger': '#1F4E79',
        'offensive midfield': '#D9D9D9'
    }

    def draw_column(pos, col_index, row_offset):
        x0 = padding + col_index * cell_width
        y = padding + title_height + row_offset

        position_color = color_map.get(pos.lower(), "#D9D9D9")
        draw.rectangle([x0, y, x0 + cell_width, y + header_height], fill=position_color)
        draw.text((x0 + 10, y + 10), pos.title(), fill="black", font=dejavu_font_bold)
        y += header_height

        for _, row in grouped[pos].iterrows():
            name_lines = wrap_text(row['player_name'], dejavu_font, cell_width - 70, draw)
            for j, line in enumerate(name_lines):
                draw.text((x0 + 10, y + j * line_height), line, fill="black", font=dejavu_font)
            draw.text((x0 + cell_width - 50, y), row['rating_display'], fill="black", font=dejavu_font)
            y += line_height * len(name_lines) + player_spacing

    for i, pos in enumerate(top_row):
        draw_column(pos, i, 0)

    for i, pos in enumerate(bottom_row):
        draw_column(pos, i, max_players_top + padding)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    st.image(buffer.getvalue(), use_container_width=True)
    return buffer