with customers as (
    select * from {{ ref('stg_customers') }}
)
select
    customer_unique_id,
    max(customer_zip_code_prefix) as zip_code_prefix,
    max(customer_city) as city,
    max(customer_state) as state
from customers
group by 1
