
USE olist_portfolio;

-- Payment method and order value analysis
SELECT
    payment_type,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(payment_value), 2) AS total_payment_value,
    ROUND(AVG(payment_value), 2) AS avg_payment_record_value
FROM order_payments
GROUP BY payment_type
ORDER BY total_payment_value DESC;

