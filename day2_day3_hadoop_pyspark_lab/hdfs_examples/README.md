# HDFS Practice Notes

Use these commands from inside the Hadoop container:

```bash
hdfs dfs -mkdir -p /data
hdfs dfs -put /data/sales.csv /data/sales.csv
hdfs dfs -ls /data
hdfs dfs -cat /data/sales.csv
hdfs dfs -du -h /data
```
