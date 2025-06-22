import pandas as pd
from pipeline.utils import log

def load_jsonl_normalized(file_path, rename_timestamp=True):
    df = pd.read_json(file_path, lines=True)

    if 'event_data' in df.columns:
        event_df = pd.json_normalize(df['event_data'])
        df = df.drop(columns='event_data').join(event_df)

    if rename_timestamp and 'day' in df.columns:
        df.rename(columns={'day': 'timestamp'}, inplace=True)

    return df

def standardize_columns(df):
    if 'value_prop' in df.columns:
        df = df.rename(columns={'value_prop': 'value_prop_id'})
    return df

def load_all_sources():
    try:
        log("Cargando fuentes de datos...")

        prints = load_jsonl_normalized("/opt/airflow/data/input/prints.json", rename_timestamp=True)
        taps = load_jsonl_normalized("/opt/airflow/data/input/taps.json", rename_timestamp=True)
        pays = pd.read_csv("/opt/airflow/data/input/pays.csv")

        prints = standardize_columns(prints)
        taps = standardize_columns(taps)
        pays = standardize_columns(pays)

        if 'pay_date' in pays.columns:
            pays.rename(columns={'pay_date': 'timestamp'}, inplace=True)

        log("Fuentes cargadas correctamente.")
        return {"prints": prints, "taps": taps, "pays": pays}

    except Exception as e:
        log(f"[ERROR] Error cargando datos: {e}")
        raise
