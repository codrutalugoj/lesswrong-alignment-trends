from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from scraper import scrape_lw
from json_to_s3 import upload_json

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'LessWrong-Trends', 
    default_args=default_args,
    description="LessWrong ETL",
    schedule=timedelta(days=0),  # Adjust the schedule interval as needed
)

# ETL workflow
# What we want this DAG to do:
# 1. run the scraper.py to collect LessWrong data into a JSON file
# 2. upload the JSON to the AWS S3 bucket
# 3. 

# 1: Extract/Scrape data
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=scrape_lw,
    dag=dag,
)

# # 2: Transform
# transform_task = PythonOperator(
#     task_id='transform_data',
#     python_callable=scrape_lw,
#     dag=dag,
# )

# Task 3: Load data
load_task = PythonOperator(
    task_id='load_data',
    python_callable=upload_json,
    dag=dag,
)

extract_task >> load_task 