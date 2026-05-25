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
    │   ├── profit_summary.sql
    │   ├── product_profit_analysis.sql
    │   ├── yearly_profit_trends.sql
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

### Original Flow
```text
Kafka Producer (sales_topic)
    ↓
Kafka Consumer
    ↓
PostgreSQL raw_sales table
    ↓
dbt sales_summary model
```

### Enhanced Flow (with Annual Profit Data)
```text
Kafka Producer (dual topics)
├── sales_topic → raw_sales table
└── profit_events → raw_profit_events table
    ↓
Multiple dbt models:
├── sales_summary (event aggregation)
├── profit_summary (annual profit by category & year)
├── product_profit_analysis (product-level metrics)
└── yearly_profit_trends (year-over-year comparison)
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
-- View sales summary
select * from sales_summary;

-- View profit summary (annual profit by category and year)
select * from profit_summary;

-- View product-level profit analysis
select * from product_profit_analysis order by total_profit desc;

-- View year-over-year profit trends
select * from yearly_profit_trends order by year desc, annual_profit desc;

-- View raw profit events
select * from raw_profit_events limit 10;

\q
```

## New Data: Annual Profit Analysis

The producer now generates profit data in addition to sales events:

### Profit Event Fields
- `product_id` - Unique identifier for the product
- `product_name` - Name of the product
- `category` - Product category (Electronics, Clothing, Home, Food)
- `year` - Calendar year (2023, 2024, 2025)
- `quantity` - Units sold in transaction
- `revenue` - Total revenue (price × quantity)
- `cost` - Total cost of goods sold
- `profit` - Net profit (revenue - cost)
- `profit_margin` - Profit margin percentage

### New dbt Models

**profit_summary**: Annual aggregates by category and year
- Total transactions and quantity
- Revenue, cost, and profit totals
- Average and overall profit margins

**product_profit_analysis**: Product-level metrics across all time
- Transaction count and total quantities
- Revenue and profit by product
- Min, max, and average profit margins

**yearly_profit_trends**: Year-over-year comparison by category
- Annual revenue, cost, and profit
- Profit margin percentage trends
- Track business growth across years



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
