import os
import pandas as pd
from pipeline.utils import log

BASE_PATH = "/opt/airflow/pipeline/data/input"

def load_jsonl_normalized(file_path):
    df = pd.read_json(file_path, lines=True)
    if 'event_data' in df.columns:
        event_df = pd.json_normalize(df['event_data'])
        df = df.drop(columns='event_data').join(event_df)

    # Renombrar si existe la columna 'time'
    if 'time' in df.columns:
        df.rename(columns={'time': 'timestamp'}, inplace=True)

    return df

def load_all_sources():
    try:
        log("Cargando fuentes de datos...")
        prints = load_jsonl_normalized(os.path.join(BASE_PATH, "prints.json"))
        taps = load_jsonl_normalized(os.path.join(BASE_PATH, "taps.json"))
        pays = pd.read_csv(os.path.join(BASE_PATH, "pays.csv"))
        log("Fuentes cargadas correctamente.")
        return {"prints": prints, "taps": taps, "pays": pays}
    except Exception as e:
        log(f"Error cargando datos: {e}")
        raise
