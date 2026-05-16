import argparse
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType


def build_spark(app_name: str) -> SparkSession:
    return (
        SparkSession.builder
        .appName(app_name)
        .getOrCreate()
    )


def load_input(spark: SparkSession, input_path: str):
    input_path = input_path.lower()
    if input_path.endswith(".csv"):
        return spark.read.option("header", True).csv(input_path)
    if input_path.endswith(".json"):
        return spark.read.json(input_path)
    raise ValueError("Unsupported input format. Use CSV or JSON.")


def main() -> None:
    parser = argparse.ArgumentParser(description="PySpark ETL for NLP training data.")
    parser.add_argument("--input", required=True, help="Raw CSV or JSON with text,label columns")
    parser.add_argument("--output_dir", required=True, help="Directory to write Parquet splits")
    args = parser.parse_args()

    spark = build_spark("PySparkTextETL")
    df = load_input(spark, args.input)

    required = {"text", "label"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    cleaned = (
        df.select("text", "label")
        .dropna(subset=["text", "label"])
        .withColumn("text", F.trim(F.col("text")))
        .filter(F.length("text") > 0)
        .withColumn("text", F.lower("text"))
        .withColumn("text", F.regexp_replace("text", r"[^a-z0-9\s]", " "))
        .withColumn("text", F.regexp_replace("text", r"\s+", " "))
        .withColumn("label", F.col("label").cast(IntegerType()))
        .dropDuplicates(["text", "label"])
    )

    # Random split for demo purposes.
    train_df, valid_df, test_df = cleaned.randomSplit([0.7, 0.15, 0.15], seed=42)

    output_dir = Path(args.output_dir)
    train_path = str(output_dir / "train.parquet")
    valid_path = str(output_dir / "valid.parquet")
    test_path = str(output_dir / "test.parquet")

    train_df.write.mode("overwrite").parquet(train_path)
    valid_df.write.mode("overwrite").parquet(valid_path)
    test_df.write.mode("overwrite").parquet(test_path)

    print(f"Train rows: {train_df.count()}")
    print(f"Valid rows: {valid_df.count()}")
    print(f"Test rows: {test_df.count()}")
    print(f"Wrote Parquet splits to: {output_dir}")

    spark.stop()


if __name__ == "__main__":
    main()
