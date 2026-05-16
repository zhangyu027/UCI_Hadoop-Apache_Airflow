
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select event
from "analytics"."public"."sales_summary"
where event is null



  
  
      
    ) dbt_internal_test