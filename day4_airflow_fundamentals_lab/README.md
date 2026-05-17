
# Day 4 — Apache Airflow Fundamentals Lab

## Goal

Teach orchestration properly using Apache Airflow.

## Topics

- DAGs
- Scheduling
- Retries
- Operators
- Dependencies
- Execution Flow

## Start Airflow

```bash
docker compose up -d
```

Open:

http://127.0.0.1:8083

Login:

admin / admin

## DAG

Students build:

daily_pipeline_dag.py

Task flow:

extract_data
   ↓
transform_data
   ↓
load_data

## Practice

- Trigger DAG manually
- Clear failed tasks
- View Logs
- Add retries
- Add logging

## Useful Commands

```bash
docker ps
docker compose down
docker compose up -d
```
