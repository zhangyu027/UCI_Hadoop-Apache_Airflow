from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

PROJECT_DIR = "/Users/yuzhang/projects/UCI_Hadoop-Apache_Airflow/kafka_dbt_project"

with DAG(
    dag_id="kafka_dbt_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["kafka", "dbt", "data-engineering"],
) as dag:

    run_producer = BashOperator(
        task_id="run_kafka_producer",
        bash_command=f"cd {PROJECT_DIR} && python3.10 producer.py",
    )

    run_dbt = BashOperator(
        task_id="run_dbt_models",
        bash_command=f"cd {PROJECT_DIR} && dbt run",
    )

    test_dbt = BashOperator(
        task_id="test_dbt_models",
        bash_command=f"cd {PROJECT_DIR} && dbt test",
    )

    run_producer >> run_dbt >> test_dbt
