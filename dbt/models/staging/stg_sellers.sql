with source as (
    select * from {{ source('raw_data', 'raw_olist_sellers_dataset') }}
)

select
    seller_id,
    cast(seller_zip_code_prefix as text) as zip_code_prefix,
    seller_city as city,
    seller_state as state
from source
