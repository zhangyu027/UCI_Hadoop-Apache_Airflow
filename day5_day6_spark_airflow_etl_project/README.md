# Day 5–6 Spark + Airflow + PostgreSQL ETL Project

This project supports:

- Day 5: Docker + Spark + Airflow Integration
- Day 6: Real ETL Pipeline Project

## Architecture

```text
Mock API
   ↓
Airflow DAG
   ↓
Spark ETL Job
   ↓
PostgreSQL Warehouse
   ↓
Verification Query
```

## Services

| Service | Purpose | URL / Port |
|---|---|---|
| Airflow | Orchestration | http://127.0.0.1:8082 |
| Spark Master UI | Spark monitoring | http://127.0.0.1:8085 |
| Mock API | Static API endpoint | http://127.0.0.1:8000/sales_events.json |
| PostgreSQL Warehouse | ETL target database | localhost:5434 |

## Step 1 — Start Docker Desktop

Make sure Docker Desktop is running.

## Step 2 — Start the project

From this folder:

```bash
docker compose up --build -d
```

Wait 60–90 seconds.

## Step 3 — Open Airflow

Open:

```text
http://127.0.0.1:8082
```

Login:

```text
username: admin
password: admin
```

## Step 4 — Trigger the DAG

Find:

```text
day6_api_spark_postgres_etl
```

Turn it ON, then click the play button to trigger it.

Expected task flow:

```text
check_services
   ↓
run_spark_etl
   ↓
verify_warehouse_tables
```

## Step 5 — Check PostgreSQL output

```bash
docker exec -it day56-warehouse-postgres psql -U postgres -d warehouse
```

Inside psql:

```sql
\dt
SELECT * FROM cleaned_sales_events;
SELECT * FROM daily_sales_summary;
\q
```

## Step 6 — Check Spark UI

Open:

```text
http://127.0.0.1:8085
```

## Day 5 Teaching Flow

Topics:

- Docker Compose services
- Docker networks
- Docker volumes
- Airflow orchestration
- Spark job execution
- PostgreSQL warehouse service

Live coding:

```python
BashOperator(
    task_id="run_spark_etl",
    bash_command="python /opt/airflow/spark_jobs/api_to_postgres_spark.py",
)
```

## Day 6 Teaching Flow

Topics:

- API ingestion
- Spark data cleaning
- PostgreSQL warehouse loading
- production pipeline design

Pipeline:

```text
API → Spark Cleaning → PostgreSQL → Airflow DAG
```

## Common Debug Commands

```bash
docker ps
docker logs day56-airflow-scheduler --tail 80
docker logs day56-airflow-webserver --tail 80
docker logs day56-spark-master --tail 80
docker logs day56-warehouse-postgres --tail 80
```

## Stop

```bash
docker compose down
```

Reset all databases:

```bash
docker compose down -v
```
