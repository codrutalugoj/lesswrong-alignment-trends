FROM apache/airflow:latest

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip install apache-airflow-providers-docker dbt-core dbt-postgres

RUN pip install -r requirements.txt 
