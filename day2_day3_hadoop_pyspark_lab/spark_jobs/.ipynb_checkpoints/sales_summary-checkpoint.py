from __future__ import annotations

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, desc, rank, sum as spark_sum
from pyspark.sql.window import Window


def main() -> None:
    spark = SparkSession.builder.appName("day3_sales_summary").getOrCreate()

    input_path = "/home/jovyan/data/sales.csv"
    df = spark.read.csv(input_path, header=True, inferSchema=True)

    print("Original Data")
    df.show(truncate=False)
    df.printSchema()

    category_summary = (
        df.groupBy("category")
        .agg(
            spark_sum("sales").alias("total_sales"),
            avg("sales").alias("average_sales"),
        )
        .orderBy(desc("total_sales"))
    )

    print("Category Sales Summary")
    category_summary.show(truncate=False)

    high_sales = df.filter(col("sales") > 100).orderBy(desc("sales"))
    print("Filtered Sales > 100")
    high_sales.show(truncate=False)

    window_spec = Window.orderBy(desc("sales"))
    ranked_sales = df.withColumn("sales_rank", rank().over(window_spec))
    print("Window Function Ranking")
    ranked_sales.show(truncate=False)

    output_path = "/home/jovyan/data/output/category_sales_summary"
    (
        category_summary
        .coalesce(1)
        .write
        .mode("overwrite")
        .option("header", True)
        .csv(output_path)
    )

    print(f"Wrote category summary to: {output_path}")
    spark.stop()


if __name__ == "__main__":
    main()
