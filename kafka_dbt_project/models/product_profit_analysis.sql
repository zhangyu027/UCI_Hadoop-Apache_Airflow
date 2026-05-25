select
    product_id,
    product_name,
    category,
    count(*) as num_transactions,
    sum(quantity) as total_quantity_sold,
    sum(revenue) as total_revenue,
    sum(cost) as total_cost,
    sum(profit) as total_profit,
    round(avg(profit_margin), 2) as avg_profit_margin,
    round(min(profit_margin), 2) as min_profit_margin,
    round(max(profit_margin), 2) as max_profit_margin
from raw_profit_events
group by product_id, product_name, category
order by total_profit desc
