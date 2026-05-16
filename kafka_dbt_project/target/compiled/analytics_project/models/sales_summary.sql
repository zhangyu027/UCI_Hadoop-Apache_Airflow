SELECT
    event,
    COUNT(*) AS total_events
FROM raw_sales
GROUP BY event