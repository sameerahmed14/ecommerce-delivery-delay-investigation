# Why Are Customers Receiving Orders Late?
## A Data-Driven Investigation into E-Commerce Delivery Performance and Customer Satisfaction

**Project type:** End-to-end data analytics portfolio case study  
**Dataset:** Olist Brazilian E-Commerce Public Dataset (historical orders, 2016–2018)  
**Tools:** Python, pandas, SQL/SQLite, SciPy, Power BI, DAX and GitHub  
**Status:** Final analytical findings and recommendations; operational root causes not independently verified  
**Prepared:** November 2026

> **Evidence boundary:** This is an independent analysis of a public historical dataset, not an engagement commissioned by Olist or a live operational intervention. All recommendations are proposals for further testing; they are not documented improvements made by the company.

## 1. Executive summary

The analysis investigated **96,470 eligible delivered orders** out of **99,441 original orders** and found **6,534 late deliveries**, a **6.77% late-delivery rate**. Late orders tended to have much longer transportation durations than on-time orders: **26.20 days versus 6.95 days** in median recorded transit time. This relationship justified investigating geography, seller origin, order timing and delivery commitments.

Delivery performance was particularly weak for orders **purchased in March 2018**, when **1,328 of 7,003 eligible orders arrived late (18.96%)**. Rio de Janeiro (RJ) was a major area of concern: **298 of 864** eligible RJ customer orders purchased that month were late (**34.49%**), including **210 orders delivered more than seven calendar days after the estimated date**.

A focused analysis of eligible **single-seller orders** found that **247 of those 298 late RJ orders** were associated with sellers registered in São Paulo (SP). The SP-seller-to-RJ-customer group recorded a **42.44%** late rate in March 2018, compared with **5.82%** in April. Median recorded transit duration for that group declined from **22.12** to **9.17 days** over the same period. This is strong descriptive evidence for prioritising transportation-stage investigation, but it does **not** establish a specific carrier, logistics event or causal explanation.

Customer satisfaction also varied sharply by delivery severity. Low review ratings (1–2 stars) appeared in **9.23%** of reviewed on-time orders, **49.36%** of reviewed orders arriving 1–7 days late, and **79.18%** of reviewed orders arriving more than seven days late. A chi-square test found a statistically significant association (**χ²(2) = 16,343.91, p < 0.001; Cramér's V ≈ 0.413**). This is an association, not proof that delays alone caused customer dissatisfaction.

**Management implication:** Investigate the SP-seller/RJ-customer segment first, monitor unusually long transit times and severe delays, and evaluate delivery promises alongside actual end-to-end performance. Treat customer review outcomes as a complementary service-quality measure.

## 2. Business question and objectives

**Primary question:** Why do customer orders miss their estimated delivery date, where are the largest and most severe problems concentrated, and what evidence-based actions should an e-commerce business consider?

The analysis sought to:

1. Establish an auditable, order-level definition of late delivery.
2. Measure delay frequency, severity and trends over purchase months.
3. Compare recorded approval, pre-carrier handoff and transportation stages.
4. Identify customer-state and seller-state groups requiring attention.
5. Check whether promised delivery windows help explain changing punctuality.
6. Assess the relationship between delay severity and customer ratings.
7. Translate findings into prioritised, testable operational recommendations.

## 3. Data and analytical methods

### 3.1 Data sources and grain

The public [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) supplied five input tables: orders, order items, customers, sellers and order reviews. Python aggregated order items and reviews before joining to produce an analytical fact table with **one row per order**. When an order had more than one review record, the pipeline calculated an **order-level mean review score**. Seller-state attribution was restricted to **single-seller orders** for route comparisons.

### 3.2 KPI definitions

| Measure | Definition |
|---|---|
| Eligible order | Delivered order with actual and estimated delivery dates and valid purchase-to-delivery chronology |
| Late delivery | Actual delivery **calendar date** after estimated delivery **calendar date** |
| Late rate | Late eligible orders / all eligible delivered orders |
| Severe delay | Actual delivery more than **7 calendar days** after the estimated date |
| Pre-carrier handoff | Recorded approval timestamp to carrier-handoff timestamp, for valid sequences |
| Transit duration | Recorded carrier-handoff timestamp to actual delivery timestamp, for valid sequences |
| Promised duration | Purchase timestamp to estimated delivery timestamp |
| Actual duration | Purchase timestamp to actual delivery timestamp |
| Low rating | Valid order-level mean review score of **2 or less**, out of 5 |
| Purchase month | Month of order purchase, **not** the month of customer delivery |

Stage durations with missing or negative intervals were excluded from the relevant duration statistics instead of being set to zero. Comparisons by seller location refer to the seller's registered state; that does not necessarily indicate the dispatch warehouse or actual shipping route.

### 3.3 Quality assurance

- The pipeline preserved one record per original order and passed four starter automated tests.
- **96,470** of **99,441** orders met the defined delivery-KPI eligibility criteria; **2,971** did not.
- An independent calendar-date comparison reproduced **6,534** late orders with **zero classification mismatches**.
- Valid reviews were present for **95,824 of 96,470** eligible delivered orders (**99.33% coverage**).
- Review coverage was **99.45%** among on-time orders and **97.66%** among late orders; potential missing-review bias is therefore relevant.
- Power BI KPI totals and key subgroup results were cross-checked against Python/SQL outputs.

The exclusion counts for distinct data-quality problems can overlap and should not be summed without checking their definitions.

## 4. Findings

### 4.1 Overall delivery performance and stage differences

| Metric | Result |
|---|---:|
| Original orders | 99,441 |
| Eligible delivered orders | 96,470 |
| Late deliveries | 6,534 |
| On-time deliveries | 89,936 |
| Late-delivery rate | 6.77% |
| Average delay among late orders | 10.62 days |

| Recorded stage (median) | Late orders | On-time orders |
|---|---:|---:|
| Approval | 24.3 minutes | 20.4 minutes |
| Pre-carrier handoff | 3.07 days | 1.79 days |
| In transit | 26.20 days | 6.95 days |

The median transit duration differed much more between late and on-time groups than the median approval duration. Because the groups were defined using delivery outcomes, these comparisons describe association and cannot by themselves isolate a root cause.

### 4.2 A pronounced March 2018 spike

| Purchase month | Eligible orders | Late orders | Late rate |
|---|---:|---:|---:|
| November 2017 | 7,288 | 904 | 12.40% |
| February 2018 | 6,555 | 926 | 14.13% |
| **March 2018** | **7,003** | **1,328** | **18.96%** |

March 2018 had the highest late-delivery rate among purchase months with at least 100 eligible orders in this investigation. Months with extremely small denominators were excluded from performance rankings to avoid misleading percentage comparisons.

### 4.3 Rio de Janeiro: high severity, then improvement

| RJ customers; purchase month | March 2018 | April 2018 |
|---|---:|---:|
| Eligible orders | 864 | 807 |
| Late orders | 298 | 39 |
| Late rate | 34.49% | 4.83% |
| Orders more than 7 days late | 210 | 19 |
| Severe-delay rate | 24.31% | 2.35% |
| Median transit duration | 17.99 days | 9.03 days |
| Median promised duration | 27.33 days | 31.09 days |
| Median actual duration | 21.22 days | 12.02 days |

RJ's severe-delay rate dropped by **21.96 percentage points** between March and April. The 90th percentile of actual end-to-end delivery duration also declined, from **43.66** to **25.04 days**. Both faster actual deliveries and more generous estimated windows accompanied the observed improvement.

### 4.4 SP seller → RJ customer segment is a priority for investigation

The following segment uses eligible single-seller orders and the seller's registered state.

| SP sellers → RJ customers | February 2018 | March 2018 | April 2018 |
|---|---:|---:|---:|
| Eligible orders | 563 | 582 | 550 |
| Late orders | 222 | 247 | 32 |
| Late rate | 39.43% | 42.44% | 5.82% |
| Severe-delay rate | 24.33% | 30.58% | 3.09% |
| Median transit duration | 17.11 days | 22.12 days | 9.17 days |
| 90th-percentile transit duration | 41.95 days | 41.88 days | 22.68 days |
| Median actual duration | 20.33 days | 25.39 days | 12.39 days |
| Median promised duration | 23.19 days | 30.07 days | 32.08 days |
| Median pre-handoff duration | 2.21 days | 2.09 days | 1.44 days |

In March, the SP-seller/RJ-customer segment accounted for **247 of the 298** late eligible RJ customer orders (**82.9% of the broader RJ late-order count**). This contribution share is different from the **42.44% late rate** *within* the SP→RJ segment.

Between March and April, the segment's late rate fell by **36.62 percentage points**, median actual delivery duration fell by **13.00 days**, and median transit duration fell by **12.95 days**. The estimated delivery window increased by **2.01 days**. These simultaneous changes mean it would be incorrect to attribute the entire punctuality improvement to any one factor based only on these aggregate comparisons.

### 4.5 Delivery promises matter alongside physical delivery speed

The Bahia (BA) comparison offers a useful counterexample: median actual delivery duration was nearly unchanged from March to April 2018 (**21.14 versus 21.11 days**), while median promised duration increased from **25.46 to 27.57 days** and late rate fell from **31.49% to 18.52%**. This supports further testing of promise-setting behaviour, not a conclusion that extending delivery promises is the best solution. Customers may prefer accurate *and* fast delivery, rather than simply more distant commitments.

### 4.6 Severe delays are associated with lower customer reviews

| Delivery severity | Valid reviewed orders | Average score / 5 | Low-rating rate (1–2 stars) |
|---|---:|---:|---:|
| On time | 89,443 | 4.29 | 9.23% |
| 1–7 days late | 3,600 | 2.72 | 49.36% |
| Over 7 days late | 2,781 | 1.70 | 79.18% |

The low-rating rate for reviewed orders over seven days late was approximately **8.6 times** the corresponding rate for reviewed on-time orders.

For SP-seller/RJ-customer reviewed orders, average ratings rose from **2.97** in March 2018 to **4.08** in April, while low-rating rates fell from **42.83% to 15.99%**. The corresponding late rate among *reviewed orders* fell from **41.61% to 5.70%**. These are reviewed-subset statistics and should not be confused with the all-eligible-order route late rates.

A chi-square test of independence comparing delivery-severity groups with low versus non-low ratings gave **χ²(2) = 16,343.91, p < 0.001**, and **Cramér's V ≈ 0.413**. The display of p = 0 in some software output reflects numerical underflow, not a literally zero probability. Statistical significance does not demonstrate causation.

## 5. Prioritised business recommendations

These are **proposals** based on observed associations, not changes implemented or proven to produce savings.

| Priority | Recommended action | How to test and monitor it |
|---|---|---|
| **1 — Immediate diagnostic focus** | Review SP-seller/RJ-customer fulfilment and carrier-handoff-to-delivery records, especially the exceptionally slow shipments. | Obtain shipment event scans, carrier IDs, dispatch facilities and exception reasons; track median and p90 transit days, late rate and severe-delay rate by actual route. |
| **2 — Service-level accuracy** | Compare promised delivery windows with observed end-to-end distributions by region, seller and season. Avoid improving on-time metrics merely by making promises unnecessarily long. | Track both *actual delivery speed* and *promise accuracy*; assess customer expectations and conversion impacts before revising commitments. |
| **3 — Severe-delay escalation** | Identify orders at risk of exceeding estimated delivery by more than seven days and investigate unresolved cases proactively. | Introduce risk flags and a triage queue; track severe-delay rate, flagged-order precision and resolution time. |
| **4 — Customer-experience monitoring** | Monitor valid-review coverage, average ratings and low-rating shares by delivery severity. | Report counts alongside rates, control for geography/product/seller mix, and test targeted interventions before claiming customer-satisfaction improvements. |
| **5 — Data quality and governance** | Maintain one-order-one-row transformations, valid timestamp rules and documented KPI definitions. | Run automated tests, monitor missing timestamps and reconcile SQL, Python and Power BI output regularly. |

**Suggested scorecard:** eligible orders, late orders, late rate, severe-delay rate, median/p90 transit days, median promised and actual days, review coverage and low-rating rate. For all segmented metrics, display denominators and minimum sample-size requirements.

## 6. Limitations and next evidence required

- The dataset covers historical Brazilian e-commerce transactions and is **not real-time**.
- Seller registration state is not a verified dispatch origin or carrier route.
- No complete carrier event history, courier identity, shipping disruption record or delivery-contract SLA is available. The study cannot identify the operational root cause of a particular shipment failure.
- Correlations may reflect geography, product mix, seasonality, promise-setting or other confounders.
- Calendar-date lateness treats delivery on the estimated date as on time regardless of clock time; another business could use a different SLA.
- Multiple reviews for one order are averaged into an order-level score; this may differ from an analysis of individual review events.
- Late orders have slightly lower review coverage than on-time orders, so missingness may bias rating comparisons.
- The chi-square test demonstrates association but does not adjust for seller, region or month; adjusted comparisons and confidence intervals are valuable extensions.
- These findings do not support unverified claims of realised revenue gains, cost reductions, courier faults or causal intervention effects.

## 7. Reproducibility and deliverables

All results should be reproduced using the **real Olist CSVs**, not the six-order synthetic example data bundled with the starter repository.

1. Download the five source CSVs listed in the [starter README](../Project_Starter_14_Days/Delivery_Investigation_Starter/README.md).
2. From the Python project directory, install the dependencies and run `python -m pytest -q`.
3. Run the pipeline:
   ```powershell
   python -m delivery_investigation.cli run --raw-dir data/raw --output-dir outputs/real
   ```
4. Run the saved investigation scripts from the project directory:
   ```powershell
   python analysis/rj_seller_routes.py
   python analysis/sp_rj_diagnostics.py
   python analysis/customer_satisfaction.py
   python analysis/statistical_validation.py
   ```
5. Compare generated tables with [the findings log](../docs/findings_log.md), then open the [four-page Power BI dashboard](../Project_Starter_14_Days/Delivery_Investigation_Starter/dashboards/Delivery_Performance_Dashboard.pbix).

**Deliverables:** tested Python ETL pipeline; auditable analytical scripts and SQL; investigation findings log; four-page interactive Power BI report covering Executive Overview, Regional & Seller Performance, Delivery Diagnostics and Customer Satisfaction; and this business report.

## 8. Conclusion

The investigation identified a substantial March 2018 delivery-performance deterioration, concentrated in part among orders associated with SP sellers and RJ customers. Dramatically shorter transit durations accompanied improved punctuality in April. Severe lateness was also strongly associated with lower customer ratings. The appropriate business response is to **investigate specific operational handoffs and shipping records, monitor severe delays, and assess delivery-promise accuracy**, rather than claim a root cause unsupported by the available data.

---

*Analysis based on the public Olist dataset. This case study presents observed relationships, not verified operational interventions. Values are rounded where indicated.*
