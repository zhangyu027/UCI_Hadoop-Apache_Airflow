# Kafka + dbt Modern Data Engineering Project

This folder contains the dbt project and the Kafka/PostgreSQL demo scripts used by the Airflow pipeline in the sibling folder:

```text
../airflow_docker_compose_kafka_dbt
```

## Folder structure

```text
UCI_Hadoop_Apache_Airflow/
├── airflow_docker_compose_kafka_dbt/
└── kafka_dbt_project/
    ├── .dbt/
    │   └── profiles.yml
    ├── models/
    │   ├── sales_summary.sql
    │   └── schema.yml
    ├── producer.py
    ├── consumer.py
    ├── consumer2.py
    ├── dashboard.py
    ├── dbt_project.yml
    ├── docker-compose.yml
    ├── requirements.txt
    └── README.md
```

## What this project demonstrates

```text
Kafka Producer
    ↓
Kafka Topic
    ↓
Kafka Consumer
    ↓
PostgreSQL raw_sales table
    ↓
dbt sales_summary model
    ↓
Airflow DAG orchestration
    ↓
Optional Streamlit dashboard
```

## Important relationship with Airflow

The Airflow project mounts this folder with:

```yaml
- ../kafka_dbt_project:/opt/airflow/kafka_dbt_project
```

Inside the Airflow container, dbt runs from:

```bash
cd /opt/airflow/kafka_dbt_project
dbt debug --profiles-dir .dbt
dbt run --profiles-dir .dbt
dbt test --profiles-dir .dbt
```

## Start standalone Kafka and PostgreSQL

Run this only if you want to test Kafka and PostgreSQL from this folder directly:

```bash
cd ~/projects/UCI_Hadoop_Apache_Airflow/kafka_dbt_project
docker compose up -d
docker compose ps
```

## Install Python dependencies locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Create sample PostgreSQL table

```bash
docker exec -it kafka_dbt_project-postgres-1 psql -U postgres -d analytics
```

Then run:

```sql
create table if not exists raw_sales (
    user_id integer,
    event varchar(50),
    amount integer
);

insert into raw_sales (user_id, event, amount)
values
    (1, 'purchase', 100),
    (2, 'purchase', 200),
    (3, 'purchase', 300);

select * from raw_sales;
\q
```

## Run Kafka producer and consumer

Terminal 1:

```bash
python consumer2.py
```

Terminal 2:

```bash
python producer.py
```

The consumer inserts Kafka messages into PostgreSQL.

## Run dbt locally

```bash
dbt debug --profiles-dir .dbt
dbt run --profiles-dir .dbt
dbt test --profiles-dir .dbt
```

Expected output:

```text
Completed successfully
```

## Verify dbt output

```bash
docker exec -it kafka_dbt_project-postgres-1 psql -U postgres -d analytics
```

Then:

```sql
select * from sales_summary;
\q
```

## Run dashboard

```bash
streamlit run dashboard.py
```

## Stop standalone services

```bash
docker compose down
```

Use the Airflow folder if you want to run the orchestrated DAG:

```bash
cd ../airflow_docker_compose_kafka_dbt
docker compose up -d
```
