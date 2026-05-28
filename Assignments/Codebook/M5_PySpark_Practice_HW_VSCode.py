"""
VS Code Runnable PySpark Practice Script
"""

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("PySparkPractice").getOrCreate()

# ##**Step 1**: Install Spark

# ##**Step 2**: Setting up Spark
# 
# Before you can connect to a Spark cluster, Spark needs to be installed. The code below is boilerplate code that can be used to set-up Spark. Please note that this code will be leveraged in all the notebooks since each nodebook is a separate entity.

# ## **Step 3**. Import the lib

# Colab-friendly setup for PySpark
!apt-get install -y openjdk-11-jdk-headless -qq > /dev/null
!pip install -q "pyspark[connect]==3.5.1" "dataproc-spark-connect==0.8.3"

import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"

from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").appName("RDDPractice").getOrCreate()
sc = spark.sparkContext

# ## **Step 4**: Using DataFrames
# 
# Spark's core data structure is the Resilient Distributed Dataset (RDD), which is a low-level object designed to handle large datasets by distributing data across multiple nodes in a cluster. However, working directly with RDDs can be challenging. To simplify this, Spark provides DataFrames, which offer a higher-level abstraction built on top of RDDs.
# 
# A Spark DataFrame functions similarly to a SQL table, where columns represent attributes and rows represent observations. DataFrames not only make it easier to manipulate and analyze data, but they are also more optimized for complex operations compared to RDDs.

## mount to google drive
from google.colab import drive
drive.mount('/content/drive')

# Read the Airlines.csv file from your Google Drive into a Spark DataFrame

## Read RDD
df = spark.read.option("header", "true").csv("/content/drive/MyDrive/Colab Notebooks/UCI/UCI_425.07_Big_Data_Analytics/Assignments/Dataset/airline.csv")
df.show(100)

# Output the column names and the "rows" and "column" counts

#outputing the column names
df.columns #Column Names

#Outputing the row count
df.count()  #Row Count
#Output the column count
len(df.columns) #Column Count

df.dtypes

# In order to examine the summary of any particular column of a DataFrame, we use the describe method.
# 
# The describe "method" gives us the statistical summary of the given column

#Examine the summary of the "DepDelay" column
df.describe('DepDelay').show()

# In order to select particular columns from the DataFrame, use the select method

df.select('ArrDelay','DepDelay').show()

# Selecting Distinct Multiple Columns

df.select('ArrDelay','DepDelay').distinct().show()

# ## **Step 5.** Filtering Data

df.filter(df.Origin=='SFO').show()

# Filtering Data (Multiple Parameters)

df.filter((df.Origin=='SFO')&(df.Dest=='PDX')).show()

# ## **Step 6**: Performing SQL Queries
# - SQL queries can be passes directly to any DataFrame; for that, we need to create a table from the DataFrame using the registerTempTable

# old (deprecated)
# df.registerTempTable('airlines')

# new (Spark 2.0+)
df.createOrReplaceTempView("airlines")

# Typically the entry point into all SQL functionality in Spark is the SQLContext class. To create a basic instance of this call, all we need is a SparkContext reference.

from pyspark.sql import SQLContext
sqlContext = SQLContext(spark)
sqlContext

sqlContext.sql('select * from airlines').show()

sqlContext.sql('select distinct(Dest) from airlines').show(20)

print(df.count())

print(df.take(3))



## Filter#3
spark.sql("""SELECT DISTINCT Origin, Dest, Distance
FROM airlines WHERE distance > 1000
ORDER BY distance DESC""").show(10)

# ## **Step 7**: Aggregation

## aggregation
spark.sql("""SELECT concat(Origin, Dest) as market,
avg(Distance)
FROM airlines
GROUP BY 1
ORDER BY 1 DESC""").show(10)

## aggregation
spark.sql("""SELECT concat(Origin, Dest) as market,
min(Distance)
FROM airlines
GROUP BY 1
ORDER BY 1 DESC""").show(10)

## Top 10
## "SFOSMF" 86 actually is "860" due to the bugs of pyspark show function
spark.sql("""SELECT concat(Origin, Dest) as market,
max(Distance)
FROM airlines
GROUP BY 1
ORDER BY max(Distance) DESC
limit 10""").show(10)


# Stop Spark session
spark.stop()