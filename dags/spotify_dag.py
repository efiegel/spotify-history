import os
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from spotify_etl import run_spotify_etl


default_args = {
    'owner': 'admin',
    'start_date': days_ago(1),
    'depends_on_past': False,
    # 'email': [os.environ['DAG_EMAIL']],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'spotify_dag',
    default_args=default_args,
    description='Spotify DAG',
    schedule_interval=timedelta(hours=2),
)

run_etl = PythonOperator(
    task_id='spotify_etl',
    python_callable=run_spotify_etl,
    dag=dag,
)

run_etl
