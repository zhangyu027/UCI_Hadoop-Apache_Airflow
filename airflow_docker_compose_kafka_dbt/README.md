# Airflow Docker Compose Kafka dbt Project — Fixed Package

This package fixes the repeated package-install problem by using a custom Airflow Docker image.

## What was fixed

The old `docker-compose.yml` used `_PIP_ADDITIONAL_REQUIREMENTS`, so Airflow installed `dbt-postgres`, `kafka-python`, `psycopg2-binary`, and other packages every time containers started. That created repeated dependency warnings and slow restarts.

This version adds:

- `Dockerfile`
- `requirements.txt`
- `custom-airflow-dbt:2.9.3` image
- permanent port mapping: `localhost:8081`
- `.dbt/profiles.yml` mount

## Folder structure

```text
airflow_docker_compose_kafka_dbt_fixed/
├── Dockerfile
├── README.md
├── docker-compose.yml
├── requirements.txt
├── .env
├── .dbt/
│   └── profiles.yml
├── dags/
│   └── kafka_dbt_pipeline_dag.py
├── logs/
│   └── .gitkeep
└── plugins/
    └── .gitkeep
```

## 1. Put folder in your projects directory

Recommended location:

```bash
~/projects/UCI_Hadoop_Apache_Airflow/airflow_docker_compose_kafka_dbt
```

If replacing an existing folder, back it up first.

## 2. Make sure your dbt project path is correct

This compose file expects your dbt project here:

```bash
~/projects/UCI_Hadoop_Apache_Airflow/kafka_dbt_project
```

The volume line is:

```yaml
../kafka_dbt_project:/opt/airflow/kafka_dbt_project
```

If your dbt project is somewhere else, update that line in `docker-compose.yml`.

## 3. Start Docker Desktop

Make sure Docker Desktop is open and running.

## 4. Go to project folder

```bash
cd ~/projects/UCI_Hadoop_Apache_Airflow/airflow_docker_compose_kafka_dbt
```

## 5. Build the custom Airflow image once

```bash
docker compose down
AIRFLOW_UID=$(id -u) docker compose build --no-cache
```

## 6. Start Airflow

```bash
AIRFLOW_UID=$(id -u) docker compose up -d
```

## 7. Check containers

```bash
docker compose ps
```

Expected:

```text
airflow-postgres     Up / healthy
airflow-webserver    Up / 0.0.0.0:8081->8080
airflow-scheduler    Up
```

## 8. Open Airflow

Use this URL:

```text
http://localhost:8081
```

Do not use `localhost:8080` unless you change the port mapping.

## 9. Login

```text
Username: admin
Password: admin
```

## 10. Check logs

```bash
docker compose logs airflow-webserver --tail 100
docker compose logs airflow-scheduler --tail 100
docker compose logs airflow-init --tail 100
```

## 11. Trigger DAG

In Airflow, search for:

```text
kafka_dbt_pipeline
```

Turn it on and click **Trigger DAG**.

## 12. Stop Airflow

```bash
docker compose down
```

## Daily restart command

After the image is built once, next time just run:

```bash
cd ~/projects/UCI_Hadoop_Apache_Airflow/airflow_docker_compose_kafka_dbt
AIRFLOW_UID=$(id -u) docker compose up -d
```

Then open:

```text
http://localhost:8081
```
