from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime
import os

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
}

def upload_to_minio():
    # 'minio_conn' must be created in Airflow Connections:
    # Conn Id: minio_conn
    # Conn Type: Amazon S3
    # Extra: {"endpoint_url": "http://minio:9000", "aws_access_key_id": "admin", "aws_secret_access_key": "password"}
    s3_hook = S3Hook(aws_conn_id='minio_conn')
    bucket_name = 'raw-data'
    
    # Ensure bucket exists
    if not s3_hook.check_for_bucket(bucket_name):
        s3_hook.create_bucket(bucket_name=bucket_name)

    data_dir = '/opt/airflow/data'
    
    files_uploaded = 0
    # Iterate over files in the data directory
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                key = f"{file}"
                
                print(f"Uploading {file_path} to s3://{bucket_name}/{key}")
                s3_hook.load_file(
                    filename=file_path,
                    key=key,
                    bucket_name=bucket_name,
                    replace=True
                )
                files_uploaded += 1
                
    if files_uploaded == 0:
        print("No CSV files found in /opt/airflow/data. Please add Olist dataset CSVs to the ./data folder.")

with DAG('ingest_to_minio', 
         default_args=default_args, 
         schedule_interval='@once', 
         catchup=False) as dag:

    upload_task = PythonOperator(
        task_id='upload_csvs_to_minio',
        python_callable=upload_to_minio,
    )
