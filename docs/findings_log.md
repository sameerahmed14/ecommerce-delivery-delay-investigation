# E-Commerce Delivery Delay Investigation
## Findings Log — Work in Progress

**Dataset:** Olist Brazilian E-Commerce (historical 2016–2018 data)
**Objective:** Investigate late deliveries, identify associated operational factors, and develop evidence-based recommendations.

## Finding 1 — Overall Delivery Performance

- Original orders: 99,441
- Eligible delivered orders: 96,470
- Late deliveries: 6,534
- Late delivery rate: 6.77%
- On-time deliveries: 89,936
- Mean delay among late orders: 10.62 days

Validation: Independent calendar-date classification returned 6,534 late orders with zero classification mismatches.

## Finding 2 — Delivery Stage Investigation

Median durations for late versus on-time orders:

| Stage | Late | On time |
|---|---:|---:|
| Approval | 24.3 min | 20.4 min |
| Pre-carrier handoff | 3.07 days | 1.79 days |
| In transit | 26.20 days | 6.95 days |

Interpretation: Longer transit durations are strongly associated with lateness. These descriptive differences do not establish carrier responsibility.

## Finding 3 — Monthly Delivery Deterioration

Orders grouped by purchase month:

| Month | Eligible orders | Late orders | Late rate |
|---|---:|---:|---:|
| November 2017 | 7,288 | 904 | 12.40% |
| February 2018 | 6,555 | 926 | 14.13% |
| March 2018 | 7,003 | 1,328 | 18.96% |

March 2018 had the highest late rate among months with at least 100 eligible orders.

## Finding 4 — Rio de Janeiro

| Metric | March 2018 | April 2018 |
|---|---:|---:|
| Orders | 864 | 807 |
| Late rate | 34.49% | 4.83% |
| Median transit duration | 17.99 days | 9.03 days |
| Median promised duration | 27.33 days | 31.09 days |
| Median actual duration | 21.22 days | 12.02 days |
| Over 7 days late | 24.31% | 2.35% |

Interpretation: Faster actual deliveries and longer promised windows both accompanied the April improvement. Their individual contributions remain unproven.

## Finding 5 — Delivery Commitment Analysis

Bahia's median actual delivery time stayed approximately 21.1 days in March and April, while its median promised window increased from 25.46 to 27.57 days.

Its late rate fell from 31.49% to 18.52%.

Hypothesis: Delivery commitments may influence measured punctuality independently of actual operational speed.

## Finding 6 — Severe Delays

Among RJ orders purchased in March 2018:
- 298 orders were late.
- 210 orders were more than seven calendar days late.
- The 90th percentile of actual delivery duration was 43.66 days.

April's severe-delay rate was only 2.35%, compared with 24.31% in March.

## Open Research Questions

- Were late deliveries concentrated on specific seller-to-customer routes?
- Were slow dispatch or transit stages responsible for particular patterns?
- Did promised delivery windows vary across regions and months?
- Were late orders associated with lower customer review scores?

## Research Limitations

Results are observational, not causal. The dataset does not provide complete carrier tracking, service-level contracts or operational incident records.

All findings are from a historical public dataset, not a live company deployment.

## Finding 7 — Seller Location and Rio de Janeiro Delivery Performance

### Research Question
Were Rio de Janeiro's February–March 2018 delays concentrated among orders from sellers in particular states?

### Scope
Eligible single-seller orders delivered to Rio de Janeiro customers, grouped by seller state and purchase month.

### SP Seller to RJ Customer Performance

| Metric | February 2018 | March 2018 | April 2018 |
|---|---:|---:|---:|
| Orders | 563 | 582 | 550 |
| Late deliveries | 222 | 247 | 32 |
| Late rate | 39.43% | 42.44% | 5.82% |
| Severe delays | 137 | 178 | 17 |
| Severe delay rate | 24.33% | 30.58% | 3.09% |
| Median transit days | 17.11 | 22.12 | 9.17 |

### Key Findings
1. SP sellers accounted for 247 of the 298 late orders recorded among all eligible RJ customer orders purchased in March 2018 (82.9%).
2. Median SP-to-RJ transit duration was 22.12 days in March, falling to 9.17 days in April.
3. In March, SP sellers had a 42.44% late rate, compared with 5.88% for RJ sellers serving RJ customers.
4. Severe-delay rates for SP-to-RJ orders decreased from 30.58% in March to 3.09% in April.

### Business Interpretation
Orders associated with SP sellers contributed disproportionately to RJ's late-delivery volume during March 2018. This seller-state group should be prioritised for investigation of dispatch timelines, transportation performance and delivery commitments.

### Limitations
Seller registered location may differ from physical dispatch location. Analysis is observational and limited to eligible single-seller orders. No specific carrier-level cause has been established.

### Next Steps
Investigate promised delivery windows, pre-handoff durations and transit-time distributions for SP-to-RJ orders.

### Reproducibility
Script: analysis/rj_seller_routes.py within the Python starter project.
Source: Olist Brazilian E-Commerce Dataset.

## Finding 8 — SP to RJ Delivery Diagnostics

### Business Question
What factors were associated with the sharp improvement in delivery performance between March and April 2018?

### Dataset Scope
Eligible single-seller orders purchased February to April 2018, with sellers registered in Sao Paulo (SP) and customers in Rio de Janeiro (RJ).

### Results

| Metric | March 2018 | April 2018 |
|---|---:|---:|
| Orders | 582 | 550 |
| Late orders | 247 | 32 |
| Late rate | 42.44% | 5.82% |
| Severe delay rate | 30.58% | 3.09% |
| Median actual delivery days | 25.39 | 12.39 |
| Median transit days | 22.12 | 9.17 |
| Median pre-handoff days | 2.09 | 1.44 |
| Median promised days | 30.07 | 32.08 |
| 90th percentile transit days | 41.88 | 22.68 |

### Key Findings

1. Median actual delivery duration decreased by 13 days.
2. Median transportation duration decreased by 12.95 days.
3. Median promised delivery duration increased by 2.01 days.
4. Late-delivery rate decreased by 36.62 percentage points.
5. Severe-delay rate decreased by 27.49 percentage points.
6. The 90th percentile of transit duration fell by 19.20 days.

### Business Interpretation

The improvement in April was associated with substantially shorter transportation and actual delivery durations. Modestly longer delivery commitments may also have contributed to better on-time performance.

### Recommendation for Further Investigation

Prioritise examining the transportation-stage performance of SP-to-RJ orders, especially unusually long transit durations. Review delivery estimates alongside actual performance to distinguish operational improvement from more generous commitments.

### Limitations

Observational analysis cannot establish causation. Seller registration state may differ from the actual dispatch location. Carrier event-level records are unavailable.

### Reproducibility

Python script:
Project_Starter_14_Days/Delivery_Investigation_Starter/analysis/sp_rj_diagnostics.py

Output:
outputs/real/sp_rj_diagnostics.csv (generated locally).


## Finding 9 — Delivery Delays and Customer Satisfaction

### Research Question
Are late deliveries associated with lower customer review scores?

### Scope
96,470 eligible delivered orders; 95,824 orders have valid review scores.

### Overall Results

| Delivery category | Reviewed orders | Average score | Low-rating rate |
|---|---:|---:|---:|
| On time | 89,443 | 4.29 | 9.23% |
| 1-7 days late | 3,600 | 2.72 | 49.36% |
| Over 7 days late | 2,781 | 1.70 | 79.18% |

Low ratings are defined as review scores of 1-2.

### SP to RJ Customer Experience

| Metric | March 2018 | April 2018 |
|---|---:|---:|
| Reviewed orders | 572 | 544 |
| Average review score | 2.97 | 4.08 |
| Low-rating rate | 42.83% | 15.99% |
| Late rate among reviewed orders | 41.61% | 5.70% |

### Key Findings

1. Average scores decreased as delivery delays became more severe.
2. Severely delayed reviewed orders had approximately 8.6 times the low-rating rate of reviewed on-time orders.
3. SP-to-RJ customer reviews improved in April, alongside a substantial improvement in delivery performance.
4. Review coverage was approximately 99.33% overall.

### Business Interpretation

The evidence supports prioritising delivery performance as a customer experience issue. Reducing severe delays could be relevant to improving satisfaction, but a causal effect has not been established.

### Limitations

- Correlation does not establish causation.
- Product quality, seller service and other factors may affect ratings.
- Missing reviews may introduce selection bias.
- Review scores are aggregated at order level using review_score_mean.
- Historical public data, not live operational performance.

### Next Steps

Evaluate missing-review patterns, verify review aggregation, and conduct statistical validation of the relationship.

### Reproducibility

Python script:
Project_Starter_14_Days/Delivery_Investigation_Starter/analysis/customer_satisfaction.py

