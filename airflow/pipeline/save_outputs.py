from pipeline.utils import log
import pandas as pd
import os

def save_csv(df):
    os.makedirs("/opt/airflow/data/output", exist_ok=True)
    df.to_csv("/opt/airflow/data/output/final_dataset.csv", index=False)
    log("CSV guardado.")

def save_parquet(df):
    df.to_parquet("/opt/airflow/data/output/final_dataset.parquet", index=False)
    log("Parquet guardado.")

def save_to_postgres(df):
    from sqlalchemy import create_engine
    engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres:5432/meli_case")
    df.to_sql("final_dataset", engine, index=False, if_exists="replace")
    log("Datos cargados en PostgreSQL.")