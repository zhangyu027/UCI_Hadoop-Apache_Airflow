# Enhanced Kafka Pipeline: Annual Profit Data

## 🎯 Mission Accomplished

You now have a production-ready Kafka + dbt data pipeline that tracks annual profit data across multiple product categories and years.

---

## 📋 What Changed

### Before
- Single Kafka topic: `sales_topic`
- Single raw table: `raw_sales` (3 columns)
- Single dbt model: `sales_summary`
- Limited analytics capability

### After ✨
- **Two Kafka topics**: `sales_topic` + `profit_events`
- **Two raw tables**: `raw_sales` + `raw_profit_events` (9 columns)
- **Four dbt models**: sales_summary + 3 new profit models
- **Advanced analytics**: Category, product, and yearly analysis

---

## 📊 Data Flow Example

**Producer generates 60 events:**
```
10 Sales Events:
  { user_id: 1, event: "purchase", amount: 100 }
  { user_id: 2, event: "purchase", amount: 200 }
  ...

50 Profit Events:
  { 
    product_id: 1, 
    product_name: "Laptop", 
    category: "Electronics", 
    year: 2024, 
    quantity: 5,
    revenue: 6000,
    cost: 3000,
    profit: 3000,
    profit_margin: 50.0 
  }
  ...
```

**Consumer ingests into PostgreSQL:**
```
raw_sales table:
  user_id | event    | amount
  1       | purchase | 100
  2       | purchase | 200

raw_profit_events table:
  product_id | product_name | category    | year | quantity | revenue | cost | profit | profit_margin
  1          | Laptop       | Electronics | 2024 | 5        | 6000    | 3000 | 3000   | 50.0
  ...
```

**dbt models transform into analytics:**
```
profit_summary:
  category    | year | total_profit | overall_profit_margin_pct
  Electronics | 2024 | 12500        | 48.5
  
product_profit_analysis:
  product_name | total_profit | avg_profit_margin
  Laptop       | 5000         | 50.0
  
yearly_profit_trends:
  category    | year | annual_profit | profit_margin_pct
  Electronics | 2024 | 12500         | 48.5
```

---

## 📁 Modified & New Files

```
kafka_dbt_project/
├── 📄 producer.py ✏️ MODIFIED
│   └── Now generates 50 profit events with realistic data
│
├── 📄 consumer2.py ✏️ MODIFIED  
│   └── Listens to 2 topics, inserts into 2 tables
│
├── 📁 models/
│   ├── 📄 sales_summary.sql (existing)
│   ├── 📄 profit_summary.sql ✨ NEW
│   ├── 📄 product_profit_analysis.sql ✨ NEW
│   ├── 📄 yearly_profit_trends.sql ✨ NEW
│   └── 📄 schema.yml ✏️ UPDATED
│
├── 📄 README.md ✏️ UPDATED
├── 📄 QUICKSTART.md ✨ NEW
└── 📄 DATA_MODEL.md ✨ NEW
```

---

## 🚀 Getting Started

### Step 1: Start Services
```bash
cd ~/projects/UCI_Hadoop_Apache_Airflow/kafka_dbt_project
docker compose up -d
```

### Step 2: Terminal 1 - Run Consumer
```bash
python consumer2.py
```
Expected output:
```
Tables created successfully!
Listening for Kafka messages... (Ctrl+C to stop)
```

### Step 3: Terminal 2 - Run Producer
```bash
python producer.py
```
Expected output:
```
=== Sending Sales Events ===
Sales event sent: {...}
...
=== Sending Profit Events ===
Profit event sent: {...}
...
All events sent successfully!
```

### Step 4: Terminal 3 - Run dbt
```bash
dbt debug --profiles-dir .dbt
dbt run --profiles-dir .dbt
dbt test --profiles-dir .dbt
```

### Step 5: Query Results
```bash
docker exec -it kafka_dbt_project-postgres-1 psql -U postgres -d analytics
```

```sql
-- See annual profit by category & year
SELECT * FROM profit_summary 
ORDER BY year DESC, total_profit DESC;

-- See product performance
SELECT * FROM product_profit_analysis 
ORDER BY total_profit DESC;

-- See year-over-year trends
SELECT * FROM yearly_profit_trends 
ORDER BY annual_profit DESC;
```

---

## 📈 Analytics Capabilities

### 1. Annual Profit by Category
```sql
SELECT 
  category, 
  year, 
  total_profit,
  overall_profit_margin_pct
FROM profit_summary
ORDER BY total_profit DESC;
```
**Insight:** Which product categories are most profitable?

### 2. Product Performance
```sql
SELECT 
  product_name,
  total_quantity_sold,
  total_profit,
  avg_profit_margin
FROM product_profit_analysis
ORDER BY total_profit DESC;
```
**Insight:** Which products drive the most profit?

### 3. Year-Over-Year Growth
```sql
SELECT 
  category,
  year,
  annual_profit
FROM yearly_profit_trends
ORDER BY category, year DESC;
```
**Insight:** Is the business growing or declining?

### 4. Margin Analysis
```sql
SELECT 
  category,
  MIN(profit_margin_pct) as min_margin,
  MAX(profit_margin_pct) as max_margin,
  AVG(profit_margin_pct) as avg_margin
FROM profit_summary
GROUP BY category;
```
**Insight:** Which categories have the best margins?

---

## 🎓 Key Concepts

### Kafka Topics (Message Streams)
- **sales_topic**: Original sales events (user purchases)
- **profit_events**: New profit data (revenue, cost, margin)

### Raw Tables (Staging)
- **raw_sales**: Unmodified sales event data
- **raw_profit_events**: Unmodified profit event data

### Analytical Models (dbt)
- **profit_summary**: Aggregate profit by category & year
- **product_profit_analysis**: Product-level metrics
- **yearly_profit_trends**: Time series analysis

### Product Catalog
- 8 products across 4 categories
- Realistic cost/price ratios
- 50-75% profit margins

### Data Coverage
- 60 total events (10 sales + 50 profit)
- 3 years (2023, 2024, 2025)
- 4 product categories
- Realistic quantities and margins

---

## ✅ Checklist

- ✅ Producer generates diverse profit data
- ✅ Consumer ingests multi-topic Kafka streams  
- ✅ PostgreSQL stores raw and profit data
- ✅ 3 new dbt models for profit analysis
- ✅ Schema documentation with tests
- ✅ Comprehensive README and guides
- ✅ Quick start guide created
- ✅ Data model documentation
- ✅ Backward compatible with original pipeline
- ✅ Airflow integration ready

---

## 🔧 Troubleshooting

**Consumer not starting?**
```bash
# Check Kafka is running
docker compose ps

# Verify PostgreSQL is accessible
docker exec kafka_dbt_project-postgres-1 pg_isready
```

**Producer errors?**
```bash
# Check Kafka broker
docker logs kafka_dbt_project-kafka-1

# Verify bootstrap server
kafka-console-producer --bootstrap-server localhost:9092 --topic test
```

**dbt not running?**
```bash
# Verify profiles.yml
cat .dbt/profiles.yml

# Test connection
dbt debug --profiles-dir .dbt
```

---

## 📚 Documentation Files

- **README.md** - Full project overview and setup
- **QUICKSTART.md** - Quick reference guide
- **DATA_MODEL.md** - Detailed data documentation
- **schema.yml** - Model definitions and tests
- **COMPLETION_REPORT.md** - What was built
- **IMPLEMENTATION_SUMMARY.md** - Technical details

---

## 🎉 You're All Set!

Your Kafka pipeline now supports comprehensive profit analysis. Start with the Quick Start guide and explore your data!

Questions? Check the documentation files or review the code in producer.py, consumer2.py, and the models/ directory.
