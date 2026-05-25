"""Produce sample sales events and profit data to Kafka."""

import json
import random
import time

from kafka import KafkaProducer


PRODUCTS = [
    {"product_id": 1, "name": "Laptop", "category": "Electronics", "cost": 600, "price": 1200},
    {"product_id": 2, "name": "Mouse", "category": "Electronics", "cost": 15, "price": 35},
    {"product_id": 3, "name": "T-Shirt", "category": "Clothing", "cost": 5, "price": 25},
    {"product_id": 4, "name": "Jeans", "category": "Clothing", "cost": 20, "price": 60},
    {"product_id": 5, "name": "Coffee Maker", "category": "Home", "cost": 30, "price": 80},
    {"product_id": 6, "name": "Pillows", "category": "Home", "cost": 10, "price": 35},
    {"product_id": 7, "name": "Coffee Beans", "category": "Food", "cost": 3, "price": 12},
    {"product_id": 8, "name": "Chocolate", "category": "Food", "cost": 2, "price": 8},
]

YEARS = [2023, 2024, 2025]


def main() -> None:
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    )

    # Send original sales events
    print("=== Sending Sales Events ===")
    for i in range(10):
        event = {
            "user_id": i + 1,
            "event": "purchase",
            "amount": (i + 1) * 100,
        }
        producer.send("sales_topic", value=event)
        print(f"Sales event sent: {event}")
        time.sleep(0.5)

    # Send profit events
    print("\n=== Sending Profit Events ===")
    for i in range(50):
        product = random.choice(PRODUCTS)
        year = random.choice(YEARS)
        quantity = random.randint(1, 20)
        revenue = product["price"] * quantity
        cost = product["cost"] * quantity
        profit = revenue - cost

        profit_event = {
            "product_id": product["product_id"],
            "product_name": product["name"],
            "category": product["category"],
            "year": year,
            "quantity": quantity,
            "revenue": revenue,
            "cost": cost,
            "profit": profit,
            "profit_margin": round((profit / revenue * 100), 2) if revenue > 0 else 0,
        }
        producer.send("profit_events", value=profit_event)
        print(f"Profit event sent: {profit_event}")
        time.sleep(0.3)

    producer.flush()
    producer.close()
    print("\nAll events sent successfully!")


if __name__ == "__main__":
    main()
