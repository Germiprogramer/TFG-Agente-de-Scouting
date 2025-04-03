
'''

#numero total de entradas
def tackles_exitosos_totales(df_eventos):
    """
    Devuelve el número total de entradas (tackles) exitosas (Won, Success In Play, Success Out).

    Retorna:
    - Entero: número total de tackles exitosos
    """
    df = df_eventos.copy()

    df['duel_type_name'] = df['duel_type'].apply(lambda x: x['name'] if isinstance(x, dict) else x)
    df['duel_outcome_name'] = df['duel_outcome'].apply(lambda x: x['name'] if isinstance(x, dict) else x)
    df = df.dropna(subset=['duel_type_name', 'duel_outcome_name'])

    df_tackle = df[df['duel_type_name'] == 'Tackle']

    if df_tackle.empty:
        return 0

    ganados = ['Won', 'Success In Play', 'Success Out']
    return df_tackle['duel_outcome_name'].isin(ganados).sum()

def porcentaje_intercepciones_exitosas(df_eventos):
    """
    Calcula el porcentaje de intercepciones exitosas (Won + Success In Play).

    Retorna:
    - Float: porcentaje de intercepciones exitosas
    """
    df = df_eventos.copy()
    df = df.dropna(subset=['interception_outcome'])

    df['interception_outcome'] = df['interception_outcome'].apply(lambda x: x['name'] if isinstance(x, dict) else x)

    exitosas = ['Won', 'Success In Play']
    total = len(df)
    
    if total == 0:
        return 0.0

    exitosas_count = df['interception_outcome'].isin(exitosas).sum()
    return round((exitosas_count / total) * 100, 2)

def intercepciones_exitosas_totales(df_eventos):
    """
    Devuelve el número total de intercepciones exitosas (Won + Success In Play).

    Retorna:
    - Entero: número de intercepciones exitosas
    """
    df = df_eventos.copy()
    df = df.dropna(subset=['interception_outcome'])

    df['interception_outcome'] = df['interception_outcome'].apply(lambda x: x['name'] if isinstance(x, dict) else x)

    exitosas = ['Won', 'Success In Play']
    return df['interception_outcome'].isin(exitosas).sum()

def numero_bloqueos(df):
    """Cuenta el número de eventos donde hay al menos un tipo de bloqueo (deflection, offensive, etc.)."""
    columnas_bloqueo = [
        'block_deflection',
        'block_offensive',
        'block_save_block',
        'block_counterpress'
    ]

    # Solo nos quedamos con las columnas que existen
    columnas_presentes = [col for col in columnas_bloqueo if col in df.columns]

    if not columnas_presentes:
        return 0

    # Creamos un DataFrame con solo las columnas de bloqueo
    bloqueos_df = df[columnas_presentes]

    # Contamos las filas que tienen al menos un True (es decir, un tipo de bloqueo)
    return bloqueos_df.any(axis=1).sum()

#despejes totales
def numero_clearances(df):
    """Cuenta el número total de despejes en el DataFrame."""
    columnas_clearance = [
        'clearance_aerial_won',
        'clearance_body_part',
        'clearance_head',
        'clearance_left_foot',
        'clearance_other',
        'clearance_right_foot'
    ]

    # Nos aseguramos de que la columna exista en el DataFrame
    columnas_presentes = [col for col in columnas_clearance if col in df.columns]

    if not columnas_presentes:
        return 0

    # Contamos filas donde al menos una de las columnas de clearance tenga dato
    return df[columnas_presentes].notna().any(axis=1).sum()

def duelos_aereos_ganados(df):
    """Número total de duelos aéreos ganados (vía despejes + tiros)."""
    despejes = df['clearance_aerial_won'].sum() if 'clearance_aerial_won' in df.columns else 0
    tiros = df['shot_aerial_won'].sum() if 'shot_aerial_won' in df.columns else 0
    return despejes + tiros

def porcentaje_duelos_aereos_ganados(df):
    """Porcentaje total de duelos aéreos ganados respecto al total (ganados + perdidos)."""
    ganados = duelos_aereos_ganados(df)
    perdidos = df['duel_type'].eq('Aerial Lost').sum() if 'duel_type' in df.columns else 0
    total = ganados + perdidos
    return 100 * ganados / total if total > 0 else 0

def tiros_cabeza_por_jugador(df_eventos, df_jugadores):
    """
    Añade al DataFrame de jugadores:
    - tiros_cabeza_totales
    - tiros_cabeza_en_duelo
    - porcentaje_tiros_cabeza_en_duelo

    Basado en:
    - 'shot_body_part' == 'Head'
    - 'shot_aerial_won' == True
    """
    df_jugadores = df_jugadores.copy()
    df = df_eventos.copy()

    # Inicializar columnas
    df_jugadores['tiros_cabeza_totales'] = 0
    df_jugadores['tiros_cabeza_en_duelo'] = 0
    df_jugadores['porcentaje_tiros_cabeza_en_duelo'] = 0.0

    for jugador in df_jugadores['player']:
        df_player = df[df['player'] == jugador]

        # Total de tiros de cabeza
        total = df_player[df_player['shot_body_part'] == 'Head'].shape[0]

        # Tiros de cabeza hechos en contexto de duelo aéreo
        en_duelo = df_player[
            (df_player['shot_body_part'] == 'Head') &
            (df_player['shot_aerial_won'] == True)
        ].shape[0]

        porcentaje = 100 * en_duelo / total if total > 0 else 0

        df_jugadores.loc[df_jugadores['player'] == jugador, 'tiros_cabeza_totales'] = total
        df_jugadores.loc[df_jugadores['player'] == jugador, 'tiros_cabeza_en_duelo'] = en_duelo
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_tiros_cabeza_en_duelo'] = round(porcentaje, 2)

    return df_jugadores
'''