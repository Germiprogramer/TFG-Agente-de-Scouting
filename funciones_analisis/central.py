#porcentaje de entradas exitosas
def porcentaje_tackles_exitosos(df_eventos):
    """
    Devuelve el porcentaje total de tackles exitosos (ganados) sobre el total de tackles realizados.
    
    Retorna:
    - Porcentaje de tackles ganados (float, entre 0 y 100)
    """
    df = df_eventos.copy()

    # Extraer tipo y resultado
    df['duel_type_name'] = df['duel_type'].apply(lambda x: x['name'] if isinstance(x, dict) else x)
    df['duel_outcome_name'] = df['duel_outcome'].apply(lambda x: x['name'] if isinstance(x, dict) else x)
    df = df.dropna(subset=['duel_type_name', 'duel_outcome_name'])

    # Filtrar tackles
    df_tackle = df[df['duel_type_name'] == 'Tackle']

    if df_tackle.empty:
        return 0.0  # evitar división por cero

    # Clasificar resultado
    ganados = ['Won', 'Success In Play', 'Success Out']
    exitosos = df_tackle['duel_outcome_name'].isin(ganados).sum()
    total = len(df_tackle)

    return round((exitosos / total) * 100, 2)

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

#bloqueos
def bloqueos_totales(df):
    """Devuelve el número total de eventos de tipo bloqueo."""
    return df['block_deflection'].notna().sum()

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

def pases_progresivos(jugador):
    pass

def pases_largos(jugador):
    pass

def acciones_defensivas(jugador):
    pass

def recuperaciones(jugador):
    pass

def goles(jugador):
    pass
