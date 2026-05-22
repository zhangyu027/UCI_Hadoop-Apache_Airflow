# Airflow Docker Compose Kafka dbt Project

This project runs Apache Airflow with PostgreSQL and includes dbt support.

## Important folder clarification

The main project folder is:

```bash
airflow_docker_compose_kafka_dbt
```

Run all Docker commands from this folder.

`kafka_dbt_project` is **not** the main Docker folder. It is only the dbt project subfolder that is mounted into the Airflow container.

Airflow reads DAG files from:

```text
./dags
```

dbt project files live in:

```text
./kafka_dbt_project
```

Inside the Airflow container, that same dbt folder appears at:

```text
/opt/airflow/kafka_dbt_project
```

That is why the Docker Compose volume line is still needed:

```yaml
- ./kafka_dbt_project:/opt/airflow/kafka_dbt_project
```

Do **not** delete that line if your DAG needs to run `dbt debug`, `dbt run`, or `dbt test`.

---

## Recommended folder structure

```text
airflow_docker_compose_kafka_dbt/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
├── dags/
│   └── kafka_dbt_pipeline_dag.py
├── logs/
├── plugins/
├── .dbt/
│   └── profiles.yml
└── kafka_dbt_project/
    ├── dbt_project.yml
    ├── models/
    └── seeds/
```

---

## 1. Start Docker Desktop

Make sure Docker Desktop is running.

---

## 2. Go to the correct project folder

```bash
cd ~/projects/UCI_Hadoop_Apache_Airflow/airflow_docker_compose_kafka_dbt
```

Check that you are in the right folder:

```bash
pwd
ls -la
```

You should see:

```text
docker-compose.yml
Dockerfile
requirements.txt
dags/
kafka_dbt_project/
```

---

## 3. Build the custom Airflow image

Run this after changing `Dockerfile` or `requirements.txt`:

```bash
docker compose build --no-cache
```

This permanently installs dbt and other Python packages into the Docker image, instead of reinstalling packages every time Airflow starts.

---

## 4. Start Airflow

Run in background:

```bash
docker compose up -d
```

Or run in foreground to watch logs:

```bash
docker compose up
```

---

## 5. Check containers

```bash
docker compose ps
```

Expected status:

```text
airflow-postgres     Up / healthy
airflow-webserver    Up
airflow-scheduler    Up
```

The webserver port should show:

```text
0.0.0.0:8081->8080/tcp
```

---

## 6. Open Airflow

Open this URL in your browser:

```text
http://localhost:8081
```

Use `8081`, not `8080`, because this project maps your Mac port `8081` to Airflow container port `8080`.

---

## 7. Login

```text
Username: admin
Password: admin
```

---

## 8. Run dbt manually inside the Airflow container

```bash
docker exec -it airflow_docker_compose_kafka_dbt-airflow-webserver-1 bash
cd /opt/airflow/kafka_dbt_project
dbt debug
dbt run
dbt test
```

---

## 9. Check logs

```bash
docker compose logs airflow-webserver --tail 100
docker compose logs airflow-scheduler --tail 100
docker compose logs airflow-init --tail 100
```

---

## 10. Stop Airflow

```bash
docker compose down
```

To remove containers and the PostgreSQL volume completely:

```bash
docker compose down -v
```

Use `down -v` only when you want to reset the Airflow database.

---

## Common issue: localhost:8080 does not open

This project uses:

```yaml
ports:
  - "8081:8080"
```

So open:

```text
http://localhost:8081
```

not:

```text
http://localhost:8080
```

---

## Common issue: packages reinstall every time

Do not use this old setting:

```yaml
_PIP_ADDITIONAL_REQUIREMENTS: dbt-postgres kafka-python psycopg2-binary pandas
```

The permanent fix is:

1. Put packages in `requirements.txt`.
2. Install them in `Dockerfile`.
3. Use `build: .` in `docker-compose.yml`.
4. Run:

```bash
docker compose build --no-cache
docker compose up -d
```
