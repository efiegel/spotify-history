from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'fiegel',
    'start_date': days_ago(1),
    'depends_on_past': True,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'mydag',
    default_args=default_args,
    description='first DAG',
    schedule_interval=timedelta(days=1),
)

def test():
    print("testing")

run_etl = PythonOperator(
    task_id='myetl',
    python_callable=test,
    dag=dag,
)

run_etl
