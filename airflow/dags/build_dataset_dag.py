from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pipeline.load_data import load_all_sources
from pipeline.transform_data import generate_features
from pipeline.data_quality import run_quality_checks
from pipeline.save_outputs import save_csv, save_parquet, save_to_postgres
from pipeline.utils import log
import pandas as pd
import os

default_args = {
    'owner': 'Jhonatan Saldarriaga',
    'depends_on_past': False,
    'retries': 1
}

with DAG(
    dag_id='mercado_libre_pipeline_dag',
    description='Construcción de dataset enriquecido para ML desde múltiples sources',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["mercado-libre", "ml", "etl", "airflow", "dags"]
) as dag:

    def start(**kwargs):
        log("DAG iniciado")

    def extract(**kwargs):
        log("Iniciando extracción de datos")
        ti = kwargs['ti']
        data = load_all_sources()

        path = '/opt/airflow/tmp/data.pkl'
        os.makedirs(os.path.dirname(path), exist_ok=True)

        pd.to_pickle(data, path)
        ti.xcom_push(key='data_path', value=path)
        log("Extracción completada y datos guardados")

    def transform(**kwargs):
        log("Iniciando transformación de datos")
        ti = kwargs['ti']
        path = ti.xcom_pull(key='data_path', task_ids='extract_data')
        if not path or not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el archivo de datos: {path}")
        data = pd.read_pickle(path)
        df = generate_features(data)
        output_path = "/opt/airflow/tmp/final_df.pkl"
        pd.to_pickle(df, output_path)
        ti.xcom_push(key='df_path', value=output_path)
        log("Transformación finalizada")

    def validate(**kwargs):
        log("🔎 Validando calidad de los datos")
        ti = kwargs['ti']
        path = ti.xcom_pull(key='df_path', task_ids='transform_data')
        if not path or not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el archivo del DataFrame transformado: {path}")
        df = pd.read_pickle(path)
        run_quality_checks(df)
        log("Validación finalizada")

    def save_outputs(**kwargs):
        log("Guardando resultados")
        ti = kwargs['ti']
        path = ti.xcom_pull(key='df_path', task_ids='transform_data')
        if not path or not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el archivo del DataFrame transformado: {path}")
        df = pd.read_pickle(path)
        save_csv(df)
        save_parquet(df)
        save_to_postgres(df)
        log("Resultados guardados exitosamente")

    def end(**kwargs):
        log("DAG finalizado correctamente")

    # Definir tareas
    t0 = PythonOperator(task_id='start', python_callable=start)
    t1 = PythonOperator(task_id='extract_data', python_callable=extract)
    t2 = PythonOperator(task_id='transform_data', python_callable=transform)
    t3 = PythonOperator(task_id='validate_data', python_callable=validate)
    t4 = PythonOperator(task_id='save_outputs', python_callable=save_outputs)
    t5 = PythonOperator(task_id='end', python_callable=end)

    # Definir flujo de ejecución
    t0 >> t1 >> t2 >> t3 >> t4 >> t5
