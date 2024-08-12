from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def print_hello():
    print("Привет!")

default_args = {
    'start_date': datetime(2023, 1, 1),
    'catchup': False
}

with DAG(dag_id='hello_world', default_args=default_args, schedule_interval=None) as dag:
    hello_task = PythonOperator(
        task_id='hello_task',
        python_callable=print_hello
    )
