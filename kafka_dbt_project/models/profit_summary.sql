select
    category,
    year,
    count(*) as total_transactions,
    sum(quantity) as total_quantity,
    sum(revenue) as total_revenue,
    sum(cost) as total_cost,
    sum(profit) as total_profit,
    round(avg(profit_margin), 2) as avg_profit_margin,
    round(sum(profit) / nullif(sum(revenue), 0) * 100, 2) as overall_profit_margin_pct
from raw_profit_events
group by category, year
order by year desc, total_profit desc
