select
    event,
    count(*) as total_events,
    sum(amount) as total_amount
from raw_sales
group by event
