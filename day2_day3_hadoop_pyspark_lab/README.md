
# Day 2 — Hadoop + HDFS Foundations

## Topics

- HDFS Architecture
- NameNode / DataNode
- Replication
- Block Storage
- Distributed Storage Concepts

## Start Hadoop

```bash
docker compose up -d
```

## HDFS Commands

```bash
docker exec -it day2-hadoop bash

hdfs dfs -mkdir /data
hdfs dfs -put sample.csv /data
hdfs dfs -ls /data
```

## Assignment

Reflection:

Why distributed storage matters?

---

# Day 3 — PySpark Fundamentals

## Topics

- Spark Architecture
- Driver / Executor
- Lazy Evaluation
- DataFrame API
- Transformations vs Actions

## Start PySpark Notebook

Open:

http://127.0.0.1:8888

## Run PySpark Script

```bash
docker exec -it day3-pyspark bash

python /home/jovyan/work/sales_summary.py
```

## Students Practice

- Filtering
- Aggregations
- Joins
- Window Functions
