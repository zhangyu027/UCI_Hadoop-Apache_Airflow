"""Read sample sales events from Kafka and print them."""

import json

from kafka import KafkaConsumer


def main() -> None:
    consumer = KafkaConsumer(
        "sales_topic",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="sales-print-consumer",
        value_deserializer=lambda raw: json.loads(raw.decode("utf-8")),
    )

    for message in consumer:
        print(f"Received: {message.value}")


if __name__ == "__main__":
    main()
