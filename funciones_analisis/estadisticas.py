def porcentaje_tackles_exitosos_por_jugador(df_eventos, df_jugadores):
    """
    Añade una columna 'porcentaje_tackles_exitosos' al DataFrame de jugadores.
    Calcula el % de tackles exitosos (ganados) por cada jugador.
    
    Retorna:
    - DataFrame df_jugadores con la nueva columna añadida
    """
    df_jugadores = df_jugadores.copy()
    df = df_eventos.copy()

    # Inicializar la nueva columna con 0.0
    df_jugadores['porcentaje_tackles_exitosos'] = 0.0

    for jugador in df_jugadores['player']:
        df_player = df[df['player'] == jugador]

        # Extraer tipo y resultado de los duelos
        df_player['duel_type_name'] = df_player['duel_type'].apply(lambda x: x['name'] if isinstance(x, dict) else x)
        df_player['duel_outcome_name'] = df_player['duel_outcome'].apply(lambda x: x['name'] if isinstance(x, dict) else x)
        df_player = df_player.dropna(subset=['duel_type_name', 'duel_outcome_name'])

        # Filtrar tackles
        df_tackle = df_player[df_player['duel_type_name'] == 'Tackle']

        if df_tackle.empty:
            continue  # seguir con el siguiente jugador si no hay tackles

        # Clasificar tackles exitosos
        ganados = ['Won', 'Success In Play', 'Success Out']
        exitosos = df_tackle['duel_outcome_name'].isin(ganados).sum()
        total = len(df_tackle)
        porcentaje = round((exitosos / total) * 100, 2) if total > 0 else 0.0

        # Asignar el valor al jugador correspondiente
        df_jugadores.loc[df_jugadores["player"] == jugador, "porcentaje_tackles_exitosos"] = porcentaje

    return df_jugadores

def tackles_exitosos_totales_por_jugador(df_eventos, df_jugadores):
    """
    Añade una columna 'tackles_exitosos_totales' al DataFrame de jugadores.
    Calcula el número de tackles exitosos por jugador (Won, Success In Play, Success Out).

    Retorna:
    - df_jugadores con columna nueva añadida
    """
    df_jugadores = df_jugadores.copy()
    df = df_eventos.copy()

    # Inicializar columna con ceros
    df_jugadores['tackles_exitosos_totales'] = 0

    for jugador in df_jugadores['player']:
        df_player = df[df['player'] == jugador]

        # Extraer tipo y resultado
        df_player['duel_type_name'] = df_player['duel_type'].apply(lambda x: x['name'] if isinstance(x, dict) else x)
        df_player['duel_outcome_name'] = df_player['duel_outcome'].apply(lambda x: x['name'] if isinstance(x, dict) else x)
        df_player = df_player.dropna(subset=['duel_type_name', 'duel_outcome_name'])

        # Filtrar tackles
        df_tackle = df_player[df_player['duel_type_name'] == 'Tackle']

        if df_tackle.empty:
            continue

        # Clasificar tackles exitosos
        ganados = ['Won', 'Success In Play', 'Success Out']
        exitosos = df_tackle['duel_outcome_name'].isin(ganados).sum()

        # Asignar al DataFrame de jugadores
        df_jugadores.loc[df_jugadores['player'] == jugador, 'tackles_exitosos_totales'] = exitosos

    return df_jugadores

def porcentaje_intercepciones_exitosas_por_jugador(df_eventos, df_jugadores):
    """
    Añade una columna 'porcentaje_intercepciones_exitosas' al DataFrame de jugadores.
    Calcula el % de intercepciones exitosas por jugador (Won, Success In Play).

    Retorna:
    - df_jugadores con columna nueva añadida
    """
    df_jugadores = df_jugadores.copy()
    df = df_eventos.copy()

    # Inicializar columna
    df_jugadores['porcentaje_intercepciones_exitosas'] = 0.0

    for jugador in df_jugadores['player']:
        df_player = df[df['player'] == jugador]

        # Limpiar columna de intercepciones
        df_player = df_player.dropna(subset=['interception_outcome'])
        if df_player.empty:
            continue

        df_player['interception_outcome'] = df_player['interception_outcome'].apply(
            lambda x: x['name'] if isinstance(x, dict) else x
        )

        total = len(df_player)
        exitosas = ['Won', 'Success In Play']
        exitosas_count = df_player['interception_outcome'].isin(exitosas).sum()
        porcentaje = round((exitosas_count / total) * 100, 2) if total > 0 else 0.0

        # Asignar al DataFrame de jugadores
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_intercepciones_exitosas'] = porcentaje

    return df_jugadores

def intercepciones_exitosas_totales_por_jugador(df_eventos, df_jugadores):
    """
    Añade una columna 'intercepciones_exitosas_totales' al DataFrame de jugadores.
    Calcula el número de intercepciones exitosas (Won + Success In Play) por jugador.

    Retorna:
    - df_jugadores con la nueva columna añadida
    """
    df_jugadores = df_jugadores.copy()
    df = df_eventos.copy()

    # Inicializar columna
    df_jugadores['intercepciones_exitosas_totales'] = 0

    for jugador in df_jugadores['player']:
        df_player = df[df['player'] == jugador]

        # Limpiar y transformar columna
        df_player = df_player.dropna(subset=['interception_outcome'])
        if df_player.empty:
            continue

        df_player['interception_outcome'] = df_player['interception_outcome'].apply(
            lambda x: x['name'] if isinstance(x, dict) else x
        )

        exitosas = ['Won', 'Success In Play']
        total_exitosas = df_player['interception_outcome'].isin(exitosas).sum()

        # Asignar al jugador
        df_jugadores.loc[df_jugadores['player'] == jugador, 'intercepciones_exitosas_totales'] = total_exitosas

    return df_jugadores

def despejes_totales_por_jugador(df_eventos, df_jugadores):
    """
    Añade una columna 'despejes_totales' al DataFrame de jugadores.
    Cuenta cuántos eventos de tipo 'Clearance' tiene cada jugador.

    Retorna:
    - df_jugadores con columna 'despejes_totales' añadida.
    """
    df_jugadores = df_jugadores.copy()
    df = df_eventos.copy()

    df_jugadores['despejes_totales'] = 0

    for jugador in df_jugadores['player']:
        df_player = df[(df['player'] == jugador) & (df['type'] == 'Clearance')]
        total_despejes = len(df_player)

        df_jugadores.loc[df_jugadores['player'] == jugador, 'despejes_totales'] = total_despejes

    return df_jugadores

def bloqueos_totales_por_jugador(df_eventos, df_jugadores):
    """
    Añade una columna 'bloqueos_totales' al DataFrame de jugadores.
    Cuenta cuántos eventos de tipo 'Block' tiene cada jugador.

    Retorna:
    - df_jugadores con columna 'bloqueos_totales' añadida.
    """
    df_jugadores = df_jugadores.copy()
    df = df_eventos.copy()

    df_jugadores['bloqueos_totales'] = 0

    for jugador in df_jugadores['player']:
        df_player = df[(df['player'] == jugador) & (df['type'] == 'Block')]
        total_bloqueos = len(df_player)

        df_jugadores.loc[df_jugadores['player'] == jugador, 'bloqueos_totales'] = total_bloqueos

    return df_jugadores

def despejes_cabeza_por_jugador(df_eventos, df_jugadores):
    """
    Añade al DataFrame de jugadores:
    - despejes_cabeza_totales
    - despejes_cabeza_ganados
    - porcentaje_despejes_cabeza_ganados

    Basado en:
    - 'clearance_body_part' == 'Head'
    - 'clearance_aerial_won' == True
    """
    df_jugadores = df_jugadores.copy()
    df = df_eventos.copy()

    # Inicializar columnas
    df_jugadores['despejes_cabeza_totales'] = 0
    df_jugadores['despejes_cabeza_ganados'] = 0
    df_jugadores['porcentaje_despejes_cabeza_ganados'] = 0.0

    for jugador in df_jugadores['player']:
        df_player = df[df['player'] == jugador]

        # Total de despejes con la cabeza
        total = df_player[df_player['clearance_body_part'] == 'Head'].shape[0]

        # Despejes aéreos ganados con la cabeza
        ganados = df_player[
            (df_player['clearance_body_part'] == 'Head') &
            (df_player['clearance_aerial_won'] == True)
        ].shape[0]

        porcentaje = 100 * ganados / total if total > 0 else 0

        df_jugadores.loc[df_jugadores['player'] == jugador, 'despejes_cabeza_totales'] = total
        df_jugadores.loc[df_jugadores['player'] == jugador, 'despejes_cabeza_ganados'] = ganados
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_despejes_cabeza_ganados'] = round(porcentaje, 2)

    return df_jugadores


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

def estadisticas_pases_por_jugador(df_eventos, df_jugadores):
    """
    Añade columnas al DataFrame de jugadores con estadísticas de pase:
    - pases_totales
    - pases_completados
    - pases_incompletos
    - pases_fuera
    - pases_fuera_de_juego
    - pases_fallidos
    - porcentaje_pases_completados
    """
    df_jugadores = df_jugadores.copy()
    df = df_eventos.copy()

    # Inicializar columnas
    columnas = [
        'pases_totales',
        'pases_completados',
        'pases_incompletos',
        'pases_fuera',
        'pases_fuera_de_juego',
        'pases_fallidos',
        'porcentaje_pases_completados'
    ]
    for col in columnas:
        df_jugadores[col] = 0

    for jugador in df_jugadores['player']:
        df_player = df[(df['player'] == jugador) & (df['type'] == 'Pass')]

        # Excluir pases "Unknown" o "Injury Clearance"
        df_validos = df_player[~df_player['pass_outcome'].isin(['Unknown', 'Injury Clearance'])]

        total = df_validos.shape[0]
        completados = df_validos['pass_outcome'].isnull().sum()
        incompletos = df_validos[df_validos['pass_outcome'] == 'Incomplete'].shape[0]
        fuera = df_validos[df_validos['pass_outcome'] == 'Out'].shape[0]
        offside = df_validos[df_validos['pass_outcome'] == 'Pass Offside'].shape[0]
        fallidos = incompletos + fuera + offside
        porcentaje = round(100 * completados / total, 2) if total > 0 else 0.0

        df_jugadores.loc[df_jugadores['player'] == jugador, 'pases_totales'] = total
        df_jugadores.loc[df_jugadores['player'] == jugador, 'pases_completados'] = completados
        df_jugadores.loc[df_jugadores['player'] == jugador, 'pases_incompletos'] = incompletos
        df_jugadores.loc[df_jugadores['player'] == jugador, 'pases_fuera'] = fuera
        df_jugadores.loc[df_jugadores['player'] == jugador, 'pases_fuera_de_juego'] = offside
        df_jugadores.loc[df_jugadores['player'] == jugador, 'pases_fallidos'] = fallidos
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_pases_completados'] = porcentaje

    return df_jugadores

