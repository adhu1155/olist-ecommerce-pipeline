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
customers as (
    select * from {{ ref('stg_customers') }}
)

select
    o.order_id,
    c.customer_unique_id,
    o.order_status,
    o.order_purchase_timestamp,
    p.total_payment_value
from orders o
left join customers c on o.customer_id = c.customer_id
left join payments p on o.order_id = p.order_id
