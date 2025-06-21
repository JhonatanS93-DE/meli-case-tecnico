from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pipeline.load_data import load_all_sources
from pipeline.transform_data import generate_features
from pipeline.data_quality import run_quality_checks
from pipeline.save_outputs import save_csv, save_parquet, save_to_postgres

default_args = {
    'owner': 'Jhonatan Saldarriaga',
    'depends_on_past': False,
    'retries': 1
}

# Definición del DAG
with DAG(
    dag_id='mercado_libre_pipeline_dag',
    description='Construcción de dataset enriquecido para ML desde múltiples sources',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,  # Se ejecuta manualmente
    catchup=False,
    tags=["mercado-libre", "ml", "etl", "airflow", "dags"]
) as dag:

    def start(**kwargs):
        print("✅ DAG started")

    # Extracción de los datos desde archivos fuente
    def extract(**kwargs):
        ti = kwargs['ti']
        data = load_all_sources()
        ti.xcom_push(key='data_dict', value=data)

    # Transformación de los datos: creación de variables para ML
    def transform(**kwargs):
        ti = kwargs['ti']
        data = ti.xcom_pull(key='data_dict', task_ids='extract_data')
        df = generate_features(data)
        ti.xcom_push(key='final_df', value=df)

    # Validación de calidad de los datos
    def validate(**kwargs):
        ti = kwargs['ti']
        df = ti.xcom_pull(key='final_df', task_ids='transform_data')
        run_quality_checks(df)

    # Guardado del dataset en CSV, Parquet y PostgreSQL
    def save_outputs(**kwargs):
        ti = kwargs['ti']
        df = ti.xcom_pull(key='final_df', task_ids='transform_data')
        save_csv(df)
        save_parquet(df)
        save_to_postgres(df)

    def end(**kwargs):
        print("✅ DAG finished")

    t0 = PythonOperator(task_id='start', python_callable=start)
    t1 = PythonOperator(task_id='extract_data', python_callable=extract)
    t2 = PythonOperator(task_id='transform_data', python_callable=transform)
    t3 = PythonOperator(task_id='validate_data', python_callable=validate)
    t4 = PythonOperator(task_id='save_outputs', python_callable=save_outputs)
    t5 = PythonOperator(task_id='end', python_callable=end)

    t0 >> t1 >> t2 >> t3 >> t4 >> t5