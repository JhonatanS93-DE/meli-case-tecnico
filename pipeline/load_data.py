import pandas as pd

def load_jsonl_normalized(file_path):
    """
    Carga un archivo JSON Lines y normaliza la columna 'event_data' en columnas separadas.
    """
    df = pd.read_json(file_path, lines=True)
    if 'event_data' in df.columns:
        event_df = pd.json_normalize(df['event_data'])
        df = df.drop(columns='event_data').join(event_df)
    return df

def load_all_sources():
    """
    Carga y normaliza los archivos prints.json, taps.json y pays.csv.
    Devuelve un diccionario con los DataFrames.
    """
    prints = load_jsonl_normalized("data/input/prints.json")
    taps = load_jsonl_normalized("data/input/taps.json")
    pays = pd.read_csv("data/input/pays.csv")
    return {"prints": prints, "taps": taps, "pays": pays}