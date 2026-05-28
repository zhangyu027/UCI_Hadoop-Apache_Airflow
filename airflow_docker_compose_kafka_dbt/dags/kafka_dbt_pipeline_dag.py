from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

DBT_PROJECT_DIR = "/opt/airflow/kafka_dbt_project"
DBT_PROFILES_DIR = "/opt/airflow/kafka_dbt_project/.dbt"

with DAG(
    dag_id="kafka_dbt_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    dbt_debug = BashOperator(
        task_id="dbt_debug",
        bash_command=f'''
        cd {DBT_PROJECT_DIR} &&
        dbt debug --profiles-dir {DBT_PROFILES_DIR}
        '''
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f'''
        cd {DBT_PROJECT_DIR} &&
        dbt run --profiles-dir {DBT_PROFILES_DIR}
        '''
    )

    dbt_debug >> dbt_run