
  create view "analytics"."public"."sales_summary__dbt_tmp"
    
    
  as (
    SELECT
    event,
    COUNT(*) AS total_events
FROM raw_sales
GROUP BY event
  );