with items as (
    select * from {{ ref('stg_order_items') }}
),
orders as (
    select * from {{ ref('stg_orders') }}
)

select
    i.order_item_id,
    i.order_id,
    i.product_id,
    i.seller_id,
    o.customer_id,
    o.order_purchase_timestamp,
    i.price,
    i.freight_value
from items i
left join orders o on i.order_id = o.order_id
