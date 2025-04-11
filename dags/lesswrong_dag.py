from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import subprocess
import logging

logger = logging.getLogger(__name__)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'LessWrong-Trends', 
    default_args=default_args,
    description="LessWrong ETL",
    schedule=timedelta(days=1),  # Adjust the schedule interval as needed
)

# ETL workflow
# What we want this DAG to do:
# 1. run the scraper.py to collect LessWrong data into a JSON file
# 2. upload the JSON to the AWS S3 bucket
# 3. 

# 1: Extract/Scrape data
def run_scraper():
    path = "/opt/airflow/elt/scraper.py" 
    result = subprocess.run(["python", path], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Scraping failed with error: {result.stderr}")
    else:
        print(result.stdout)

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=run_scraper,
    dag=dag,
)

# Task 2: Load data to AWS S3
def run_json_to_s3():
    path = "/opt/airflow/elt/json_to_s3.py" 
    result = subprocess.run(["python", path], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Uploading JSON to S3 failed with error: {result.stderr}")
    else:
        print(result.stdout)
    

load_task = PythonOperator(
    task_id='load_data',
    python_callable=run_json_to_s3,
    dag=dag,
)

def run_s3_to_database():
    path = "/opt/airflow/elt/s3_to_database.py" 
    result = subprocess.run(["python", path], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Loading data from S3 failed: {result.stderr}")
    else:
        logger.info(result)
        print(result.stdout)
    
# Task 3: Load from AWS S3
load_from_s3 = PythonOperator(
    task_id='load_from_s3',
    python_callable=run_s3_to_database,
    dag=dag,
)

# Task 4: Transform
# transform_task = BashOperator(
#     task_id='dbt_transform',
#     bash_command="dbt run --project-dir /app/dbt --profiles-dir /root/.dbt --full-refresh",
#     dag=dag,
# )

extract_task >> load_task >> load_from_s3