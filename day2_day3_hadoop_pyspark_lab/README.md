# Day 2–3 — Hadoop HDFS + PySpark Fundamentals Lab

This lab covers Hadoop/HDFS foundations and PySpark DataFrame transformations.

## Architecture

```text
Docker Compose
├── day2-hadoop       → Hadoop command-line HDFS practice container
└── day3-pyspark      → Jupyter PySpark notebook/script container
```

## Folder structure

```text
day2_day3_hadoop_pyspark_lab/
├── data/
│   └── sales.csv
├── hdfs_examples/
│   └── README.md
├── spark_jobs/
│   ├── sales_summary.py
│   └── word_count.py
├── docker-compose.yml
├── README.md
└── .gitignore
```

## Start the lab

```bash
cd ~/projects/UCI_Hadoop_Apache_Airflow/day2_day3_hadoop_pyspark_lab
docker compose down
docker compose up -d
docker compose ps
```

Expected containers:

```text
day2-hadoop
day3-pyspark
```

## Day 2 — Hadoop / HDFS practice

Enter the Hadoop container:

```bash
docker exec -it day2-hadoop bash
```

Check Hadoop commands:

```bash
hadoop version
hdfs version
```

Create an HDFS-style practice directory and inspect the mounted file:

```bash
ls -la /data
cat /data/sales.csv
```

Practice common HDFS commands:

```bash
hdfs dfs -mkdir -p /data
hdfs dfs -put /data/sales.csv /data/sales.csv
hdfs dfs -ls /data
hdfs dfs -cat /data/sales.csv
hdfs dfs -du -h /data
```

Exit:

```bash
exit
```

Note: this lightweight lab container is mainly for Hadoop CLI practice. The PySpark container performs the working data transformation.

## Day 3 — PySpark practice

Run the Spark sales summary job:

```bash
docker exec -it day3-pyspark bash
python /home/jovyan/work/sales_summary.py
```

Expected outputs:

- Original sales data
- Category-level sales summary
- Filtered sales greater than 100
- Window function ranking
- CSV output under `data/output/category_sales_summary`

Run the word count job:

```bash
python /home/jovyan/work/word_count.py
```

## Open Jupyter notebook

Open:

```text
http://127.0.0.1:8888
```

Token:

```text
admin
```

Inside Jupyter, open:

```text
work/sales_summary.py
```

or create a notebook and use the mounted files under:

```text
/home/jovyan/data
/home/jovyan/work
```

## Validate output on your Mac

After running `sales_summary.py`, check:

```bash
ls -la data/output/category_sales_summary
```

## Stop

```bash
docker compose down
```

## Full reset

```bash
docker compose down -v
rm -rf data/output
docker compose up -d
```

## What this lab demonstrates

- Docker Compose service setup
- Hadoop/HDFS command concepts
- PySpark DataFrame loading
- Filtering
- Aggregation
- Window ranking
- Writing transformed output
