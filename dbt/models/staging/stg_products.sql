with source as (
    select * from {{ source('raw_data', 'raw_olist_products_dataset') }}
)

select
    product_id,
    product_category_name as category_name,
    product_photos_qty as photos_qty,
    product_weight_g as weight_g,
    product_length_cm as length_cm,
    product_height_cm as height_cm,
    product_width_cm as width_cm
from source
