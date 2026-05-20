# Airflow Docker Compose Package for Kafka + dbt

This package lets your `kafka_dbt_project` folder run with:

```bash
docker compose up -d
```

## Replace or add files

Copy these into:

```bash
~/projects/kafka_dbt_project
```

Files included:

```text
docker-compose.yml
dags/kafka_dbt_pipeline_dag.py
.dbd/profiles.yml example note
logs/.gitkeep
plugins/.gitkeep
```

## Important folder assumption

This `docker-compose.yml` assumes your Kafka/dbt project is here:

```bash
~/projects/UCI_Hadoop-Apache_Airflow/kafka_dbt_project
```

The volume line is:

```yaml
../UCI_Hadoop-Apache_Airflow/kafka_dbt_project:/opt/airflow/kafka_dbt_project
```

## Add dbt profile into your Kafka project

Create this folder:

```bash
mkdir -p ~/projects/UCI_Hadoop-Apache_Airflow/airflow_docker_compose_kafka_dbt/.dbt
```

Put the included `.dbt/profiles.yml` there.

## Start Kafka/Postgres first

```bash
cd ~/projects/UCI_Hadoop-Apache_Airflow/airflow_docker_compose_kafka_dbt
docker compose up -d
```

## Start Airflow

```bash
cd ~/projects/kafka_dbt_project
echo "AIRFLOW_UID=$(id -u)" > .env
docker compose up airflow-init
docker compose up -d
```

## Open Airflow

```text
http://localhost:8080
http://localhost:8081
```

Login:

```text
username: admin
password: admin
```

## Trigger DAG

Search for:

```text
kafka_dbt_pipeline
```

Turn it ON and click **Trigger DAG**.
