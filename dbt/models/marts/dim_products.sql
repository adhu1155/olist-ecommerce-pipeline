with products as (
    select * from {{ ref('stg_products') }}
)

select
    product_id,
    category_name,
    weight_g,
    length_cm,
    height_cm,
    width_cm,
    photos_qty
from products
