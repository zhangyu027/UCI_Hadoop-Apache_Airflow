
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for i in range(10):

    event = {
        "user_id": i,
        "event": "purchase",
        "amount": i * 100
    }

    producer.send('sales_topic', value=event)

    print("Sent:", event)

    time.sleep(1)

producer.flush()
