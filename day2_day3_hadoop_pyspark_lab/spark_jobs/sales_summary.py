
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, avg, rank
from pyspark.sql.window import Window
from pyspark.sql.functions import col
from pyspark.sql.functions import desc

spark = SparkSession.builder.appName("sales_summary").getOrCreate()

df = spark.read.csv("/home/jovyan/data/sales.csv", header=True, inferSchema=True)

print("Original Data")
df.show()

summary_df = df.groupBy("category").sum("sales")

print("Category Sales Summary")
summary_df.show()

filtered_df = df.filter(col("sales") > 100)

print("Filtered Sales > 100")
filtered_df.show()

window_spec = Window.orderBy(desc("sales"))

ranked_df = df.withColumn("sales_rank", rank().over(window_spec))

print("Window Function Ranking")
ranked_df.show()

spark.stop()
