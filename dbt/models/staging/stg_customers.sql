-- dbt/models/staging/stg_customers.sql
with source as (
    select * from {{ source('raw_data', 'raw_olist_customers_dataset') }}
)
select
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
from source
