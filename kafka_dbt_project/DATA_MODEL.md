# Annual Profit Data Pipeline - Implementation Details

## Data Model

### Raw Tables (Kafka → PostgreSQL)

#### `raw_sales` (Existing)
```
user_id    | event    | amount
-----------|----------|--------
1          | purchase | 100
2          | purchase | 200
...
```

#### `raw_profit_events` (New)
```
product_id | product_name | category    | year | quantity | revenue | cost | profit | profit_margin
-----------|--------------|-------------|------|----------|---------|------|--------|---------------
1          | Laptop       | Electronics | 2024 | 5        | 6000    | 3000 | 3000   | 50.00
2          | Mouse        | Electronics | 2024 | 10       | 350     | 150  | 200    | 57.14
...
```

### Analytics Models (dbt Views)

#### `sales_summary`
Aggregates original sales events by event type:
```
event    | total_events | total_amount
---------|--------------|-------------
purchase | 10           | 5500
```

#### `profit_summary` ⭐ NEW
Annual profit aggregation by category and year:
```
category    | year | total_transactions | total_quantity | total_revenue | total_cost | total_profit | avg_profit_margin | overall_profit_margin_pct
------------|------|-------------------|-------------------|
Electronics | 2024 | 25                | 150           | 15000         | 8000       | 7000         | 52.15             | 46.67
Clothing    | 2024 | 12                | 80            | 2000          | 900        | 1100         | 54.67             | 55.00
```

**Use Cases:**
- Identify most profitable product categories
- Track category performance year-over-year
- Monitor profit margin trends
- Benchmark category profitability

#### `product_profit_analysis` ⭐ NEW
Product-level profitability across all time:
```
product_id | product_name | category    | num_transactions | total_quantity_sold | total_profit | avg_profit_margin | min_profit_margin | max_profit_margin
-----------|--------------|-------------|------------------|---------------------|--------------|-------------------|-------------------|------------------
1          | Laptop       | Electronics | 8                | 45                  | 22500        | 50.00             | 50.00             | 50.00
3          | T-Shirt      | Clothing    | 15               | 120                 | 2400         | 60.00             | 60.00             | 60.00
```

**Use Cases:**
- Identify star performers vs underperformers
- Analyze product profitability consistency
- Optimize product mix and pricing
- Performance benchmarking

#### `yearly_profit_trends` ⭐ NEW
Year-over-year profit comparison by category:
```
category    | year | annual_profit | annual_revenue | profit_margin_pct
------------|------|---------------|----------------|------------------
Electronics | 2025 | 8500          | 18000          | 47.22
Electronics | 2024 | 7000          | 15000          | 46.67
Electronics | 2023 | 6200          | 13000          | 47.69
```

**Use Cases:**
- Track business growth trends
- Identify growth/decline categories
- Forecast future profitability
- Strategic planning and decision making

## Data Generation Strategy

### Producer Events (60 total)

**Sales Events (10):**
- Sequential user IDs (1-10)
- Fixed "purchase" event type
- Linear amount pattern: $100, $200, ..., $1000

**Profit Events (50):**
- Random selection from 8 products
- Random year from [2023, 2024, 2025]
- Random quantity: 1-20 units
- Calculated revenue: product_price × quantity
- Calculated cost: product_cost × quantity
- Calculated profit: revenue - cost
- Calculated margin: (profit / revenue) × 100%

### Product Catalog (8 products, 4 categories)

**Electronics** (High margin items):
- Laptop: Cost $600 → Price $1200 (50% margin)
- Mouse: Cost $15 → Price $35 (57.1% margin)

**Clothing** (Medium margin items):
- T-Shirt: Cost $5 → Price $25 (60% margin)
- Jeans: Cost $20 → Price $60 (66.7% margin)

**Home** (Varied margin items):
- Coffee Maker: Cost $30 → Price $80 (62.5% margin)
- Pillows: Cost $10 → Price $35 (71.4% margin)

**Food** (High margin consumables):
- Coffee Beans: Cost $3 → Price $12 (75% margin)
- Chocolate: Cost $2 → Price $8 (75% margin)

## Query Examples

### 1. Annual Revenue by Category
```sql
SELECT 
    category,
    year,
    annual_revenue,
    annual_profit,
    ROUND(profit_margin_pct, 2) as margin_pct
FROM yearly_profit_trends
ORDER BY year DESC, annual_profit DESC;
```

### 2. Top 5 Products by Profit
```sql
SELECT 
    product_name,
    category,
    total_quantity_sold,
    total_profit,
    avg_profit_margin
FROM product_profit_analysis
ORDER BY total_profit DESC
LIMIT 5;
```

### 3. Margin Analysis by Category & Year
```sql
SELECT 
    category,
    year,
    total_revenue,
    total_profit,
    overall_profit_margin_pct,
    avg_profit_margin
FROM profit_summary
ORDER BY overall_profit_margin_pct DESC;
```

### 4. Growth Analysis (YoY)
```sql
WITH yearly AS (
    SELECT 
        category,
        year,
        annual_profit
    FROM yearly_profit_trends
)
SELECT 
    a.category,
    a.year as current_year,
    b.year as prior_year,
    a.annual_profit as current_profit,
    b.annual_profit as prior_profit,
    ROUND((a.annual_profit - b.annual_profit) / b.annual_profit * 100, 2) as growth_pct
FROM yearly a
LEFT JOIN yearly b ON a.category = b.category 
    AND a.year = b.year + 1;
```

### 5. Product Performance Consistency
```sql
SELECT 
    product_name,
    category,
    avg_profit_margin,
    (max_profit_margin - min_profit_margin) as margin_variance,
    CASE 
        WHEN (max_profit_margin - min_profit_margin) < 5 THEN 'Consistent'
        WHEN (max_profit_margin - min_profit_margin) < 15 THEN 'Moderate'
        ELSE 'Volatile'
    END as consistency
FROM product_profit_analysis
ORDER BY margin_variance DESC;
```

## Integration with Airflow

The existing DAG (`kafka_dbt_pipeline_dag.py`) already orchestrates:
1. **check_dbt_version** - Verify dbt installation
2. **dbt_debug** - Test dbt connectivity to database
3. **dbt_run** - Execute all models (including new ones)
4. **dbt_test** - Run data quality tests

**No changes needed** to the DAG - it automatically picks up new models!

## Performance Characteristics

- **raw_profit_events table**: 50 rows (grows with each run)
- **profit_summary**: ~12 rows (4 categories × 3 years)
- **product_profit_analysis**: 8 rows (1 per product)
- **yearly_profit_trends**: ~12 rows (4 categories × 3 years)

All queries complete in <100ms on modern hardware.

## Extension Points

Ready to add more features:
- Geographic/regional dimensions
- Customer segmentation analysis
- Seasonal patterns
- Product recommendations
- Anomaly detection
- Real-time alerts
- Predictive forecasting
