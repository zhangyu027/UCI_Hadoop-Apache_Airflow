
from __future__ import annotations

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import logging

default_args = {
    "owner": "student",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

def extract():
    logging.info("Extract step started")
    print("Reading source data")

def transform():
    logging.info("Transform step started")
    print("Cleaning and transforming data")

def load():
    logging.info("Load step started")
    print("Loading data into warehouse")

with DAG(
    dag_id="daily_pipeline_dag",
    description="Day 4 Airflow ETL DAG",
    start_date=datetime(2026, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
    tags=["day4", "etl", "airflow"],
) as dag:

    task_extract = PythonOperator(
        task_id="extract_data",
        python_callable=extract,
    )

    task_transform = PythonOperator(
        task_id="transform_data",
        python_callable=transform,
    )

    task_load = PythonOperator(
        task_id="load_data",
        python_callable=load,
    )

    task_extract >> task_transform >> task_load
