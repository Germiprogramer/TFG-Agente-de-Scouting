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

def estadisticas_pases_zonas_peligrosas_por_jugador(df_eventos, df_jugadores):
    """
    Añade estadísticas de pases al tercio final y al área rival al DataFrame de jugadores.
    """
    df_jugadores = df_jugadores.copy()
    df = df_eventos[df_eventos['type'] == 'Pass'].copy()

    # Inicializar columnas
    df_jugadores['pases_tercio_final'] = 0
    df_jugadores['porcentaje_tercio_final_completados'] = 0.0
    df_jugadores['pases_al_area'] = 0
    df_jugadores['porcentaje_pases_area_completados'] = 0.0

    def es_en_area(loc):
        if not isinstance(loc, list):
            return False
        x, y = loc
        return x >= 102 and 18 <= y <= 62

    for jugador in df_jugadores['player']:
        df_player = df[df['player'] == jugador]

        # Tercio final
        en_tercio = df_player[df_player['pass_end_location'].apply(lambda loc: isinstance(loc, list) and loc[0] >= 80)]
        total_tercio = en_tercio.shape[0]
        completados_tercio = en_tercio['pass_outcome'].isnull().sum()
        porcentaje_tercio = 100 * completados_tercio / total_tercio if total_tercio > 0 else 0

        # Área rival
        en_area = df_player[df_player['pass_end_location'].apply(es_en_area)]
        total_area = en_area.shape[0]
        completados_area = en_area['pass_outcome'].isnull().sum()
        porcentaje_area = 100 * completados_area / total_area if total_area > 0 else 0

        # Asignar al jugador
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
