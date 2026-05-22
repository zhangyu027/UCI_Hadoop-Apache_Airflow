from __future__ import annotations

from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="kafka_dbt_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["kafka", "dbt"],
) as dag:
    check_dbt = BashOperator(
        task_id="check_dbt_version",
        bash_command="dbt --version",
    )

    run_dbt = BashOperator(
        task_id="run_dbt_project",
        bash_command="cd /opt/airflow/kafka_dbt_project && dbt run --profiles-dir /opt/airflow/.dbt",
    )

    check_dbt >> run_dbt
