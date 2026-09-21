from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
}

with DAG('dbt_transform', 
         default_args=default_args, 
         schedule_interval='@once', 
         catchup=False) as dag:

    # Assuming the dbt folder is mounted at /opt/airflow/dbt in the docker-compose.yml
    # We need to mount the dbt folder into Airflow containers to run this.
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='dbt run --project-dir /opt/airflow/dbt --profiles-dir /opt/airflow/dbt',
    )
