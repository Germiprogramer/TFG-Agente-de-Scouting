import numpy as np
import pandas as pd

# Función para truncar a 2 decimales (sin redondear) y formatear como string con dos decimales
def truncar_y_formatear(x):
    return f"{np.floor(x * 100) / 100:.2f}"

def normalizar_metricas_percentiles(
    df, 
    metricas, 
    variables_extra, 
    posiciones_filtrar=None,
    min_minutos=850 #25% de una temporada
):
    """
    Normaliza métricas usando percentiles (0-100).
    
    Parámetros:
    - df: DataFrame original
    - metricas: lista de columnas a normalizar
    - variables_extra: lista de columnas a mantener sin cambios
    - posiciones_filtrar: None (no filtra) o lista de valores de 'main_position' a filtrar
    
    Devuelve:
    - DataFrame normalizado por percentiles
    """
        # Filtrar por minutos jugados
    if "minutes_played" in df.columns:
        df = df[df['minutes_played'] >= min_minutos]
    
    # Si se especifican posiciones, filtramos
    if posiciones_filtrar is not None:
        df = df[df['main_position'].isin(posiciones_filtrar)].copy()
    
    # Comprobamos qué métricas existen realmente en el DataFrame
    columnas_existentes = [col for col in metricas if col in df.columns]
    
    # Crear nuevo DataFrame con métricas y variables extra
    df_percentiles = df[variables_extra + columnas_existentes].copy()
    
    # Convertimos a numérico las columnas de métricas
    for col in columnas_existentes:
        df_percentiles[col] = pd.to_numeric(df_percentiles[col], errors='coerce')
    
    # Aplicar percentiles (0-100)
    for col in columnas_existentes:
        df_percentiles[col] = df_percentiles[col].rank(pct=True) * 100

    return df_percentiles

def normalizar_metricas_minmax(df, metricas, variables_extra, posiciones_filtrar=None, min_minutos= 850):
    """
    Normaliza métricas usando min-max scaling (0-100).

    Parámetros:
    - df: DataFrame original
    - metricas: lista de columnas a normalizar
    - variables_extra: lista de columnas a mantener sin cambios
    - posiciones_filtrar: None o lista de posiciones de 'main_position' a filtrar

    Devuelve:
    - DataFrame normalizado con valores entre 0 y 100
    """
        # Filtrar por minutos jugados
    if "minutes_played" in df.columns:
        df = df[df['minutes_played'] >= min_minutos]

    # Filtrado opcional
    if posiciones_filtrar is not None:
        df = df[df['main_position'].isin(posiciones_filtrar)].copy()
    
    # Seleccionar columnas existentes
    columnas_existentes = [col for col in metricas if col in df.columns]
    
    # Crear DataFrame nuevo
    df_minmax = df[variables_extra + columnas_existentes].copy()
    
    # Convertir métricas a numérico
    for col in columnas_existentes:
        df_minmax[col] = pd.to_numeric(df_minmax[col], errors='coerce')
    
    # Aplicar normalización min-max
    for col in columnas_existentes:
        col_values = df_minmax[col]
        min_val = col_values.min()
        max_val = col_values.max()
        if pd.notnull(min_val) and pd.notnull(max_val) and max_val != min_val:
            df_minmax[col] = (col_values - min_val) / (max_val - min_val) * 100
        else:
            df_minmax[col] = 0  # Para columnas constantes o vacías

    return df_minmax

def calcular_rating(df):
    """
    Calcula el rating ponderado de los jugadores según su posición principal ('main_position'),
    usando las ponderaciones definidas por el usuario.

    Parámetros:
    - df: DataFrame normalizado (min-max o percentiles)
    - tipo: 'minmax' o 'percentiles' (solo para referencia, no afecta al cálculo ahora)

    Devuelve:
    - DataFrame con una nueva columna 'rating'
    """

    # Ponderaciones actualizadas por "grupo" de posiciones (las tuyas)
    ponderaciones = {
        'goalkeeper': {
            'saves_per90': 0.075,
            'save_percentage': 0.25,
            'xg_against_minus_goals_conceded_per90': 0.425,
            'keeper_sweeper_per90': 0.075,
            'penalty_save_percentage': 0.05,
            'aerial_dominance_index_per90': 0.1,
            'pass_completion_rate': 0.75
        },
        'center_back': {
            'interceptions_per90': 0.15,
            'clearances_per90': 0.15,
            'blocks_per90': 0.10,
            'tackle_success_rate': 0.05,
            'duels_won_per90': 0.10,
            'duel_success_rate': 0.10,
            'interception_success_rate': 0.05,
            'times_dribbled_past_per90': 0.10,  # ¡Invertir!
            'passes_completed_per90': 0.025,
            'progressive_passes_per90': 0.075,
            'tackles_successful_per90': 0.05,
            'goals_scored_per90': 0.05
        },
        'side_back': {
            'pressures_per90': 0.15,
            'progressive_carries_per90': 0.15,
            'crosses_completed_per90': 0.1,
            'duels_won_per90': 0.10,
            'tackle_success_rate': 0.10,
            'interception_success_rate': 0.05,
            'tackles_successful_per90': 0.05,
            'fouls_committed_per90': 0.05,  # ¡Invertir!
            'goal_assists_per90': 0.05,
            'chances_created_per90': 0.1,
            'goals_scored_per90': 0.05
        },
        'defensive_midfield': {
            "pass_completion_rate" : 0.15,
            'ball_recoveries_per90': 0.125,
            'interceptions_per90': 0.125,
            'pressures_per90': 0.10,
            'duels_won_per90': 0.075,
            'duel_success_rate': 0.10,
            'progressive_passes_per90': 0.125,
            'fouls_committed_per90': 0.05,  # ¡Invertir!
            'chances_created_per90': 0.10,
            'goals_scored_per90': 0.05
        },
        'center_midfield': {
            "pass_completion_rate" : 0.10,
            'progressive_passes_per90': 0.20,
            'chances_created_per90': 0.125,
            'dribbles_completed_per90': 0.05,
            'dribble_success_rate': 0.10,
            'duels_won_per90': 0.10,
            'duel_success_rate': 0.10,
            'pressures_per90': 0.10,
            'goal_assists_per90': 0.05,
            'goals_scored_per90': 0.075
        },
        'offensive_midfield': {
            "pass_completion_rate" : 0.05,
            'goal_assists_per90': 0.175,
            'chances_created_per90': 0.175,
            'shots_total_per90': 0.05,
            'xg_total_per90': 0.05,
            'dribbles_completed_per90': 0.075,
            'dribble_success_rate': 0.075,
            'goals_scored_per90': 0.15,
            'fouls_won_per90': 0.05,
            'pressures_per90': 0.05,
            'progressive_passes_per90': 0.10,
        },
        'winger': {
            'dribbles_completed_per90': 0.10,
            'dribble_success_rate': 0.10,
            'progressive_carries_per90': 0.025,
            'crosses_completed_per90': 0.025,
            'chances_created_per90': 0.10,
            'goal_assists_per90': 0.15,
            'goals_scored_per90': 0.225,
            'goals_minus_xg_per90': 0.20,
            'progressive_carries_rate': 0.05,
            'ball_recoveries_per90': 0.025,
            'pressures_per90': 0.025,
            'fouls_won_per90': 0.025
        },
        'striker': {
            'xg_total_per90': 0.05,
            'goals_scored_per90': 0.20,
            'shot_accuracy': 0.05,
            'goals_minus_xg_per90': 0.20,
            'headed_shot_duel_rate': 0.05,
            'dribbles_completed': 0.05,
            'chances_created_per90': 0.075,
            'goal_assists_per90': 0.05,
            'fouls_won_per90': 0.05,
            'progressive_carries_per90': 0.075,
            'pass_completion_rate': 0.075,
            'ball_recoveries_per90': 0.05,
            'pressures_per90': 0.025
        }
    }

    # Definir mapeo de etiquetas
    etiquetas_posiciones = {
        "goalkeeper": ["Goalkeeper"],
        "center_back": ['Center Back', 'Right Center Back', 'Left Center Back'],
        "side_back": ['Left Back', 'Right Back', 'Right Wing Back', 'Left Wing Back'],
        "defensive_midfield": ['Right Defensive Midfield', 'Center Defensive Midfield', 'Left Defensive Midfield'],
        "center_midfield": ['Right Center Midfield', 'Center Midfield', 'Left Center Midfield'],
        "offensive_midfield": ['Left Attacking Midfield', 'Center Attacking Midfield', 'Right Attacking Midfield'],
        "winger": ['Left Wing', 'Left Midfield', 'Right Wing', 'Right Midfield'],
        "striker": ['Center Forward', 'Secondary Striker', 'Left Center Forward', 'Right Center Forward']
    }

    # Invertir el diccionario para encontrar la categoría desde la etiqueta
    etiqueta_a_categoria = {}
    for categoria, etiquetas in etiquetas_posiciones.items():
        for etiqueta in etiquetas:
            etiqueta_a_categoria[etiqueta] = categoria

    # Calcular ratings
    df = df.copy()
    ratings = []

    for idx, row in df.iterrows():
        main_position = row['main_position']
        rating = 0

        if main_position in etiqueta_a_categoria:
            categoria = etiqueta_a_categoria[main_position]
            if categoria in ponderaciones:
                for stat, peso in ponderaciones[categoria].items():
                    if stat in row:
                        valor = row[stat]
                        # Invertimos métricas "negativas"
                        if stat in ['times_dribbled_past_per90', 'fouls_committed_per90']:
                            valor = 100 - valor
                        rating += valor * peso
        ratings.append(rating)

    df['rating'] = ratings
    return df

def imprimir_estadisticas_rating(df, nombre_variable):
    maximo = round(df['rating'].max(), 2)
    minimo = round(df['rating'].min(), 2)
    media = round(df['rating'].mean(), 2)
    mediana = round(df['rating'].median(), 2)
    
    print(f"Dataset: {nombre_variable}")
    print(f"  Máximo: {maximo}")
    print(f"  Mínimo: {minimo}")
    print(f"  Media: {media}")
    print(f"  Mediana: {mediana}")
    print("")

def escalar_con_clipping_superior(df, col='rating', mediana_destino=60, escala=10, maximo=100):
    """
    Escala robusta centrada en la mediana, usando IQR para controlar dispersión.
    Solo aplica clipping superior para evitar que los valores altos distorsionen la escala.
    """
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    mediana = df[col].median()

    if iqr == 0:
        df[col + '_normalizado'] = mediana_destino
    else:
        normalizado = ((df[col] - mediana) / iqr) * escala + mediana_destino
        df[col + '_normalizado'] = normalizado.clip(upper=maximo)

    return df

def imprimir_estadisticas_rating_normalizado(df, nombre_variable):
    """
    Imprime las estadísticas básicas del rating normalizado de un DataFrame.
    """
    maximo = round(df['rating_normalizado'].max(), 2)
    minimo = round(df['rating_normalizado'].min(), 2)
    media = round(df['rating_normalizado'].mean(), 2)
    mediana = round(df['rating_normalizado'].median(), 2)

    print(f"Dataset: {nombre_variable}")
    print(f"  Máximo: {maximo}")
    print(f"  Mínimo: {minimo}")
    print(f"  Media: {media}")
    print(f"  Mediana: {mediana}")
    print("")

def contar_sin_valorar(df, columna='rating'):
    """
    Cuenta cuántos jugadores tienen el valor 'S.V' (Sin Valorar) en la columna indicada.
    """
    return (df[columna] == "S.V").sum()