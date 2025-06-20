from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pipeline.load_data import load_all_sources
from pipeline.transform_data import generate_features
from pipeline.data_quality import run_quality_checks
from pipeline.save_outputs import save_csv, save_parquet, save_to_postgres

def start():
    print("DAG started")

def end():
    print("DAG finished")

def pipeline_flow():
    # Main pipeline flow for transforming and validating the data
    data = load_all_sources()
    df = generate_features(data)
    run_quality_checks(df)
    save_csv(df)
    save_parquet(df)
    save_to_postgres(df)

with DAG('mercado_libre_pipeline_dag',
         start_date=datetime(2024, 1, 1),
         schedule_interval=None,
         catchup=False) as dag:

    t1 = PythonOperator(task_id='start', python_callable=start)
    t2 = PythonOperator(task_id='run_pipeline', python_callable=pipeline_flow)
    t3 = PythonOperator(task_id='end', python_callable=end)

    t1 >> t2 >> t3
