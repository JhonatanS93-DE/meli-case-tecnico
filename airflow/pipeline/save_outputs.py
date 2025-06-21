import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import sqlalchemy
import os
from pipeline.utils import log

def save_csv(df):
    df.to_csv("data/output/final_dataset.csv", index=False)
    log("✅ CSV guardado en data/output/final_dataset.csv")

def save_parquet(df):
    table = pa.Table.from_pandas(df)
    pq.write_table(table, "data/output/final_dataset.parquet")
    log("✅ Parquet guardado en data/output/final_dataset.parquet")

def save_to_postgres(df):
    if df.empty:
        log("⚠️ Dataset vacío, no se guarda en PostgreSQL.")
        return
    conn_str = os.getenv("DB_CONN", "postgresql+psycopg2://airflow:airflow@localhost:5432/meli_case")
    engine = sqlalchemy.create_engine(conn_str)
    df.to_sql("value_prop_dataset", engine, if_exists='replace', index=False)
    log("📥 Datos guardados en PostgreSQL correctamente.")