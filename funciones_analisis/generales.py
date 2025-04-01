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
