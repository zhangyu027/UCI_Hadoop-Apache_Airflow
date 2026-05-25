# Quick Reference Card - Annual Profit Pipeline

## 🚀 Getting Started (5 minutes)

```bash
# Step 1: Start services
cd ~/projects/UCI_Hadoop_Apache_Airflow/kafka_dbt_project
docker compose up -d && docker compose ps

# Step 2: Three terminals needed

# TERMINAL 1: Consumer
python consumer2.py
# Expected: "Tables created successfully!"
# "Listening for Kafka messages..."

# TERMINAL 2: Producer
python producer.py
# Expected: 10 sales events + 50 profit events
# "All events sent successfully!"

# TERMINAL 3: dbt
dbt run --profiles-dir .dbt

# TERMINAL 4: Query
docker exec -it kafka_dbt_project-postgres-1 psql -U postgres -d analytics
```

---

## 📊 Essential Queries

### Top Profitable Categories
```sql
SELECT category, year, total_profit, overall_profit_margin_pct 
FROM profit_summary 
ORDER BY total_profit DESC LIMIT 10;
```

### Best Performing Products
```sql
SELECT product_name, total_profit, avg_profit_margin 
FROM product_profit_analysis 
ORDER BY total_profit DESC LIMIT 5;
```

### Year-over-Year Trends
```sql
SELECT category, year, annual_profit, profit_margin_pct 
FROM yearly_profit_trends 
ORDER BY annual_profit DESC;
```

### Data Check
```sql
SELECT 'raw_sales' as table_name, COUNT(*) as row_count FROM raw_sales
UNION ALL
SELECT 'raw_profit_events', COUNT(*) FROM raw_profit_events
UNION ALL
SELECT 'profit_summary', COUNT(*) FROM profit_summary
UNION ALL
SELECT 'product_profit_analysis', COUNT(*) FROM product_profit_analysis
UNION ALL
SELECT 'yearly_profit_trends', COUNT(*) FROM yearly_profit_trends;
```

---

## 📁 Key Files

| File | Purpose | Type |
|------|---------|------|
| `producer.py` | Generates 60 events (10 sales + 50 profit) | Python |
| `consumer2.py` | Ingests from 2 Kafka topics | Python |
| `profit_summary.sql` | Annual profit by category & year | SQL Model |
| `product_profit_analysis.sql` | Product-level metrics | SQL Model |
| `yearly_profit_trends.sql` | Year-over-year comparison | SQL Model |
| `schema.yml` | Model documentation & tests | YAML |

---

## 🎯 Data at a Glance

**Products:** 8 (Electronics, Clothing, Home, Food)
**Categories:** 4
**Years:** 3 (2023, 2024, 2025)
**Events:** 60 total (10 sales + 50 profit)
**Profit Margins:** 50-75%
**Tables:** 5 (2 raw + 3 analytical views)

---

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| Consumer won't start | Check: `docker compose ps` |
| Producer errors | Check: Kafka broker logs |
| dbt errors | Run: `dbt debug --profiles-dir .dbt` |
| No data in tables | Check: Consumer running first? Producer ran? |
| Query errors | Verify: dbt ran successfully |

---

## 📚 Documentation

| File | What | When |
|------|------|------|
| `QUICKSTART.md` | Quick reference | First time setup |
| `GUIDE.md` | Complete walkthrough | New to pipeline |
| `DATA_MODEL.md` | Technical details | Deep dive needed |
| `README.md` | Full overview | Understanding architecture |

---

## ⏹️ Stopping Services

```bash
# Stop all containers
docker compose down

# Check status
docker compose ps

# Clean up (careful!)
docker compose down -v  # Removes volumes too
```

---

## ✅ Expected Outputs

**profit_summary** (~12 rows):
```
category    | year | total_transactions | total_profit | overall_profit_margin_pct
Electronics | 2024 | 8                  | 4000         | 50.0
...
```

**product_profit_analysis** (8 rows):
```
product_name | category | num_transactions | total_profit
Laptop       | Electronics | 2            | 2000
...
```

**yearly_profit_trends** (~12 rows):
```
category | year | annual_profit | profit_margin_pct
Electronics | 2024 | 4000        | 50.0
...
```

---

## 🎓 Quick Concepts

**raw_sales** - Original sales events (user_id, event, amount)
**raw_profit_events** - Profit data from Kafka (product, category, year, revenue, cost, profit)
**profit_summary** - Aggregated by category & year
**product_profit_analysis** - Per-product metrics
**yearly_profit_trends** - Trend analysis across years

---

## 🚀 What's New vs Original

**Before:**
- 1 Kafka topic
- 1 raw table
- 1 dbt model
- Limited analytics

**After:**
- 2 Kafka topics ✨
- 2 raw tables ✨
- 4 dbt models (3 new) ✨
- Advanced profit analytics ✨

---

## 💡 Pro Tips

1. **Verify data first:**
   ```sql
   SELECT COUNT(*) FROM raw_profit_events;
   ```

2. **Check for nulls:**
   ```sql
   SELECT * FROM profit_summary WHERE total_profit IS NULL;
   ```

3. **Monitor margins:**
   ```sql
   SELECT AVG(profit_margin) FROM product_profit_analysis;
   ```

4. **Track growth:**
   ```sql
   SELECT category, year, annual_profit FROM yearly_profit_trends 
   ORDER BY category, year;
   ```

---

## ⚡ Performance Notes

- All queries complete in < 100ms
- ~60 total events for testing
- Tables auto-created on consumer startup
- Airflow DAG auto-picks up new models

---

## 🎉 You're Ready!

Start with: `python consumer2.py` → `python producer.py` → `dbt run`

Then query: `SELECT * FROM profit_summary ORDER BY total_profit DESC;`

Questions? Check GUIDE.md or DATA_MODEL.md

**Happy analyzing! 📊**
