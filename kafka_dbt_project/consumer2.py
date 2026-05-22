"""Read sales events from Kafka and insert them into PostgreSQL."""

import json

import psycopg2
from kafka import KafkaConsumer


CREATE_TABLE_SQL = """
create table if not exists raw_sales (
    user_id integer,
    event varchar(50),
    amount integer
);
"""

INSERT_SQL = """
insert into raw_sales (user_id, event, amount)
values (%s, %s, %s);
"""


def main() -> None:
    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        database="analytics",
        user="postgres",
        password="postgres",
    )
    cursor = connection.cursor()
    cursor.execute(CREATE_TABLE_SQL)
    connection.commit()

    consumer = KafkaConsumer(
        "sales_topic",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="sales-postgres-consumer",
        value_deserializer=lambda raw: json.loads(raw.decode("utf-8")),
    )

    for message in consumer:
        data = message.value
        print(f"Received: {data}")

        cursor.execute(
            INSERT_SQL,
            (data["user_id"], data["event"], data["amount"]),
        )
        connection.commit()


if __name__ == "__main__":
    main()
