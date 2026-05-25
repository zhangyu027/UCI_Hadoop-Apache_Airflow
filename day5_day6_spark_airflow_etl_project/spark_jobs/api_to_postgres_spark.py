from __future__ import annotations

import json
import os
from pathlib import Path

import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count as spark_count, current_timestamp
from pyspark.sql.functions import round as spark_round
from pyspark.sql.functions import sum as spark_sum


API_URL = os.getenv("API_URL", "http://mock-api:8000/sales_events.json")
RAW_PATH = Path("/opt/airflow/data/raw/sales_events.json")
SPARK_MASTER = os.getenv("SPARK_MASTER", "local[*]")
WAREHOUSE_JDBC_URL = os.getenv(
    "WAREHOUSE_JDBC_URL",
    "jdbc:postgresql://warehouse-postgres:5432/warehouse",
)
WAREHOUSE_USER = os.getenv("WAREHOUSE_USER", "postgres")
WAREHOUSE_PASSWORD = os.getenv("WAREHOUSE_PASSWORD", "postgres")
POSTGRES_JAR = "/opt/airflow/jars/postgresql-42.7.3.jar"


def download_api_payload() -> None:
    print(f"Downloading API data from: {API_URL}")
    response = requests.get(API_URL, timeout=20)
    response.raise_for_status()

    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_PATH.write_text(json.dumps(response.json(), indent=2))
    print(f"Wrote raw API payload to {RAW_PATH}")


def build_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName("Day6_API_Spark_Postgres_ETL")
        .master(SPARK_MASTER)
        .config("spark.jars", POSTGRES_JAR)
        .getOrCreate()
    )


def main() -> None:
    download_api_payload()

    spark = build_spark_session()

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


if __name__ == "__main__":
    main()
