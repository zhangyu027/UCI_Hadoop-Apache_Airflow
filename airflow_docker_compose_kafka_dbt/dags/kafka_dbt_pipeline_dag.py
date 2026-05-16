from __future__ import annotations

from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_DIR = "/opt/airflow/kafka_dbt_project"

with DAG(
    dag_id="kafka_dbt_pipeline",
    description="Run dbt models and tests after Kafka demo data is loaded",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["kafka", "dbt", "modern-data-engineering"],
) as dag:

    check_project_files = BashOperator(
        task_id="check_project_files",
        bash_command=f"ls -la {PROJECT_DIR} && ls -la {PROJECT_DIR}/models",
    )

    run_dbt_models = BashOperator(
        task_id="run_dbt_models",
        bash_command=f"cd {PROJECT_DIR} && dbt run --profiles-dir {PROJECT_DIR}/.dbt",
    )

    test_dbt_models = BashOperator(
        task_id="test_dbt_models",
        bash_command=f"cd {PROJECT_DIR} && dbt test --profiles-dir {PROJECT_DIR}/.dbt",
    )

    check_project_files >> run_dbt_models >> test_dbt_models
