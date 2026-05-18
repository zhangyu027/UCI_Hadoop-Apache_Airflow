# AWS Free-Tier / Very-Low-Cost Data Lake Solution

## Goal

Create a small AWS data lake for teaching and portfolio use with:

```text
S3 Raw Zone
   ↓
Glue Data Catalog
   ↓
Athena SQL Query
   ↓
S3 Athena Results
```

This avoids expensive services such as EMR, Redshift, OpenSearch, always-on EC2, and Glue ETL jobs.

## Cost Note

This is designed for very small demo data. It is not guaranteed to be $0 because AWS charges depend on your account age, region, free-tier credits, S3 requests/storage, and Athena query scans. Keep files tiny and delete the stack when finished.

## Prerequisites

```bash
aws --version
aws configure
```

Use region:

```text
us-west-2
```

## Deploy

From this folder:

```bash
chmod +x scripts/deploy.sh scripts/cleanup.sh
./scripts/deploy.sh yu-free-datalake us-west-2
```

## Query in Athena

Go to AWS Console → Athena.

Select workgroup:

```text
yu-free-datalake-workgroup
```

Select database:

```text
yu-free-datalake_db
```

Run:

```sql
SELECT * FROM sales_csv;
```

Then:

```sql
SELECT
  event,
  COUNT(*) AS total_events,
  SUM(amount) AS total_amount
FROM sales_csv
GROUP BY event;
```

## Clean Up

```bash
./scripts/cleanup.sh yu-free-datalake us-west-2
```

## What Students Learn

- Data lake raw zone
- S3 object storage
- Metadata catalog
- External table
- Serverless SQL with Athena
- Cost-aware cloud design
```
unzip aws_free_tier_data_lake_solution.zip
cd aws_free_tier_data_lake_solution

chmod +x scripts/deploy.sh scripts/cleanup.sh
./scripts/deploy.sh yu-free-datalake us-west-2
```
./scripts/cleanup.sh yu-free-datalake us-west-2
```
git add .
git commit -m "Add AWS Athena data lake project and ETL updates"
git push origin master
```