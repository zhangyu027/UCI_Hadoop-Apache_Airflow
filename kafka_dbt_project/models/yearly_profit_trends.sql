select
    category,
    year,
    sum(profit) as annual_profit,
    sum(revenue) as annual_revenue,
    sum(cost) as annual_cost,
    count(*) as transaction_count,
    round(sum(profit) / nullif(sum(revenue), 0) * 100, 2) as profit_margin_pct
from raw_profit_events
group by category, year
order by category, year desc
