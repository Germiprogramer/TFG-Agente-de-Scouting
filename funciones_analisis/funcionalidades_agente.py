import streamlit as st
from mplsoccer import PyPizza
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
import os
from PIL import Image, ImageDraw, ImageFont
from matplotlib import font_manager
import io

# Conexión a PostgreSQL
engine = create_engine("postgresql+psycopg2://postgres@localhost:5432/scouting")

# RADAR DE JUGADORES
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
        s.minutes_played,
        n.*
    FROM player_profile p
    LEFT JOIN normalized_stats_position n ON p.player_id = n.player_id
    LEFT JOIN player_stats s ON p.player_id = s.player_id
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
prefix2 = """
You are an expert agent in football player analysis. You are only allowed to use the data available in the connected PostgreSQL database.

🗂️ By default, you should use the tables `player_profile`, `player_stats` to answer questions about players, as they contain the main performance metrics and individual characteristics.

Teams are stored in the `teams` table. The player-related tables only contain the `team_id` field to reference teams.

**You also have a function called generate_player_radar that you must always use to visualize a player's profile with a radar chart.**

**After answering any query involving one or more players, you must always select one player among the results — preferably the one with the best performance based on the query — and call generate_player_radar using their name.**

**This function should always be triggered, even if the user does not explicitly ask for a radar chart.**

When a query mentions metrics from different tables, you **must join those tables using `player_id`**. The following are the columns available in each table:

**You must not use any external knowledge.**
**You must not mention players who are not present in the database.**
**Do not fabricate information or values — respond only using real, existing data from the database.**

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

"Market value" means `value_eur`.

When asked about rating, you must only return **numeric ratings**. If the rating is a string value like `"S.V"`, it means the player is unrated and must be excluded.

When asked about the height in cm of a player, you must answer in base to the column height_cm.

Remember!
**You must not use any external knowledge.**
**You must not mention players who are not present in the database.**
**Do not fabricate information or values — respond only using real, existing data from the database.**

❌ You must not guess or invent data. If you cannot find relevant results in the database, you must return an empty table or say that no matching players were found.

"""
# GRÁFICO DE PLANTILLAS DE EQUIPO
# Cargar fuentes
dejavu_path = font_manager.findfont("DejaVu Sans")
dejavu_font = ImageFont.truetype(dejavu_path, 18)
dejavu_font_bold = ImageFont.truetype(dejavu_path, 22)

def generar_grafico_equipo_streamlit(equipo, engine):
    # Consulta SQL
    query = text("""
            SELECT pp.player_name, pp.main_position, pp.rating
            FROM player_profile pp
            JOIN teams t ON pp.team_id = t.team_id
            WHERE t.team = :team
        """)
    # Obtener datos desde SQL
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
    row_height = 40
    title_height = 60
    header_height = 40
    padding = 20

    max_players_top = max(len(grouped[pos]) for pos in top_row) if top_row else 0
    max_players_bottom = max(len(grouped[pos]) for pos in bottom_row) if bottom_row else 0

    width = padding * 2 + max(len(top_row), len(bottom_row)) * cell_width
    height = padding * 3 + title_height + (max_players_top + 1) * row_height + (max_players_bottom + 1) * row_height

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    font_small = dejavu_font
    font_header = dejavu_font_bold
    font_title = ImageFont.truetype(dejavu_path, 26)

    draw.text((padding, padding), f"{equipo} Squad Ratings", fill="black", font=font_title)

    color_map = {
        'goalkeeper': '#4F81BD',
        'center back': '#4BACC6',
        'side back': '#F79646',
        'center midfield': '#9BBB59',
        'defensive midfield': '#8064A2',
        'attacking midfield': '#C0504D',
        'striker': '#C00000',
        'winger': '#1F4E79'
    }

    def truncate_name(name, max_width):
        text_width = draw.textlength(name, font=font_small)
        if text_width <= max_width:
            return name
        parts = name.split(" ")
        truncated = ""
        for i in range(len(parts)):
            candidate = " ".join(parts[:len(parts)-i])
            if draw.textlength(candidate + "...", font=font_small) <= max_width:
                return candidate + "..."
        return name[:10] + "..."

    def draw_column(pos, col_index, row_offset):
        x0 = padding + col_index * cell_width
        y0 = padding + title_height + row_offset

        position_color = color_map.get(pos.lower(), "#D9D9D9")
        draw.rectangle([x0, y0, x0 + cell_width, y0 + header_height], fill=position_color)
        draw.text((x0 + 10, y0 + 10), pos.title(), fill="black", font=font_header)

        for i, (_, row) in enumerate(grouped[pos].iterrows()):
            y = y0 + header_height + i * row_height
            max_name_width = cell_width - 70
            name = truncate_name(row['player_name'], max_name_width)
            draw.text((x0 + 10, y), name, fill="black", font=font_small)
            draw.text((x0 + cell_width - 50, y), row['rating_display'], fill="black", font=font_small)

    for i, pos in enumerate(top_row):
        draw_column(pos, i, 0)

    for i, pos in enumerate(bottom_row):
        draw_column(pos, i, (max_players_top + 1) * row_height + padding)

    # Mostrar imagen en Streamlit sin guardar a disco
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    st.image(buffer.getvalue(), use_container_width=True)
    return buffer
