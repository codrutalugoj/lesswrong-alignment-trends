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
    'JSON_to_DB', 
    default_args=default_args,
    description="Pulls the latest JSON data from S3 and writes it to a Postgres database",
    schedule=timedelta(days=1),  # Adjust the schedule interval as needed
)

def run_s3_to_database():
    path = "/opt/airflow/elt/s3_to_database.py" 
    result = subprocess.run(["python", path], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Loading data from S3 failed: {result.stderr}")
    else:
        print(result.stdout)
    
# Task 3: Load from AWS S3
load_from_s3 = PythonOperator(
    task_id='load_from_s3',
    python_callable=run_s3_to_database,
    dag=dag,
)

# Task 4: Transform the table with dbt
dbt = BashOperator(
    task_id='dbt_transformation',
    bash_command="cd ./lesswrong && dbt run",
    dag=dag,
)

load_from_s3 >> dbt