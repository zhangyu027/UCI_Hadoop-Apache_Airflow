from __future__ import annotations

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split


def main() -> None:
    spark = SparkSession.builder.appName("day3_word_count").getOrCreate()

    sentences = [
        ("hadoop stores data across machines",),
        ("spark processes data in memory",),
        ("airflow orchestrates data pipelines",),
        ("data engineering combines storage processing and orchestration",),
    ]

    df = spark.createDataFrame(sentences, ["sentence"])
    words = df.select(explode(split(col("sentence"), " ")).alias("word"))
    counts = words.groupBy("word").count().orderBy(col("count").desc(), col("word"))

    print("Word Count Results")
    counts.show(truncate=False)
    spark.stop()


if __name__ == "__main__":
    main()
