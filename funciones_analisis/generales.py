import pandas as pd
import statsbombpy as sb


def filtrar_partidos_por_equipo(df_matches, nombre_equipo):
    return df_matches[(df_matches['home_team'] == nombre_equipo) | (df_matches['away_team'] == nombre_equipo)]


def filtrar_eventos_por_columna_util(df_eventos, jugador, columna):
    # Filtrar por jugador
    df_jugador = df_eventos[df_eventos['player'] == jugador]
    
    # Filtrar filas donde la columna elegida no sea NaN
    df_filtrado = df_jugador[df_jugador[columna].notna()]
    
    # Eliminar columnas que están completamente vacías
    df_limpio = df_filtrado.dropna(axis=1, how='all')
    
    return df_limpio

def valores_unicos_columna(df, columna, contar=False):
    """
    Devuelve los valores únicos (o su conteo) de una columna de un DataFrame.

    Parámetros:
    - df: DataFrame
    - columna: nombre de la columna (string)
    - contar: si es True, devuelve un conteo de valores; si es False, una lista única

    Retorna:
    - Lista de valores únicos o Series con conteos
    """
    if columna not in df.columns:
        raise ValueError(f"La columna '{columna}' no existe en el DataFrame.")
    
    serie = df[columna].dropna()

    # Si los valores son diccionarios con 'name', los extraemos
    if isinstance(serie.iloc[0], dict) and 'name' in serie.iloc[0]:
        serie = serie.apply(lambda x: x['name'])

    return serie.value_counts() if contar else serie.unique()

def ordenar_partidos_cronologicamente(df_partidos):
    df = df_partidos.copy()
    
    # Convertir a tipo datetime (fecha y hora combinadas)
    df['fecha_hora'] = pd.to_datetime(df['match_date'] + ' ' + df['kick_off'])
    
    # Ordenar por fecha y hora
    df_ordenado = df.sort_values(by='fecha_hora').reset_index(drop=True)
    
    return df_ordenado


from statsbombpy import sb
import pandas as pd

def jugadores_faltantes_en_df(lista_match_ids, df_jugadores):
    """
    Obtiene todos los jugadores que han jugado al menos un partido, y los compara
    con un DataFrame de jugadores.

    Parámetros:
    - lista_match_ids: lista de ints, ids de partidos
    - df_jugadores: DataFrame con columnas 'player_id' y 'player'

    Retorna:
    - DataFrame con jugadores que han jugado pero no están en df_jugadores
    """

    jugadores_partidos = set()

    for i, match_id in enumerate(lista_match_ids):
        try:
            partido = sb.events(match_id=match_id)

            # Titulares
            alineaciones = partido[partido['type'] == 'Starting XI']
            for _, row in alineaciones.iterrows():
                lineup = row.get('tactics', {}).get('lineup', [])
                for jugador in lineup:
                    if isinstance(jugador, dict) and 'player' in jugador:
                        jugadores_partidos.add((
                            jugador['player']['id'],
                            jugador['player']['name']
                        ))

            # Sustituciones
            sustituciones = partido[partido['type'] == 'Substitution']
            for _, row in sustituciones.iterrows():
                fuera = row.get('player')
                dentro = row.get('substitution', {}).get('replacement')

                if isinstance(fuera, dict):
                    jugadores_partidos.add((fuera['id'], fuera['name']))
                if isinstance(dentro, dict):
                    jugadores_partidos.add((dentro['id'], dentro['name']))

            if (i + 1) % 20 == 0:
                print(f"✅ Procesados {i+1}/{len(lista_match_ids)} partidos")

        except Exception as e:
            print(f"❌ Error en partido {match_id}: {e}")
            continue

    # Convertir a DataFrame
    df_partido = pd.DataFrame(jugadores_partidos, columns=['player_id', 'player'])

    # Buscar los que faltan
    df_faltantes = df_partido[~df_partido['player_id'].isin(df_jugadores['player_id'])]

    return df_faltantes

def calcular_eventos_por_partido(competition_id, season_id, verbose=False):
    """
    Calcula el número promedio de eventos por partido para una competición y temporada específica.

    Parámetros:
    - competition_id: ID de la competición (por ejemplo, 11 para La Liga)
    - season_id: ID de la temporada (por ejemplo, 4 para 2015/2016)
    - verbose: si True, imprime el progreso partido a partido

    Devuelve:
    - promedio (float): media de eventos por partido
    - df_eventos (DataFrame): tabla con match_id y número de eventos por partido
    """
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    match_ids = matches['match_id'].tolist()

    eventos_por_partido = []

    for i, match_id in enumerate(match_ids):
        try:
            eventos = sb.events(match_id=match_id)
            eventos_por_partido.append({
                "match_id": match_id,
                "num_eventos": len(eventos)
            })
            if verbose:
                print(f"✔️ {i+1}/{len(match_ids)} - {match_id} ({len(eventos)} eventos)")
        except Exception as e:
            print(f"❌ Error en match {match_id}: {e}")

    df_eventos = pd.DataFrame(eventos_por_partido)
    promedio = df_eventos["num_eventos"].mean()

    return promedio, df_eventos