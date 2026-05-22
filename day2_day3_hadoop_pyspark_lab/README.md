# Day 2–3 Hadoop + PySpark Lab

This fixed version uses a custom `Dockerfile.pyspark` so PySpark is installed every time.

## Start

```bash
cd ~/projects/UCI_Hadoop_Apache_Airflow/day2_day3_hadoop_pyspark_lab
docker compose down --remove-orphans
docker rm -f day3-pyspark day2-hadoop 2>/dev/null || true
docker compose build --no-cache
docker compose up -d
```

## Test PySpark

```bash
docker exec -it day3-pyspark bash
python -c "from pyspark.sql import SparkSession; print('PySpark works')"
python /home/jovyan/work/sales_summary.py
```

## Open Jupyter

```text
http://127.0.0.1:8888
```

Token:

```text
admin
```

## Stop

```bash
docker compose down
```
