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
