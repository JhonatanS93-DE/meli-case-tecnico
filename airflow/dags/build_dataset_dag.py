from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pipeline.load_data import load_all_sources
from pipeline.transform_data import generate_features
from pipeline.data_quality import run_quality_checks
from pipeline.save_outputs import save_csv, save_parquet, save_to_postgres
from pipeline.utils import log
import sys

sys.path.append('/opt/airflow')

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
        ti.xcom_push(key='data_dict', value=data)

    def transform(**kwargs):
        log("Iniciando transformación")
        ti = kwargs['ti']
        data = ti.xcom_pull(key='data_dict', task_ids='extract_data')
        if data is None:
            raise ValueError("No se encontraron datos en XCom desde extract_data")
        df = generate_features(data)
        ti.xcom_push(key='final_df', value=df)

    def validate(**kwargs):
        log("Validación de calidad de datos")
        ti = kwargs['ti']
        df = ti.xcom_pull(key='final_df', task_ids='transform_data')
        if df is None:
            raise ValueError("No se encontraron datos transformados en XCom")
        run_quality_checks(df)

    def save_outputs(**kwargs):
        log("Guardando resultados")
        ti = kwargs['ti']
        df = ti.xcom_pull(key='final_df', task_ids='transform_data')
        if df is None:
            raise ValueError("No se encontraron datos transformados en XCom")
        save_csv(df)
        save_parquet(df)
        save_to_postgres(df)

    def end(**kwargs):
        log("DAG finalizado")

    t0 = PythonOperator(task_id='start', python_callable=start)
    t1 = PythonOperator(task_id='extract_data', python_callable=extract)
    t2 = PythonOperator(task_id='transform_data', python_callable=transform)
    t3 = PythonOperator(task_id='validate_data', python_callable=validate)
    t4 = PythonOperator(task_id='save_outputs', python_callable=save_outputs)
    t5 = PythonOperator(task_id='end', python_callable=end)

    t0 >> t1 >> t2 >> t3 >> t4 >> t5
