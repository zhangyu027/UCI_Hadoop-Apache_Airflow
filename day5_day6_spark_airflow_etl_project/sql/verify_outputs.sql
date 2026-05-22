\dt

select *
from public.cleaned_sales_events
order by event_date, order_id;

select *
from public.daily_sales_summary
order by event_date, event;
