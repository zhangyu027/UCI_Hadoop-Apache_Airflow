# Quick Start: Annual Profit Pipeline

## 1. Start Infrastructure
```bash
cd ~/projects/UCI_Hadoop_Apache_Airflow/kafka_dbt_project
docker compose up -d
docker compose ps
```

## 2. Run Consumer (Terminal 1)
```bash
python consumer2.py
```
Expected: "Tables created successfully!" → "Listening for Kafka messages..."

## 3. Run Producer (Terminal 2)
```bash
python producer.py
```
Expected: 10 sales events + 50 profit events sent

## 4. Run dbt (Terminal 3)
```bash
dbt debug --profiles-dir .dbt
dbt run --profiles-dir .dbt
dbt test --profiles-dir .dbt
```

## 5. Query Results
```bash
docker exec -it kafka_dbt_project-postgres-1 psql -U postgres -d analytics
```

### Top Profitable Categories (YoY)
```sql
SELECT * FROM profit_summary ORDER BY total_profit DESC LIMIT 10;
```

### Top Performing Products
```sql
SELECT * FROM product_profit_analysis ORDER BY total_profit DESC LIMIT 5;
```

### Profit Trends by Year
```sql
SELECT * FROM yearly_profit_trends ORDER BY annual_profit DESC;
```

### Raw Data Check
```sql
SELECT COUNT(*) as profit_events_count FROM raw_profit_events;
SELECT COUNT(*) as sales_events_count FROM raw_sales;
```

## Key Files Modified

| File | Purpose |
|------|---------|
| `producer.py` | Generates 60 total events (10 sales + 50 profit) |
| `consumer2.py` | Ingests from 2 topics into 2 tables |
| `profit_summary.sql` | Annual profit by category/year |
| `product_profit_analysis.sql` | Product-level metrics |
| `yearly_profit_trends.sql` | Year-over-year comparison |
| `schema.yml` | Documentation & tests |

## Data Coverage

- **Products**: 8 products across 4 categories
- **Years**: 2023, 2024, 2025
- **Metrics**: Revenue, cost, profit, margins
- **Events**: 50 profit transactions + 10 sales events

## Stop Services
```bash
docker compose down
```

---

For detailed documentation, see README.md
