-- SQLite-compatible examples. These query the `fact_orders` table exported by CLI.
-- Business rules: eligible_sla=1 means delivered + valid customer delivery chronology
-- + non-null promised date. Date-level comparison is computed by the Python pipeline.

-- 1. What fraction of eligible delivered orders were late?
SELECT COUNT(*) AS delivered_orders,
       SUM(is_late) AS late_orders,
       ROUND(100.0 * SUM(is_late) / NULLIF(COUNT(*), 0), 2) AS late_rate_pct
FROM fact_orders WHERE eligible_sla = 1;

-- 2. Monthly late-delivery trend, grouped by PURCHASE month.
SELECT order_month, COUNT(*) AS delivered_orders,
       SUM(is_late) AS late_orders,
       ROUND(100.0 * SUM(is_late) / NULLIF(COUNT(*),0), 2) AS late_rate_pct
FROM fact_orders WHERE eligible_sla = 1
GROUP BY order_month ORDER BY order_month;

-- 3. States with at least 30 eligible orders (protect against very small groups).
SELECT customer_state, COUNT(*) AS delivered_orders,
       SUM(is_late) AS late_orders,
       ROUND(100.0 * SUM(is_late) / COUNT(*), 2) AS late_rate_pct
FROM fact_orders WHERE eligible_sla = 1
GROUP BY customer_state HAVING COUNT(*) >= 30
ORDER BY late_rate_pct DESC, delivered_orders DESC;

-- 4. Seller association: ONE-SELLER orders only, not proof of responsibility.
SELECT single_seller_id, COUNT(*) AS delivered_orders,
       SUM(is_late) AS late_orders,
       ROUND(100.0 * SUM(is_late) / COUNT(*), 2) AS late_rate_pct
FROM fact_orders
WHERE eligible_sla = 1 AND single_seller_order = 1 AND single_seller_id IS NOT NULL
GROUP BY single_seller_id HAVING COUNT(*) >= 30
ORDER BY late_rate_pct DESC, delivered_orders DESC;

-- 5. Customer review scores among reviewed orders (ASSOCIATION only).
SELECT CASE WHEN is_late = 1 THEN 'Late' ELSE 'On time' END AS delivery_group,
       COUNT(*) AS reviewed_orders,
       ROUND(AVG(review_score_mean), 2) AS avg_review_score,
       ROUND(100.0 * SUM(CASE WHEN review_score_mean <= 2 THEN 1 ELSE 0 END)/COUNT(*), 2) AS low_review_pct
FROM fact_orders
WHERE eligible_sla = 1 AND review_score_mean IS NOT NULL
GROUP BY delivery_group;

-- 6. Stage medians in Python; SQLite has no built-in portable MEDIAN aggregate.
SELECT is_late, COUNT(*) AS eligible_orders,
       ROUND(AVG(approval_days),2) AS mean_purchase_to_approval_days,
       ROUND(AVG(pre_handoff_days),2) AS mean_approval_to_handoff_days,
       ROUND(AVG(in_transit_days),2) AS mean_handoff_to_delivery_days
FROM fact_orders WHERE eligible_sla = 1
GROUP BY is_late;

-- 7. Intermediate/advanced SQL: rank states by late rate, using a CTE + window function.
WITH state_rates AS (
    SELECT customer_state, COUNT(*) AS total_delivered,
           SUM(is_late) AS late_delivered,
           1.0 * SUM(is_late) / NULLIF(COUNT(*),0) AS late_rate
    FROM fact_orders WHERE eligible_sla = 1
    GROUP BY customer_state HAVING COUNT(*) >= 30
)
SELECT customer_state, total_delivered, late_delivered,
       ROUND(100 * late_rate, 2) AS late_rate_pct,
       DENSE_RANK() OVER (ORDER BY late_rate DESC) AS late_rate_rank
FROM state_rates ORDER BY late_rate_rank, total_delivered DESC;

-- 8. Intermediate/advanced SQL: month-on-month changes in percentage points.
WITH monthly AS (
    SELECT order_month, 100.0 * SUM(is_late) / NULLIF(COUNT(*),0) AS late_rate_pct
    FROM fact_orders WHERE eligible_sla = 1 GROUP BY order_month
)
SELECT order_month, ROUND(late_rate_pct,2) AS late_rate_pct,
       ROUND(late_rate_pct - LAG(late_rate_pct) OVER (ORDER BY order_month),2)
           AS change_from_prior_month_pp
FROM monthly ORDER BY order_month;
