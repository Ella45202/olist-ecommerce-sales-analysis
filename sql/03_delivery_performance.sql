
USE olist_portfolio;

-- Delivery performance analysis
SELECT
    COUNT(*) AS delivered_orders,
    ROUND(
        AVG(DATEDIFF(
            order_delivered_customer_date,
            order_purchase_timestamp
        )), 2
    ) AS avg_days_from_purchase_to_delivery,
    SUM(
        CASE
            WHEN order_delivered_customer_date >
                 order_estimated_delivery_date
            THEN 1 ELSE 0
        END
    ) AS late_orders,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN order_delivered_customer_date >
                     order_estimated_delivery_date
                THEN 1 ELSE 0
            END
        ) / COUNT(*), 2
    ) AS late_delivery_percentage
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL;

