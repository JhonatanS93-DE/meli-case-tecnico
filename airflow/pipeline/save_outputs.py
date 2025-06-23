from pipeline.utils import log
import pandas as pd
import os
from sqlalchemy import create_engine, text

def ensure_table_exists():
    engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres:5432/meli_case")
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS value_prop_dataset (
                user_id TEXT NOT NULL,
                value_prop_id TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                was_clicked BOOLEAN DEFAULT FALSE,
                views_last_3_weeks INTEGER DEFAULT 0,
                clicks_last_3_weeks INTEGER DEFAULT 0,
                payments_last_3_weeks INTEGER DEFAULT 0,
                total_amount_last_3_weeks NUMERIC(10, 2) DEFAULT 0.0
            );
        """))

def save_csv(df):
    os.makedirs("/opt/airflow/data/output", exist_ok=True)
    df.to_csv("/opt/airflow/data/output/final_dataset.csv", index=False)
    log("CSV guardado.")

def save_parquet(df):
    df.to_parquet("/opt/airflow/data/output/final_dataset.parquet", index=False)
    log("Parquet guardado.")

def save_to_postgres(df):
    ensure_table_exists()
    engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres:5432/meli_case")
    df.to_sql("value_prop_dataset", engine, index=False, if_exists="replace")
    log("Datos cargados en PostgreSQL.")
