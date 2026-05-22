from __future__ import annotations

import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    "owner": "student",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}


def extract() -> None:
    """Simulate extracting source data."""
    logging.info("Extract step started")
    logging.info("Reading source data")


def transform() -> None:
    """Simulate transforming source data."""
    logging.info("Transform step started")
    logging.info("Cleaning and transforming data")


def load() -> None:
    """Simulate loading transformed data into a warehouse."""
    logging.info("Load step started")
    logging.info("Loading data into warehouse")


with DAG(
    dag_id="daily_pipeline_dag",
    description="Day 4 Airflow ETL DAG",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=["day4", "etl", "airflow"],
) as dag:
    extract_data = PythonOperator(
        task_id="extract_data",
        python_callable=extract,
    )

    transform_data = PythonOperator(
        task_id="transform_data",
        python_callable=transform,
    )

    load_data = PythonOperator(
        task_id="load_data",
        python_callable=load,
    )

    extract_data >> transform_data >> load_data
