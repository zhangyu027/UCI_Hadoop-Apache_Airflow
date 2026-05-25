from __future__ import annotations

from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


CHECK_SERVICES_COMMAND = dedent(
    """
    python - <<'PY'
    import os
    import requests
    import psycopg2

    api_url = os.getenv("API_URL", "http://mock-api:8000/sales_events.json")
    response = requests.get(api_url, timeout=20)
    response.raise_for_status()
    print(f"API OK: {api_url}")

    conn = psycopg2.connect(
        host="warehouse-postgres",
        port=5432,
        dbname="warehouse",
        user="postgres",
        password="postgres",
    )
    conn.close()
    print("Warehouse PostgreSQL OK")
    PY
    """
).strip()


VERIFY_WAREHOUSE_COMMAND = dedent(
    """
    python - <<'PY'
    import psycopg2

    conn = psycopg2.connect(
        host="warehouse-postgres",
        port=5432,
        dbname="warehouse",
        user="postgres",
        password="postgres",
    )
    cur = conn.cursor()

    for table in ["cleaned_sales_events", "daily_sales_summary"]:
        cur.execute(f"select count(*) from public.{table};")
        count = cur.fetchone()[0]
        print(f"{table}: {count} rows")
        if count == 0:
            raise RuntimeError(f"{table} is empty")

    cur.close()
    conn.close()
    print("Warehouse verification passed")
    PY
    """
).strip()


with DAG(
    dag_id="day6_api_spark_postgres_etl",
    description="Mock API to Spark to PostgreSQL warehouse ETL pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["day5", "day6", "spark", "postgres", "etl"],
) as dag:
    check_services = BashOperator(
        task_id="check_services",
        bash_command=CHECK_SERVICES_COMMAND,
    )

    run_spark_etl = BashOperator(
        task_id="run_spark_etl",
        bash_command="python /opt/airflow/spark_jobs/api_to_postgres_spark.py",
    )

    verify_warehouse_tables = BashOperator(
        task_id="verify_warehouse_tables",
        bash_command=VERIFY_WAREHOUSE_COMMAND,
    )

    check_services >> run_spark_etl >> verify_warehouse_tables
