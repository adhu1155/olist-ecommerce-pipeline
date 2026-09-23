from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import pandas as pd
import io

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
}

def load_data_to_postgres():
    s3_hook = S3Hook(aws_conn_id='minio_conn')
    pg_hook = PostgresHook(postgres_conn_id='postgres_warehouse')
    bucket_name = 'raw-data'
    
    # List all objects in the bucket
    keys = s3_hook.list_keys(bucket_name=bucket_name)
    
    if not keys:
        print(f"No files found in MinIO bucket '{bucket_name}'.")
        return
        
    engine = pg_hook.get_sqlalchemy_engine()
    
    for key in keys:
        if key.endswith('.csv'):
            print(f"Reading {key} from MinIO...")
            
            # Get the file from MinIO
            file_obj = s3_hook.get_key(key=key, bucket_name=bucket_name)
            csv_content = file_obj.get()['Body'].read()
            
            # Read into pandas DataFrame
            df = pd.read_csv(io.BytesIO(csv_content))
            
            # Table name derived from filename (e.g., olist_customers_dataset.csv -> raw_olist_customers_dataset)
            table_name = 'raw_' + key.replace('.csv', '').replace('-', '_')
            
            print(f"Loading data into PostgreSQL table: {table_name}")
            df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
            print(f"Successfully loaded {len(df)} rows into {table_name}.")

with DAG('load_to_postgres', 
         default_args=default_args, 
         schedule_interval='@once', 
         catchup=False) as dag:

    load_task = PythonOperator(
        task_id='load_csvs_to_postgres',
        python_callable=load_data_to_postgres,
    )
