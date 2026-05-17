from __future__ import annotations

from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="day6_api_spark_postgres_etl",
    description="API ingestion -> Spark cleaning -> PostgreSQL warehouse",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["day6", "spark", "api", "postgres", "etl"],
) as dag:

    check_services = BashOperator(
        task_id="check_services",
        bash_command="""
        python - <<'PY'
import requests
resp = requests.get("http://mock-api:8000/sales_events.json", timeout=10)
print("API status:", resp.status_code)
print("Payload length:", len(resp.text))
resp.raise_for_status()
PY
        """,
    )

    run_spark_etl = BashOperator(
        task_id="run_spark_etl",
        bash_command="python /opt/airflow/spark_jobs/api_to_postgres_spark.py",
    )

    verify_warehouse_tables = BashOperator(
        task_id="verify_warehouse_tables",
        bash_command="""
        python - <<'PY'
import psycopg2
conn = psycopg2.connect(host="warehouse-postgres", database="warehouse", user="postgres", password="postgres", port=5432)
cur = conn.cursor()
for table in ["cleaned_sales_events", "daily_sales_summary"]:
    cur.execute(f"SELECT COUNT(*) FROM {table};")
    print(table, "row_count =", cur.fetchone()[0])
cur.close()
conn.close()
PY
        """,
    )

    check_services >> run_spark_etl >> verify_warehouse_tables
