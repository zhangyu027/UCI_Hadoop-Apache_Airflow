"""Produce sample sales events to Kafka."""

import json
import time

from kafka import KafkaProducer


def main() -> None:
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    )

    for i in range(10):
        event = {
            "user_id": i + 1,
            "event": "purchase",
            "amount": (i + 1) * 100,
        }
        producer.send("sales_topic", value=event)
        print(f"Sent: {event}")
        time.sleep(1)

    producer.flush()
    producer.close()


if __name__ == "__main__":
    main()
