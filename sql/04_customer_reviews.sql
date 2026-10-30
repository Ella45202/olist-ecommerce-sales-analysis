
USE olist_portfolio;

-- Customer review score analysis
SELECT
    review_score,
    CASE
        WHEN review_score >= 4 THEN 'Positive'
        WHEN review_score = 3 THEN 'Neutral'
        ELSE 'Negative'
    END AS review_sentiment,
    COUNT(*) AS total_reviews,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM order_reviews
WHERE review_score IS NOT NULL
GROUP BY
    review_score,
    CASE
        WHEN review_score >= 4 THEN 'Positive'
        WHEN review_score = 3 THEN 'Neutral'
        ELSE 'Negative'
    END
ORDER BY review_score DESC;

