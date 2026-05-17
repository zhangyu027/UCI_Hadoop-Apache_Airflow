import json
import os
from pathlib import Path

import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, round as spark_round, sum as spark_sum, count as spark_count

API_URL = os.getenv("API_URL", "http://mock-api:8000/sales_events.json")
RAW_PATH = Path("/opt/airflow/data/raw/sales_events.json")

SPARK_MASTER = os.getenv("SPARK_MASTER", "spark://spark-master:7077")
WAREHOUSE_JDBC_URL = os.getenv("WAREHOUSE_JDBC_URL", "jdbc:postgresql://warehouse-postgres:5432/warehouse")
WAREHOUSE_USER = os.getenv("WAREHOUSE_USER", "postgres")
WAREHOUSE_PASSWORD = os.getenv("WAREHOUSE_PASSWORD", "postgres")

print(f"Downloading API data from: {API_URL}")
response = requests.get(API_URL, timeout=20)
response.raise_for_status()

RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
payload = response.json()
RAW_PATH.write_text(json.dumps(payload, indent=2))
print(f"Wrote raw API payload to {RAW_PATH}")

spark = (
    SparkSession.builder
    .appName("Day6_API_Spark_Postgres_ETL")
    .master(SPARK_MASTER)
    .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3")
    .getOrCreate()
)

raw_df = spark.read.option("multiline", "true").json(str(RAW_PATH))

print("Raw API data:")
raw_df.show(truncate=False)

clean_df = (
    raw_df
    .dropna(subset=["order_id", "customer_id", "event", "amount", "event_date"])
    .filter(col("amount") > 0)
    .withColumn("amount", spark_round(col("amount").cast("double"), 2))
    .withColumn("ingested_at", current_timestamp())
)

print("Cleaned data:")
clean_df.show(truncate=False)

summary_df = (
    clean_df
    .groupBy("event_date", "event")
    .agg(
        spark_count("*").alias("total_events"),
        spark_sum("amount").alias("total_amount"),
    )
    .orderBy("event_date", "event")
)

jdbc_props = {
    "user": WAREHOUSE_USER,
    "password": WAREHOUSE_PASSWORD,
    "driver": "org.postgresql.Driver",
}

clean_df.write.mode("overwrite").jdbc(
    url=WAREHOUSE_JDBC_URL,
    table="public.cleaned_sales_events",
    properties=jdbc_props,
)

summary_df.write.mode("overwrite").jdbc(
    url=WAREHOUSE_JDBC_URL,
    table="public.daily_sales_summary",
    properties=jdbc_props,
)

print("Wrote PostgreSQL tables:")
print(" - public.cleaned_sales_events")
print(" - public.daily_sales_summary")

spark.stop()
