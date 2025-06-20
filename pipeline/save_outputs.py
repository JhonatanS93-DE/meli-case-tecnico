import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import sqlalchemy

def save_csv(df):
    df.to_csv("data/output/final_dataset.csv", index=False)

def save_parquet(df):
    table = pa.Table.from_pandas(df)
    pq.write_table(table, "data/output/final_dataset.parquet")

def save_to_postgres(df):
    engine = sqlalchemy.create_engine("postgresql+psycopg2://airflow:airflow@localhost:5432/airflow")
    df.to_sql("value_prop_dataset", engine, if_exists='replace', index=False)
