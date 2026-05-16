
# Kafka + dbt Modern Data Engineering Project

## Stack
- Kafka
- PostgreSQL
- dbt
- Docker Compose
- Python

## Run Environment

```bash
docker compose up -d
```
docker compose down
docker compose up -d
```
docker ps
```
## Run Producer

```bash
python producer.py
```
python3.10 consumer.py
```
## Run Consumer

```bash
python3.10 consumer.py
```

```
STEP 1 — Create PostgreSQL Table
```
docker exec -it kafka_dbt_project-postgres-1 psql -U postgres -d analytics
```
CREATE TABLE raw_sales (
    user_id INT,
    event VARCHAR(50),
    amount INT
);
```
\d
```
\q
```
STEP 2 — Upgrade Consumer
```
STEP 3 — Rerun Consumer
```
python3.10 consumer2.py
```
STEP 4 - Run producer again 
```
python3.10 producer.py
```
STEP 5 — Verify Data Exists
```
docker exec -it kafka_dbt_project-postgres-1 psql -U postgres -d analytics
SELECT * FROM raw_sales;
```
STEP 6 - RUN dbt
## Run dbt

```bash
dbt run
dbt test
```
Producer
   ↓
Kafka
   ↓
Consumer
   ↓
PostgreSQL
   ↓
dbt Models
   ↓
Analytics Tables
```
docker exec -it kafka_dbt_project-postgres-1 psql -U postgres -d analytics
```
SELECT * FROM sales_summary;
```
mkdir -p ~/.dbt

cat > ~/.dbt/profiles.yml <<'EOF'
default:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: postgres
      password: postgres
      port: 5432
      dbname: analytics
      schema: public
      threads: 1
EOF
```
ls -l ~/.dbt
cat ~/.dbt/profiles.yml
```
dbt debug
```
Kafka Producer
      ↓
Kafka Topic
      ↓
Consumer
      ↓
PostgreSQL
      ↓
dbt
      ↓
Analytics Tables
      ↓
Airflow DAG
      ↓
Dashboard
```
mkdir -p dags
```
nano dags/kafka_dbt_pipeline_dag.py
```
ls dags
```
docker ps
```
docker inspect airflow_etl_weather_cd08ca-scheduler-1
```
http://localhost:8081
```
docker ps
```
docker compose up -d
```
run_dbt_models
```
Logs
```
Completed successfully
```check_project_files ✅
run_dbt_models ✅
test_dbt_models ⏳

and the DAG summary already shows:

Total success: 2

That means:

Airflow is working
Docker containers are working
dbt is connecting to PostgreSQL
profiles.yml is fixed
your dbt model compiled successfully
sales_summary was created successfully

The only remaining task is test_dbt_models, and it is likely still running or about to finish.

Wait ~5–10 seconds and refresh.

You should soon see:

test_dbt_models ✅

Then your whole pipeline is complete.

You have now successfully integrated:

Airflow
Kafka
PostgreSQL
dbt
Docker Compose

into one working pipeline.

Future errors can still happen (normal in data engineering), but the major architecture/configuration problems are now solved:

Kafka broker issue ✅
Airflow DAG issue ✅
Docker networking issue ✅
dbt profiles issue ✅
PostgreSQL connection issue ✅
Missing table issue ✅

Your system is now in a stable state.
```
(base) mac:kafka_dbt_project yuzhang$ docker exec -it kafka_dbt_project-postgres-1 psql -U postgres -d analytics
psql (15.18 (Debian 15.18-1.pgdg13+1))
Type "help" for help.

analytics=# CREATE TABLE IF NOT EXISTS raw_sales (
    user_id INT,
    event VARCHAR(50),
    amount INT
);

INSERT INTO raw_sales (user_id, event, amount)
VALUES
(1, 'purchase', 100),
(2, 'purchase', 200),
(3, 'purchase', 300);
CREATE TABLE
INSERT 0 3
analytics=# \dt
           List of relations
 Schema |   Name    | Type  |  Owner   
--------+-----------+-------+----------
 public | raw_sales | table | postgres
(1 row)

analytics=# SELECT * FROM raw_sales;
 user_id |  event   | amount 
---------+----------+--------
       1 | purchase |    100
       2 | purchase |    200
       3 | purchase |    300
(3 rows)
```
