
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
Step 1: Start Kafka/Postgres
Step 2: Run producer.py
Step 3: Confirm raw_sales table
Step 4: Trigger Airflow DAG
Step 5: dbt creates sales_summary
Step 6: dbt test validates model
```
cd ~/projects/UCI_Hadoop-Apache_Airflow
git status
git add kafka_dbt_project airflow_docker_compose_kafka_dbt
git commit -m "Add Kafka dbt Airflow pipeline"
git push
```
Day 8 add the pyspark stream and dashboard
```
1. Explain architecture
2. Show producer.py
3. Show Airflow DAG
4. Show dbt transformation
5. Show debugging issues you solved
6. Show Streamlit dashboard
7. Discuss scaling + production improvements
```
cd ~/projects/UCI_Hadoop-Apache_Airflow
```
nano .gitignore
```
logs/
target/
__pycache__/
*.log
.env
```
CTRL + O
ENTER
CTRL + X
```
git rm -r --cached airflow_docker_compose_kafka_dbt/logs
git rm -r --cached kafka_dbt_project/target
```
git status
```
git add .gitignore
git commit -m "Remove generated logs and dbt target files"
```
git push
```
git status
```
Day5-Day6
```
perl -pi -e 's/bitnami\/spark:3\.5/bitnami\/spark:3.5.1/g' docker-compose.yml
```
docker compose down -v
docker compose up --build -d
```
docker exec -it day56-warehouse-postgres psql -U postgres -d warehouse
```
\dt
SELECT * FROM cleaned_sales_events;
SELECT * FROM daily_sales_summary;
```
warehouse=# \dt
                List of relations
 Schema |         Name         | Type  |  Owner   
--------+----------------------+-------+----------
 public | cleaned_sales_events | table | postgres
 public | daily_sales_summary  | table | postgres
(2 rows)

```
echo "logs/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.log" >> .gitignore
```
git add .gitignore
git commit -m "Update gitignore for generated files"
git push
````
day2_day3_hadoop_pyspark_lab
```
python /home/jovyan/work/sales_summary.py
```
pip uninstall -y pyspark py4j
pip install pyspark==3.5.1
```
exit
docker compose down
docker compose up -d
```
+-------+-----------+-----+----------+
|product|   category|sales|sales_rank|
+-------+-----------+-----+----------+
| Laptop|Electronics| 1200|         1|
|  Phone|Electronics|  800|         2|
|   Desk|  Furniture|  300|         3|
|  Chair|  Furniture|  150|         4|
|   Book|      Books|   40|         5|
+-------+-----------+-----+----------+

```