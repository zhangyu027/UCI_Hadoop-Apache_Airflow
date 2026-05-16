from kafka import KafkaConsumer
import json
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="analytics",
    user="postgres",
    password="postgres"
)

cursor = conn.cursor()

consumer = KafkaConsumer(
    'sales_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:

    data = message.value

    print("Received:", data)

    cursor.execute(
        """
        INSERT INTO raw_sales (user_id, event, amount)
        VALUES (%s, %s, %s)
        """,
        (
            data["user_id"],
            data["event"],
            data["amount"]
        )
    )

    conn.commit()