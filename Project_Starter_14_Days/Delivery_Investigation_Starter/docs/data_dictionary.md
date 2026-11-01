# Analytical data dictionary and granularity

**Primary analytical table:** `fact_orders` — exactly one record per `order_id`; analysis never divides a raw join of orders × items × reviews.

| Field | Meaning | Use/caution |
|---|---|---|
| `order_id` | Unique order ID | Fact primary key |
| `order_status` | Order status | Only delivered population is SLA-eligible |
| `order_purchase_timestamp` | Purchase timestamp | For chronology and order month |
| `order_approved_at` | Approval timestamp | Optional pre-dispatch stage |
| `order_delivered_carrier_date` | Handoff to logistics partner | Date provided, not carrier ID |
| `order_delivered_customer_date` | Delivery timestamp | Actual delivery date |
| `order_estimated_delivery_date` | Customer's estimated delivery date | Compare dates, not times |
| `eligible_sla` | 1 if delivered, promised and actual dates present, and delivery >= purchase | Denominator for late rate |
| `is_late` | 1 if eligible and delivered calendar date > estimated calendar date | Sum over eligible denominator |
| `is_on_time` | 1 if eligible and not late | Sum over eligible denominator |
| `late_days` | Nonnegative whole calendar days after estimated date | Null for ineligible |
| `bad_stage_sequence` | Reversed known timestamps within processing stages | Exclude invalid durations; retain separate audit |
| `approval_days` | Days from purchase to approval | Null for missing/negative |
| `pre_handoff_days` | Days from approval to carrier handoff | Null for missing/negative |
| `in_transit_days` | Days from handoff to customer delivery | Null for missing/negative |
| `end_to_end_days` | Days from purchase to delivery | Null for missing/negative |
| `customer_state` | Customer's state (Brazilian abbreviations) | Descriptive grouping |
| `single_seller_id` | Seller ID only if exactly one seller for order | Avoid seller attribution on multi-seller orders |
| `seller_count` | Number of distinct sellers associated with order | Multi-seller alert |
| `review_score_mean` | Mean of available numeric scores for all reviews of an order | May mask multiple reviews; reviewed-only |
| `review_count` | Number of numeric scores for an order | Review coverage |
| `freight_value_brl` | Sum of item-level freight charges, BRL | Charges, not shipping company cost/profit |
| `item_value_brl` | Sum of order-item prices, BRL | Not net revenue or profit |

## Cautions
- `shipping_limit_date` is in raw items; it can be used in Phase 3 to investigate fulfilment deadlines, but requires attention to item-level versus order-level semantics.
- Do not infer precise kilometres from seller/customer state. Geo enrichment would require defensible geocoding.
- Date precision/timezone assumptions must be documented; current pipeline works with supplied wall-clock timestamps and calendar dates.
- `order_month` is based on purchase month, not delivery month.
