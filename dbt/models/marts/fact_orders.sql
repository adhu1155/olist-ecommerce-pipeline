with orders as (
    select * from {{ ref('stg_orders') }}
),
payments as (
    select 
        order_id,
        sum(payment_value) as total_payment_value
    from {{ ref('stg_payments') }}
    group by 1
),
order_items as (
    select
        order_id,
        count(order_item_id) as total_items,
        sum(price) as total_items_price,
        sum(freight_value) as total_freight_value
    from {{ ref('stg_order_items') }}
    group by 1
),
customers as (
    select * from {{ ref('stg_customers') }}
)

select
    o.order_id,
    c.customer_unique_id,
    o.order_status,
    o.order_purchase_timestamp,
    coalesce(i.total_items, 0) as total_items,
    coalesce(i.total_items_price, 0) as total_items_price,
    coalesce(i.total_freight_value, 0) as total_freight_value,
    p.total_payment_value
from orders o
left join customers c on o.customer_id = c.customer_id
left join payments p on o.order_id = p.order_id
left join order_items i on o.order_id = i.order_id
