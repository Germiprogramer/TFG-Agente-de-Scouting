from statsbombpy import sb

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

def estadisticas_pases_avanzadas_por_jugador(df_eventos, df_jugadores):
    """
    Añade columnas al DataFrame de jugadores con estadísticas avanzadas de pase.
    """
    df_jugadores = df_jugadores.copy()
    df = df_eventos[df_eventos['type'] == 'Pass'].copy()

    # Inicializar columnas
    columnas = [
        'media_longitud_pase',
        'media_angulo_pase',
        'ground_passes',
        'low_passes',
        'high_passes',
        'porcentaje_ground',
        'porcentaje_low',
        'porcentaje_high',
        'total_crosses',
        'crosses_completados',
        'cutbacks',
        'cutbacks_completados',
        'switches',
        'switches_completados',
        'pases_miscommunication',
        'pases_deflected'
    ]
    for col in columnas:
        df_jugadores[col] = 0.0

    def filtrar_pases_completados(df):
        df_filtrado = df[~df['pass_outcome'].isin(['Unknown', 'Injury Clearance'])]
        return df_filtrado[df_filtrado['pass_outcome'].isnull()]

    for jugador in df_jugadores['player']:
        df_player = df[df['player'] == jugador]

        df_completados = filtrar_pases_completados(df_player)
        df_altura = df_player[df_player['pass_height'].notnull()]

        media_longitud = df_completados['pass_length'].mean()
        media_angulo = df_completados['pass_angle'].mean()

        ground = df_altura[df_altura['pass_height'] == 'Ground Pass'].shape[0]
        low = df_altura[df_altura['pass_height'] == 'Low Pass'].shape[0]
        high = df_altura[df_altura['pass_height'] == 'High Pass'].shape[0]
        total_altura = df_altura.shape[0]

        porcentaje_ground = 100 * ground / total_altura if total_altura > 0 else 0
        porcentaje_low = 100 * low / total_altura if total_altura > 0 else 0
        porcentaje_high = 100 * high / total_altura if total_altura > 0 else 0

        crosses = df_player[df_player['pass_cross'] == True].shape[0]
        crosses_ok = df_completados[df_completados['pass_cross'] == True].shape[0]

        cutbacks = df_player[df_player['pass_cut_back'] == True].shape[0]
        cutbacks_ok = df_completados[df_completados['pass_cut_back'] == True].shape[0]

        switches = df_player[df_player['pass_switch'] == True].shape[0]
        switches_ok = df_completados[df_completados['pass_switch'] == True].shape[0]

        miscomm = df_player[df_player['pass_miscommunication'] == True].shape[0]
        deflected = df_player[df_player['pass_deflected'] == True].shape[0]

        df_jugadores.loc[df_jugadores['player'] == jugador, 'media_longitud_pase'] = media_longitud
        df_jugadores.loc[df_jugadores['player'] == jugador, 'media_angulo_pase'] = media_angulo
        df_jugadores.loc[df_jugadores['player'] == jugador, 'ground_passes'] = ground
        df_jugadores.loc[df_jugadores['player'] == jugador, 'low_passes'] = low
        df_jugadores.loc[df_jugadores['player'] == jugador, 'high_passes'] = high
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_ground'] = porcentaje_ground
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_low'] = porcentaje_low
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_high'] = porcentaje_high
        df_jugadores.loc[df_jugadores['player'] == jugador, 'total_crosses'] = crosses
        df_jugadores.loc[df_jugadores['player'] == jugador, 'crosses_completados'] = crosses_ok
        df_jugadores.loc[df_jugadores['player'] == jugador, 'cutbacks'] = cutbacks
        df_jugadores.loc[df_jugadores['player'] == jugador, 'cutbacks_completados'] = cutbacks_ok
        df_jugadores.loc[df_jugadores['player'] == jugador, 'switches'] = switches
        df_jugadores.loc[df_jugadores['player'] == jugador, 'switches_completados'] = switches_ok
        df_jugadores.loc[df_jugadores['player'] == jugador, 'pases_miscommunication'] = miscomm
        df_jugadores.loc[df_jugadores['player'] == jugador, 'pases_deflected'] = deflected

    return df_jugadores

def estadisticas_creacion_por_jugador(df_eventos, df_jugadores):
    """
    Añade columnas al DataFrame de jugadores con datos de creación ofensiva:
    - Asistencias de gol
    - Asistencias a tiro (key passes)
    - Ocasiones creadas totales
    """
    df_jugadores = df_jugadores.copy()
    df = df_eventos[df_eventos['type'] == 'Pass'].copy()

    # Inicializar columnas
    df_jugadores['goal_assists'] = 0
    df_jugadores['key_passes'] = 0
    df_jugadores['chances_created'] = 0

    for jugador in df_jugadores['player']:
        df_player = df[df['player'] == jugador]

        asistencias_gol = df_player[df_player['pass_goal_assist'] == True].shape[0]
        asistencias_tiro = df_player[df_player['pass_shot_assist'] == True].shape[0]
        total_chances = asistencias_gol + asistencias_tiro

        df_jugadores.loc[df_jugadores['player'] == jugador, 'goal_assists'] = asistencias_gol
        df_jugadores.loc[df_jugadores['player'] == jugador, 'key_passes'] = asistencias_tiro
        df_jugadores.loc[df_jugadores['player'] == jugador, 'chances_created'] = total_chances

    return df_jugadores


def estadisticas_tecnicas_pase_por_jugador(df_eventos, df_jugadores):
    """
    Añade al DataFrame de jugadores estadísticas técnicas de pase:
    - Through balls (completados y totales)
    - Uso del pie derecho, izquierdo, cabeza (y precisión)
    - Pases en campo propio vs rival
    """
    df_jugadores = df_jugadores.copy()
    df = df_eventos[df_eventos['type'] == 'Pass'].copy()

    # Inicializar columnas
    columnas = [
        'through_balls', 'through_balls_completados',
        'total_pases_con_body_part',
        'porcentaje_cabeza', 'porcentaje_derecho', 'porcentaje_izquierdo',
        'porcentaje_derecho_acertado', 'porcentaje_izquierdo_acertado',
        'pases_campo_propio', 'pases_campo_rival',
        'porcentaje_pases_campo_rival'
    ]
    for col in columnas:
        df_jugadores[col] = 0.0

    def filtrar_pases_completados(df_):
        df_filtrado = df_[~df_['pass_outcome'].isin(['Unknown', 'Injury Clearance'])]
        return df_filtrado[df_filtrado['pass_outcome'].isnull()]

    for jugador in df_jugadores['player']:
        df_player = df[df['player'] == jugador]
        df_completados = filtrar_pases_completados(df_player)

        # Through balls
        total_through = df_player[df_player['pass_technique'] == 'Through Ball'].shape[0]
        through_ok = df_completados[df_completados['pass_technique'] == 'Through Ball'].shape[0]

        # Partes del cuerpo
        con_body_part = df_player['pass_body_part'].notnull().sum()
        cabeza = df_player[df_player['pass_body_part'] == 'Head'].shape[0]
        derecho_df = df_player[df_player['pass_body_part'] == 'Right Foot']
        izquierdo_df = df_player[df_player['pass_body_part'] == 'Left Foot']

        derecho_total = derecho_df.shape[0]
        izquierdo_total = izquierdo_df.shape[0]
        derecho_ok = filtrar_pases_completados(derecho_df).shape[0]
        izquierdo_ok = filtrar_pases_completados(izquierdo_df).shape[0]

        pct_cabeza = 100 * cabeza / con_body_part if con_body_part > 0 else 0
        pct_derecho = 100 * derecho_total / con_body_part if con_body_part > 0 else 0
        pct_izquierdo = 100 * izquierdo_total / con_body_part if con_body_part > 0 else 0
        pct_derecho_ok = 100 * derecho_ok / derecho_total if derecho_total > 0 else 0
        pct_izquierdo_ok = 100 * izquierdo_ok / izquierdo_total if izquierdo_total > 0 else 0

        # Campo propio/rival
        pases_validos = df_player[~df_player['pass_outcome'].isin(['Unknown', 'Injury Clearance'])]
        campo_propio = pases_validos[pases_validos['location'].apply(lambda loc: isinstance(loc, list) and loc[0] < 60)].shape[0]
        campo_rival = pases_validos[pases_validos['location'].apply(lambda loc: isinstance(loc, list) and loc[0] >= 60)].shape[0]
        total_validos = pases_validos.shape[0]
        pct_rival = 100 * campo_rival / total_validos if total_validos > 0 else 0

        # Asignar al DataFrame
        df_jugadores.loc[df_jugadores['player'] == jugador, 'through_balls'] = total_through
        df_jugadores.loc[df_jugadores['player'] == jugador, 'through_balls_completados'] = through_ok
        df_jugadores.loc[df_jugadores['player'] == jugador, 'total_pases_con_body_part'] = con_body_part
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_cabeza'] = pct_cabeza
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_derecho'] = pct_derecho
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_izquierdo'] = pct_izquierdo
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_derecho_acertado'] = pct_derecho_ok
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_izquierdo_acertado'] = pct_izquierdo_ok
        df_jugadores.loc[df_jugadores['player'] == jugador, 'pases_campo_propio'] = campo_propio
        df_jugadores.loc[df_jugadores['player'] == jugador, 'pases_campo_rival'] = campo_rival
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_pases_campo_rival'] = pct_rival

    return df_jugadores

def estadisticas_pases_progresivos_por_jugador(df_eventos, df_jugadores):
    """
    Añade columnas al DataFrame de jugadores con estadísticas de pases progresivos tipo Wyscout.
    """
    df_jugadores = df_jugadores.copy()
    df = df_eventos[df_eventos['type'] == 'Pass'].copy()

    # Inicializar columnas
    df_jugadores['pases_progresivos_wyscout'] = 0
    df_jugadores['pases_progresivos_completados_wyscout'] = 0
    df_jugadores['porcentaje_pases_progresivos_completados'] = 0.0

    def filtrar_pases_completados(df_):
        df_filtrado = df_[~df_['pass_outcome'].isin(['Unknown', 'Injury Clearance'])]
        return df_filtrado[df_filtrado['pass_outcome'].isnull()]

    def es_progresivo_wyscout(start, end):
        if not (isinstance(start, list) and isinstance(end, list)):
            return False

        inicio = 120 - start[0]
        fin = 120 - end[0]
        ganancia = inicio - fin

        en_propio = start[0] < 60 and end[0] < 60
        cambia_de_mitad = start[0] < 60 and end[0] >= 60
        en_rival = start[0] >= 60 and end[0] >= 60

        if en_propio and ganancia >= 30:
            return True
        elif cambia_de_mitad and ganancia >= 15:
            return True
        elif en_rival and ganancia >= 10:
            return True
        else:
            return False

    for jugador in df_jugadores['player']:
        df_player = df[df['player'] == jugador]
        df_completados = filtrar_pases_completados(df_player)

        progresivos = df_player.apply(lambda row: es_progresivo_wyscout(row['location'], row['pass_end_location']), axis=1).sum()
        progresivos_ok = df_completados.apply(lambda row: es_progresivo_wyscout(row['location'], row['pass_end_location']), axis=1).sum()
        porcentaje = 100 * progresivos_ok / progresivos if progresivos > 0 else 0

        df_jugadores.loc[df_jugadores['player'] == jugador, 'pases_progresivos_wyscout'] = progresivos
        df_jugadores.loc[df_jugadores['player'] == jugador, 'pases_progresivos_completados_wyscout'] = progresivos_ok
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_pases_progresivos_completados'] = round(porcentaje, 2)

    return df_jugadores
def es_pase_en_tercio_final(loc):
    if isinstance(loc, list) and len(loc) == 2:
        x, y = loc
        return x >= 80
    return False

def es_pase_al_area(loc):
    if isinstance(loc, list) and len(loc) == 2:
        x, y = loc
        return x >= 102 and 18 <= y <= 62
    return False

def estadisticas_pases_zonas_peligrosas_por_jugador(df_eventos, df_jugadores):
    """
    Añade estadísticas de pases al tercio final y al área rival al DataFrame de jugadores.
    """
    df_jugadores = df_jugadores.copy()
    df = df_eventos[df_eventos['type'] == 'Pass'].copy()

    # Asegurar que pass_outcome es accesible como string (por si viene como dict)
    if 'pass_outcome' in df.columns:
        df['pass_outcome'] = df['pass_outcome'].apply(lambda x: x.get('name') if isinstance(x, dict) else x)

    # Añadir columnas nuevas al DataFrame
    df_jugadores['pases_tercio_final'] = 0
    df_jugadores['porcentaje_tercio_final_completados'] = 0.0
    df_jugadores['pases_al_area'] = 0
    df_jugadores['porcentaje_pases_area_completados'] = 0.0

    for jugador in df_jugadores['player']:
        df_player = df[df['player'] == jugador]

        # --- Tercio final ---
        en_tercio = df_player[df_player['pass_end_location'].apply(es_pase_en_tercio_final)]
        total_tercio = en_tercio.shape[0]
        completados_tercio = en_tercio['pass_outcome'].isnull().sum() if 'pass_outcome' in en_tercio.columns else 0
        porcentaje_tercio = 100 * completados_tercio / total_tercio if total_tercio > 0 else 0

        # --- Área rival ---
        en_area = df_player[df_player['pass_end_location'].apply(es_pase_al_area)]
        total_area = en_area.shape[0]
        completados_area = en_area['pass_outcome'].isnull().sum() if 'pass_outcome' in en_area.columns else 0
        porcentaje_area = 100 * completados_area / total_area if total_area > 0 else 0

        # Asignar a jugador
        df_jugadores.loc[df_jugadores['player'] == jugador, 'pases_tercio_final'] = total_tercio
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_tercio_final_completados'] = round(porcentaje_tercio, 2)
        df_jugadores.loc[df_jugadores['player'] == jugador, 'pases_al_area'] = total_area
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_pases_area_completados'] = round(porcentaje_area, 2)

    return df_jugadores


import numpy as np

def estadisticas_carries_por_jugador(df_eventos, df_jugadores):
    """
    Añade estadísticas de carries por jugador:
    - Carries válidos (≥5m)
    - Distancia media por carry
    - Carries progresivos
    - Porcentaje de carries progresivos (directness)
    """
    df_jugadores = df_jugadores.copy()
    df = df_eventos[df_eventos['type'] == 'Carry'].copy()

    # Inicializar columnas
    df_jugadores['carries'] = 0
    df_jugadores['carries_progresivos'] = 0
    df_jugadores['porcentaje_carries_progresivos'] = 0.0
    df_jugadores['distancia_media_carries'] = 0.0

    def es_valido(row):
        return isinstance(row['location'], list) and isinstance(row['carry_end_location'], list)

    def distancia(row):
        return np.linalg.norm(np.array(row['carry_end_location']) - np.array(row['location']))

    for jugador in df_jugadores['player']:
        df_player = df[df['player'] == jugador]
        df_player = df_player[df_player.apply(es_valido, axis=1)]

        # Carries válidos: distancia ≥ 5 metros
        df_carries = df_player[df_player.apply(lambda row: distancia(row) >= 5, axis=1)]
        total_carries = df_carries.shape[0]

        # Carries progresivos: ganancia horizontal ≥ 5 metros (hacia portería rival)
        carries_progresivos = df_carries[df_carries.apply(lambda row: row['carry_end_location'][0] - row['location'][0] >= 5, axis=1)].shape[0]

        # Distancia media
        if total_carries > 0:
            distancia_media = df_carries.apply(distancia, axis=1).mean()
        else:
            distancia_media = 0.0

        # Porcentaje progresivos
        pct_progresivos = 100 * carries_progresivos / total_carries if total_carries > 0 else 0

        # Guardar
        df_jugadores.loc[df_jugadores['player'] == jugador, 'carries'] = total_carries
        df_jugadores.loc[df_jugadores['player'] == jugador, 'carries_progresivos'] = carries_progresivos
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_carries_progresivos'] = round(pct_progresivos, 2)
        df_jugadores.loc[df_jugadores['player'] == jugador, 'distancia_media_carries'] = round(distancia_media, 2)

    return df_jugadores

def estadisticas_duelos_por_jugador(df_eventos, df_jugadores):
    """
    Añade columnas con estadísticas de duelos por jugador:
    - duelos_totales
    - duelos_ganados
    - porcentaje_duelos_ganados
    """
    df_jugadores = df_jugadores.copy()
    df = df_eventos[df_eventos['type'] == 'Duel'].copy()

    df_jugadores['duelos_totales'] = 0
    df_jugadores['duelos_ganados'] = 0
    df_jugadores['porcentaje_duelos_ganados'] = 0.0

    for jugador in df_jugadores['player']:
        df_player = df[df['player'] == jugador]
        df_validos = df_player[df_player['duel_outcome'].notnull()]
        total = df_validos.shape[0]
        ganados = df_validos['duel_outcome'].isin(['Won', 'Success In Play']).sum()
        porcentaje = 100 * ganados / total if total > 0 else 0

        df_jugadores.loc[df_jugadores['player'] == jugador, 'duelos_totales'] = total
        df_jugadores.loc[df_jugadores['player'] == jugador, 'duelos_ganados'] = ganados
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_duelos_ganados'] = round(porcentaje, 2)

    return df_jugadores

def estadisticas_tarjetas_por_jugador(df_eventos, df_jugadores):
    """
    Añade columnas con estadísticas disciplinarias:
    - tarjetas_amarillas
    - expulsiones
    """
    df_jugadores = df_jugadores.copy()

    df_jugadores['tarjetas_amarillas'] = 0
    df_jugadores['expulsiones'] = 0

    for jugador in df_jugadores['player']:
        df_player = df_eventos[df_eventos['player'] == jugador]

        amarillas_foul = df_player[df_player['foul_committed_card'] == 'Yellow Card'].shape[0]
        amarillas_behaviour = df_player[df_player['bad_behaviour_card'] == 'Yellow Card'].shape[0]

        rojas_foul = df_player[df_player['foul_committed_card'].isin(['Red Card', 'Second Yellow'])].shape[0]
        rojas_behaviour = df_player[df_player['bad_behaviour_card'].isin(['Red Card', 'Second Yellow'])].shape[0]

        df_jugadores.loc[df_jugadores['player'] == jugador, 'tarjetas_amarillas'] = amarillas_foul + amarillas_behaviour
        df_jugadores.loc[df_jugadores['player'] == jugador, 'expulsiones'] = rojas_foul + rojas_behaviour

    return df_jugadores

def estadisticas_defensivas_por_jugador(df_eventos, df_jugadores):
    """
    Añade columnas con métricas defensivas:
    - veces_regateado
    - recuperaciones
    - recuperaciones_ofensivas
    - presiones
    - counterpress
    """
    df_jugadores = df_jugadores.copy()

    df_jugadores['veces_regateado'] = 0
    df_jugadores['recuperaciones'] = 0
    df_jugadores['recuperaciones_ofensivas'] = 0
    df_jugadores['presiones'] = 0
    df_jugadores['counterpress'] = 0

    for jugador in df_jugadores['player']:
        df_player = df_eventos[df_eventos['player'] == jugador]

        regateado = df_player[df_player['type'] == 'Dribbled Past'].shape[0]

        recuperaciones = df_player[
            (df_player['type'] == 'Ball Recovery') & 
            (df_player['ball_recovery_recovery_failure'] != True)
        ].shape[0]

        ofensivas = df_player[
            (df_player['type'] == 'Ball Recovery') & 
            (df_player['ball_recovery_offensive'] == True)
        ].shape[0]

        presiones = df_player[df_player['type'] == 'Pressure'].shape[0]

        counterpress = df_player[
            (df_player['type'] == 'Pressure') & 
            (df_player['counterpress'] == True)
        ].shape[0]

        df_jugadores.loc[df_jugadores['player'] == jugador, 'veces_regateado'] = regateado
        df_jugadores.loc[df_jugadores['player'] == jugador, 'recuperaciones'] = recuperaciones
        df_jugadores.loc[df_jugadores['player'] == jugador, 'recuperaciones_ofensivas'] = ofensivas
        df_jugadores.loc[df_jugadores['player'] == jugador, 'presiones'] = presiones
        df_jugadores.loc[df_jugadores['player'] == jugador, 'counterpress'] = counterpress

    return df_jugadores

def estadisticas_regates_por_jugador(df_eventos, df_jugadores):
    """
    Añade estadísticas de regates al DataFrame de jugadores:
    - regates_completados
    - porcentaje_regates_completados
    """
    df_jugadores = df_jugadores.copy()
    df = df_eventos[df_eventos['type'] == 'Dribble'].copy()

    df_jugadores['regates_completados'] = 0
    df_jugadores['porcentaje_regates_completados'] = 0.0

    for jugador in df_jugadores['player']:
        df_player = df[df['player'] == jugador]
        df_validos = df_player[df_player['dribble_outcome'].notnull()]
        total = df_validos.shape[0]
        completados = df_validos[df_validos['dribble_outcome'] == 'Complete'].shape[0]
        porcentaje = 100 * completados / total if total > 0 else 0

        df_jugadores.loc[df_jugadores['player'] == jugador, 'regates_completados'] = completados
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_regates_completados'] = round(porcentaje, 2)

    return df_jugadores

def estadisticas_faltas_por_jugador(df_eventos, df_jugadores):
    """
    Añade columnas de faltas al DataFrame de jugadores:
    - faltas_provocadas
    - penaltis_provocados
    - faltas_cometidas
    - penaltis_cometidos
    """
    df_jugadores = df_jugadores.copy()

    df_jugadores['faltas_provocadas'] = 0
    df_jugadores['penaltis_provocados'] = 0
    df_jugadores['faltas_cometidas'] = 0
    df_jugadores['penaltis_cometidos'] = 0

    for jugador in df_jugadores['player']:
        df_player = df_eventos[df_eventos['player'] == jugador]

        provocadas = df_player[df_player['type'] == 'Foul Won'].shape[0]
        penales_provocados = df_player[
            (df_player['type'] == 'Foul Won') & 
            (df_player['foul_won_penalty'] == True)
        ].shape[0]

        cometidas = df_player[df_player['type'] == 'Foul Committed'].shape[0]
        penales_cometidos = df_player[
            (df_player['type'] == 'Foul Committed') & 
            (df_player['foul_committed_penalty'] == True)
        ].shape[0]

        df_jugadores.loc[df_jugadores['player'] == jugador, 'faltas_provocadas'] = provocadas
        df_jugadores.loc[df_jugadores['player'] == jugador, 'penaltis_provocados'] = penales_provocados
        df_jugadores.loc[df_jugadores['player'] == jugador, 'faltas_cometidas'] = cometidas
        df_jugadores.loc[df_jugadores['player'] == jugador, 'penaltis_cometidos'] = penales_cometidos

    return df_jugadores

def calcular_minutos_jugados_en_df(lista_partidos, df_jugadores):
    """
    Calcula los minutos jugados por cada jugador en el dataset de jugadores.

    Parámetros:
    - lista_partidos: lista de IDs de partidos
    - df_jugadores: DataFrame con al menos las columnas 'player_id' y 'player'

    Retorna:
    - df_jugadores con una nueva columna 'minutos_jugados'
    """
    minutos_totales = {}

    for i, match_id in enumerate(lista_partidos):
        try:
            partido = sb.events(match_id=match_id)

            jugadores_partido = []

            # Alineaciones iniciales
            alineaciones = partido[partido['type'] == 'Starting XI']
            for _, row in alineaciones.iterrows():
                tactics = row.get('tactics', {})
                lineup = tactics.get('lineup', [])
                if isinstance(lineup, list):
                    for jugador in lineup:
                        if isinstance(jugador, dict) and 'player' in jugador:
                            jugadores_partido.append({
                                'player_id': jugador['player']['id'],
                                'minuto_inicio': 0,
                                'minuto_fin': 90
                            })

            # Sustituciones
            sustituciones = partido[partido['type'] == 'Substitution']
            for _, row in sustituciones.iterrows():
                jugador_fuera = row.get('player')
                sustitucion = row.get('substitution', {})
                jugador_dentro = sustitucion.get('replacement')
                minuto_sustitucion = row.get('minute', 0)

                if isinstance(jugador_fuera, dict) and isinstance(jugador_dentro, dict):
                    for jugador in jugadores_partido:
                        if jugador['player_id'] == jugador_fuera['id']:
                            jugador['minuto_fin'] = minuto_sustitucion

                    jugadores_partido.append({
                        'player_id': jugador_dentro['id'],
                        'minuto_inicio': minuto_sustitucion,
                        'minuto_fin': 90
                    })

            for jugador in jugadores_partido:
                minutos = jugador['minuto_fin'] - jugador['minuto_inicio']
                pid = jugador['player_id']

                if pid not in minutos_totales:
                    minutos_totales[pid] = 0
                minutos_totales[pid] += minutos

            if (i + 1) % 20 == 0:
                print(f"✅ Procesados {i+1}/{len(lista_partidos)} partidos")

        except Exception as e:
            print(f"❌ Error en partido {match_id}: {e}")
            continue

    # Añadir los minutos al dataframe original de jugadores
    df_jugadores = df_jugadores.copy()
    df_jugadores["minutos_jugados"] = df_jugadores["player_id"].map(minutos_totales).fillna(0).astype(int)

    return df_jugadores

def estadisticas_tiro_basicas_por_jugador(df_eventos, df_jugadores):
    """
    Añade estadísticas de tiro básicas por jugador:
    - goles_marcados
    - tiros_intentados
    - tiros_utiles
    - tiros_a_puerta
    - tiros_fuera
    - tiros_bloqueados
    - porcentaje_tiros_a_puerta
    """
    df_jugadores = df_jugadores.copy()

    df_jugadores['goles_marcados'] = 0
    df_jugadores['tiros_intentados'] = 0
    df_jugadores['tiros_utiles'] = 0
    df_jugadores['tiros_a_puerta'] = 0
    df_jugadores['tiros_fuera'] = 0
    df_jugadores['tiros_bloqueados'] = 0
    df_jugadores['porcentaje_tiros_a_puerta'] = 0.0

    for jugador in df_jugadores['player']:
        df_player = df_eventos[df_eventos['player'] == jugador]

        # Asegurarse de que existan las columnas necesarias
        if 'shot_outcome' not in df_player.columns:
            continue

        df_shots = df_player[df_player['type'] == 'Shot']

        goles = df_shots[df_shots['shot_outcome'] == 'Goal'].shape[0]
        intentos = df_shots.shape[0]
        utiles = df_shots[df_shots['shot_outcome'] != 'Blocked'].shape[0]
        a_puerta = df_shots[df_shots['shot_outcome'].isin(['Goal', 'Saved', 'Saved To Post'])].shape[0]
        fuera = df_shots[df_shots['shot_outcome'].isin(['Off T', 'Wayward', 'Post'])].shape[0]
        bloqueados = df_shots[df_shots['shot_outcome'] == 'Blocked'].shape[0]
        porcentaje = round(100 * a_puerta / utiles, 2) if utiles > 0 else 0.0

        df_jugadores.loc[df_jugadores['player'] == jugador, 'goles_marcados'] = goles
        df_jugadores.loc[df_jugadores['player'] == jugador, 'tiros_intentados'] = intentos
        df_jugadores.loc[df_jugadores['player'] == jugador, 'tiros_utiles'] = utiles
        df_jugadores.loc[df_jugadores['player'] == jugador, 'tiros_a_puerta'] = a_puerta
        df_jugadores.loc[df_jugadores['player'] == jugador, 'tiros_fuera'] = fuera
        df_jugadores.loc[df_jugadores['player'] == jugador, 'tiros_bloqueados'] = bloqueados
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_tiros_a_puerta'] = porcentaje

    return df_jugadores

def estadisticas_xg_por_jugador(df_eventos, df_jugadores):
    """
    Añade columnas de estadísticas de expected goals (xG) al DataFrame de jugadores:
    - xg_total
    - xg_promedio
    - diferencia_goles_xg
    """
    df_jugadores = df_jugadores.copy()
    df_jugadores['xg_total'] = 0.0
    df_jugadores['xg_promedio'] = 0.0
    df_jugadores['diferencia_goles_xg'] = 0.0

    for jugador in df_jugadores['player']:
        df_player = df_eventos[df_eventos['player'] == jugador]
        df_shots = df_player[df_player['type'] == 'Shot']

        if df_shots.empty or 'shot_statsbomb_xg' not in df_shots.columns:
            continue

        xg_total = df_shots['shot_statsbomb_xg'].sum()
        xg_promedio = df_shots['shot_statsbomb_xg'].mean()
        goles_reales = df_shots[df_shots['shot_outcome'] == 'Goal'].shape[0]
        diferencia = round(goles_reales - xg_total, 2)

        df_jugadores.loc[df_jugadores['player'] == jugador, 'xg_total'] = xg_total
        df_jugadores.loc[df_jugadores['player'] == jugador, 'xg_promedio'] = xg_promedio
        df_jugadores.loc[df_jugadores['player'] == jugador, 'diferencia_goles_xg'] = diferencia

    return df_jugadores

def estadisticas_tiro_area_y_penalti_por_jugador(df_eventos, df_jugadores):
    """
    Añade columnas al DataFrame de jugadores con estadísticas de tiros desde el área y penaltis:
    - goles_penalti
    - tiros_dentro_area
    - tasa_conversion_dentro_area
    """
    df_jugadores = df_jugadores.copy()

    df_jugadores['goles_penalti'] = 0
    df_jugadores['tiros_dentro_area'] = 0
    df_jugadores['tasa_conversion_dentro_area'] = 0.0

    def es_dentro_area(loc):
        if isinstance(loc, list) and len(loc) == 2:
            x, y = loc
            return x >= 102 and 18 <= y <= 62
        return False

    for jugador in df_jugadores['player']:
        df_player = df_eventos[df_eventos['player'] == jugador]
        df_shots = df_player[df_player['type'] == 'Shot']

        # Si no hay columnas necesarias, salta al siguiente jugador
        if df_shots.empty or 'shot_outcome' not in df_shots.columns or 'shot_type' not in df_shots.columns:
            continue

        # Goles desde penalti
        goles_penalti = df_shots[
            (df_shots['shot_type'] == 'Penalty') & 
            (df_shots['shot_outcome'] == 'Goal')
        ].shape[0]

        # Tiros dentro del área
        tiros_area = df_shots[df_shots['location'].apply(es_dentro_area)]
        tiros_dentro_area = tiros_area.shape[0]

        # Tasa de conversión dentro del área
        goles_area = tiros_area[tiros_area['shot_outcome'] == 'Goal']
        tasa_conversion = round(100 * goles_area.shape[0] / tiros_dentro_area, 2) if tiros_dentro_area > 0 else 0.0

        # Guardar resultados
        df_jugadores.loc[df_jugadores['player'] == jugador, 'goles_penalti'] = goles_penalti
        df_jugadores.loc[df_jugadores['player'] == jugador, 'tiros_dentro_area'] = tiros_dentro_area
        df_jugadores.loc[df_jugadores['player'] == jugador, 'tasa_conversion_dentro_area'] = tasa_conversion

    return df_jugadores

def porcentaje_goles_por_parte_cuerpo_por_jugador(df_eventos, df_jugadores):
    df_jugadores = df_jugadores.copy()

    df_jugadores['goles_izquierda_pct'] = 0.0
    df_jugadores['goles_derecha_pct'] = 0.0
    df_jugadores['goles_cabeza_pct'] = 0.0

    for jugador in df_jugadores['player']:
        df_player = df_eventos[(df_eventos['player'] == jugador) & 
                               (df_eventos['type'] == 'Shot') & 
                               (df_eventos['shot_outcome'] == 'Goal')]

        total = df_player.shape[0]
        if total == 0:
            continue

        porcentaje = df_player['shot_body_part'].value_counts(normalize=True) * 100

        df_jugadores.loc[df_jugadores['player'] == jugador, 'goles_izquierda_pct'] = round(porcentaje.get('Left Foot', 0.0), 2)
        df_jugadores.loc[df_jugadores['player'] == jugador, 'goles_derecha_pct'] = round(porcentaje.get('Right Foot', 0.0), 2)
        df_jugadores.loc[df_jugadores['player'] == jugador, 'goles_cabeza_pct'] = round(porcentaje.get('Head', 0.0), 2)

    return df_jugadores

def goles_de_falta_por_jugador(df_eventos, df_jugadores):
    df_jugadores = df_jugadores.copy()
    df_jugadores['goles_de_falta'] = 0

    for jugador in df_jugadores['player']:
        df_player = df_eventos[(df_eventos['player'] == jugador) & 
                               (df_eventos['type'] == 'Shot') & 
                               (df_eventos['shot_type'] == 'Free Kick') & 
                               (df_eventos['shot_outcome'] == 'Goal')]

        goles = df_player.shape[0]
        df_jugadores.loc[df_jugadores['player'] == jugador, 'goles_de_falta'] = goles

    return df_jugadores

def estadisticas_porteros_por_jugador(df_eventos, df_jugadores):
    """
    Añade estadísticas de porteros al DataFrame de jugadores:
    - paradas_reales
    - porcentaje_paradas_exitosas
    - indice_dominio_aereo
    - penaltis_parados
    - porcentaje_penaltis_parados
    - keeper_sweeper_acciones
    """
    df_jugadores = df_jugadores.copy()

    df_jugadores['paradas_reales'] = 0
    df_jugadores['porcentaje_paradas_exitosas'] = 0.0
    df_jugadores['indice_dominio_aereo'] = 0.0
    df_jugadores['penaltis_parados'] = 0
    df_jugadores['porcentaje_penaltis_parados'] = 0.0
    df_jugadores['keeper_sweeper_acciones'] = 0

    for jugador in df_jugadores['player']:
        df_player = df_eventos[df_eventos['player'] == jugador]

        # Asegurarse de que las columnas están limpias
        if df_player.empty or 'goalkeeper_type' not in df_player.columns:
            continue

        tipos_validos = [
            'Shot Saved', 'Shot Saved Off T', 'Shot Saved To Post',
            'Saved To Post', 'Penalty Saved To Post', 'Penalty Saved'
        ]
        outcomes_validos = [
            'Success', 'In Play Safe', 'In Play Danger',
            'Saved Twice', 'Touched Out', 'Won'
        ]

        # 1. Paradas reales
        paradas = df_player[
            df_player['goalkeeper_type'].isin(tipos_validos) &
            df_player['goalkeeper_outcome'].isin(outcomes_validos)
        ].shape[0]

        # 2. Porcentaje paradas exitosas
        tipos_parada = tipos_validos
        tipos_gol = ['Goal Conceded', 'Penalty Conceded']

        n_paradas = df_player[df_player['goalkeeper_type'].isin(tipos_parada)].shape[0]
        n_goles = df_player[df_player['goalkeeper_type'].isin(tipos_gol)].shape[0]
        total_tiros = n_paradas + n_goles
        pct_paradas = round(100 * n_paradas / total_tiros, 2) if total_tiros > 0 else 0.0

        # 3. Dominio aéreo
        claims = df_player[df_player['goalkeeper_outcome'] == 'Claim'].shape[0]
        punches = df_player[df_player['goalkeeper_type'] == 'Punch'].shape[0]
        collected_twice = df_player[df_player['goalkeeper_outcome'] == 'Collected Twice'].shape[0]
        aerial_types = ['Collected', 'Punch', 'Claim', 'Collected Twice']
        fails_aereos = df_player[
            (df_player['goalkeeper_outcome'] == 'Fail') &
            df_player['goalkeeper_type'].isin(aerial_types)
        ].shape[0]
        idap = (1.0 * claims) + (0.7 * punches) + (0.3 * collected_twice) - (1.0 * fails_aereos)
        idap = round(idap, 2)

        # 4. Penaltis parados
        paradas_penalti = ['Penalty Saved', 'Penalty Saved To Post']
        penaltis_parados = df_player[
            df_player['goalkeeper_type'].isin(paradas_penalti)
        ].shape[0]

        # 5. % penaltis parados
        tipos_penalti = ['Penalty Faced', 'Penalty Saved', 'Penalty Saved To Post', 'Penalty Conceded']
        df_penales = df_player[df_player['goalkeeper_type'].isin(tipos_penalti)]
        total_penales = df_penales.shape[0]
        pct_penales = round((penaltis_parados / total_penales) * 100, 2) if total_penales > 0 else 0.0

        # 6. Keeper Sweeper
        keeper_sweeper = df_player[df_player['goalkeeper_type'] == 'Keeper Sweeper'].shape[0]

        # Guardar en el dataset
        df_jugadores.loc[df_jugadores['player'] == jugador, 'paradas_reales'] = paradas
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_paradas_exitosas'] = pct_paradas
        df_jugadores.loc[df_jugadores['player'] == jugador, 'indice_dominio_aereo'] = idap
        df_jugadores.loc[df_jugadores['player'] == jugador, 'penaltis_parados'] = penaltis_parados
        df_jugadores.loc[df_jugadores['player'] == jugador, 'porcentaje_penaltis_parados'] = pct_penales
        df_jugadores.loc[df_jugadores['player'] == jugador, 'keeper_sweeper_acciones'] = keeper_sweeper

    return df_jugadores

def estadisticas_avanzadas_portero_por_jugador(df_eventos, df_jugadores, df_partidos):
    """
    Añade estadísticas avanzadas de portero al DataFrame de jugadores:
    - PSxG (post-shot xG recibido)
    - OPA (acciones defensivas fuera del área)
    - imbatibilidades (porterías a cero)
    """
    from collections import defaultdict

    df_jugadores = df_jugadores.copy()
    df_jugadores['PSxG'] = 0.0
    df_jugadores['OPA'] = 0
    df_jugadores['imbatibilidades'] = 0

    # 1. PSxG
    tiros = df_eventos[
        (df_eventos['type'] == 'Shot') &
        (df_eventos['shot_outcome'].isin(['Goal', 'Saved', 'Saved To Post']))
    ][['match_id', 'team', 'shot_statsbomb_xg']].copy()

    porteros = df_eventos[df_eventos['type'] == 'Goal Keeper'][['match_id', 'player', 'team']].drop_duplicates()

    psxg_dict = defaultdict(float)

    for _, tiro in tiros.iterrows():
        match_id = tiro['match_id']
        equipo_tirador = tiro['team']
        xg = tiro['shot_statsbomb_xg']
        porteros_partido = porteros[(porteros['match_id'] == match_id) & (porteros['team'] != equipo_tirador)]
        if not porteros_partido.empty:
            portero = porteros_partido.iloc[0]['player']
            psxg_dict[portero] += xg

    for jugador in df_jugadores['player']:
        if jugador in psxg_dict:
            df_jugadores.loc[df_jugadores['player'] == jugador, 'PSxG'] = round(psxg_dict[jugador], 2)

    # 2. OPA
    acciones = df_eventos[
        (df_eventos['player'].notnull()) &
        (df_eventos['type'].isin(['Pressure', 'Ball Recovery', 'Interception', 'Duel']))
    ].copy()

    def fuera_del_area(loc):
        if isinstance(loc, list) and len(loc) == 2:
            x, y = loc
            return x < 102 or y < 18 or y > 62
        return False

    acciones = acciones[acciones['location'].apply(fuera_del_area)]
    opa_agrupado = acciones.groupby('player').size().reset_index(name='OPA')

    for _, row in opa_agrupado.iterrows():
        jugador = row['player']
        valor = row['OPA']
        df_jugadores.loc[df_jugadores['player'] == jugador, 'OPA'] = valor

    # 3. Imbatibilidades
    imbatibilidades = defaultdict(int)
    match_ids = df_partidos['match_id'].unique()

    for match_id in match_ids:
        try:
            eventos_partido = df_eventos[df_eventos['match_id'] == match_id]
            alineaciones = eventos_partido[eventos_partido['type'] == 'Starting XI']
            partido_info = df_partidos[df_partidos['match_id'] == match_id].iloc[0]
            home_team = partido_info['home_team']
            away_team = partido_info['away_team']
            home_goals = partido_info['home_score']
            away_goals = partido_info['away_score']

            for _, row in alineaciones.iterrows():
                equipo = row['team']
                es_local = equipo == home_team
                goles_en_contra = away_goals if es_local else home_goals
                if goles_en_contra == 0:
                    lineup = row.get('tactics', {}).get('lineup', [])
                    for jugador in lineup:
                        if isinstance(jugador, dict):
                            if jugador['position']['name'] == 'Goalkeeper':
                                pid = jugador['player']['id']
                                imbatibilidades[pid] += 1
        except:
            continue

    for pid, imba in imbatibilidades.items():
        df_jugadores.loc[df_jugadores['player_id'] == pid, 'imbatibilidades'] = imba

    return df_jugadores

def añadir_goles_encajados_por_portero(df_eventos, df_jugadores):
    """
    Añade columna 'goles_encajados' al df_jugadores.
    Se basa en tiros que terminan en gol, asignando el gol al portero rival del equipo que disparó.
    """
    from collections import defaultdict

    df_jugadores = df_jugadores.copy()
    df_jugadores["goles_encajados"] = 0

    # Goles marcados por jugadores
    tiros_gol = df_eventos[
        (df_eventos["type"] == "Shot") &
        (df_eventos["shot_outcome"] == "Goal")
    ][["match_id", "team"]]

    # Eventos de portero (para identificar porteros por equipo y partido)
    porteros = df_eventos[df_eventos["type"] == "Goal Keeper"]
    porteros = porteros[["match_id", "team", "player"]].drop_duplicates()

    goles_por_portero = defaultdict(int)

    for _, row in tiros_gol.iterrows():
        match_id = row["match_id"]
        equipo_tirador = row["team"]

        portero_rival = porteros[
            (porteros["match_id"] == match_id) & (porteros["team"] != equipo_tirador)
        ]

        if not portero_rival.empty:
            portero = portero_rival.iloc[0]["player"]
            goles_por_portero[portero] += 1

    for player, goles in goles_por_portero.items():
        df_jugadores.loc[df_jugadores["player"] == player, "goles_encajados"] = goles

    return df_jugadores

def añadir_diferencia_PSxG_y_goles(df_jugadores):
    """
    Añade una columna 'diferencia_PSxG_goles' que compara PSxG y goles encajados:
    positivo si el portero ha parado más de lo esperado (bueno),
    negativo si ha encajado más de lo esperado (malo).
    """
    df_jugadores = df_jugadores.copy()

    if 'PSxG' not in df_jugadores.columns or 'goles_encajados' not in df_jugadores.columns:
        raise ValueError("Faltan las columnas 'PSxG' o 'goles_encajados' en el DataFrame.")

    df_jugadores["diferencia_PSxG_goles"] = round(
        df_jugadores["PSxG"] - df_jugadores["goles_encajados"], 2
    )

    return df_jugadores
