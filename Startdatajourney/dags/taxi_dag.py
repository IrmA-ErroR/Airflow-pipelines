from datetime import datetime

from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from airflow.providers.http.operators.http import SimpleHttpOperator
from .functions import download_dataset, convert_to_parquet

default_args = {
    'owner': 'airflow',
}

@dag(default_args=default_args,
     schedule_interval='@monthly',
     start_date=datetime(2020, 1, 1),
)
def nyc_taxi_dataset_dag():

   # здесь будут таски
   return 0
