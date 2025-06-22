from pipeline.utils import log
import pandas as pd
import os

OUTPUT_DIR = "/opt/airflow/data/output"
CSV_PATH = f"{OUTPUT_DIR}/final_dataset.csv"
PARQUET_PATH = f"{OUTPUT_DIR}/final_dataset.parquet"

def save_csv(df):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_csv(CSV_PATH, index=False)
    log(f"CSV guardado en {CSV_PATH}")

def save_parquet(df):
    df.to_parquet(PARQUET_PATH, index=False)
    log(f"Parquet guardado en {PARQUET_PATH}")

def save_to_postgres(df):
    try:
        from sqlalchemy import create_engine
        engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres:5432/meli_case")
        df.to_sql("final_dataset", engine, index=False, if_exists="replace")
        log("Datos cargados exitosamente en PostgreSQL.")
    except Exception as e:
        log(f"[ERROR] Fallo al guardar en PostgreSQL: {e}")
        raise
