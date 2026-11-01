# Power BI dashboard blueprint (planned - not yet a .pbix file)

Import `outputs/real/fact_orders.csv` and use the one-order-per-row fact table for the first version. Do **not** join raw `order_items` or raw `reviews` into this fact without pre-aggregation: it multiplies orders and distorts the late rate.

## Starter measures (DAX)
```DAX
Eligible Delivered Orders = SUM(fact_orders[eligible_sla])
Late Orders = SUM(fact_orders[is_late])
On-Time Orders = SUM(fact_orders[is_on_time])
Late Delivery Rate = DIVIDE([Late Orders], [Eligible Delivered Orders])
On-Time Delivery Rate = DIVIDE([On-Time Orders], [Eligible Delivered Orders])
Orders With Reviews = COUNTROWS(FILTER(fact_orders, fact_orders[eligible_sla] = 1 && NOT ISBLANK(fact_orders[review_score_mean])))
Avg Review Score = CALCULATE(AVERAGE(fact_orders[review_score_mean]), fact_orders[eligible_sla] = 1)
```
Format rate measures as percentages in Power BI, **not** multiplied by 100 in DAX.

## Pages
1. **Executive overview**: eligible deliveries, late rate, on-time rate, late count; monthly trend and geographic distribution.
2. **Delay investigation**: pre-handoff vs in-transit duration distributions; missing/invalid timestamps prominently labelled; state and seller drilldowns.
3. **Customer experience**: average review scores and low-review rates by delivery status; sample sizes; no causal claims.
4. **Recommendations & limitations**: priority segments, tests proposed, assumed tradeoffs, absence of carrier IDs, historical data.

## Filters
Purchase month; customer state; single seller only when seller comparisons are shown; delivery group.

## Modeling upgrade (later)
Create `dim_purchase_date`, `dim_customer_geography` and `dim_single_seller` with one-to-many relationships to `fact_orders`; keep order-level grain. Consider multiple role-playing date dimensions for purchase and actual delivery dates. Follow Microsoft's star-schema guidance.

Official guidance: https://learn.microsoft.com/en-us/power-bi/guidance/star-schema

## Validation
Check that Power BI card totals agree exactly with `kpis.json` and `sql/analysis_queries.sql` before publishing. Label that only 2016-2018 historical Brazilian orders are included.
