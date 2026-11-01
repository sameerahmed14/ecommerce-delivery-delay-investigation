# 14-day intensive roadmap — Delivery Performance Investigation

**Target:** finish a credible end-to-end data-analyst portfolio case study in 14 days.
**Pace:** 3–5 focused hours/day (roughly 42–70 hours). This is ambitious; spend more time on a day's evidence gate if needed rather than skipping validation.
**Final deliverables:** reproducible Python/SQL analysis; validated late-delivery KPIs; 2–3-page Power BI report; evidence-backed management memo; public GitHub case study without private/raw licensed data.

## Week 1 — Build the data foundation and investigate lateness

| Day | Practical tasks | New skills | Evidence gate |
|---|---|---|---|
| **1** | Set up VS Code/Python environment; run tests + synthetic demo; download 5 Olist CSVs | Virtual environments, project structure, data provenance | Tests pass; data files saved unmodified |
| **2** | Map table keys and one-to-many relationships; profile source tables | pandas profiling, keys, grain, missing values | Schema and data-quality notes recorded |
| **3** | Run and inspect real pipeline; audit eligibility and date definitions | SQL join cardinality, null handling, validation, timestamps | `data_quality.json` reviewed; one row/order verified |
| **4** | Independently calculate eligible, late, on-time orders using SQL | SELECT, WHERE, CASE, COUNT, CTEs, percentage denominators | SQL result reconciles with `kpis.json` |
| **5** | Analyse lateness by purchase month; inspect delay days | GROUP BY, date grouping, distributions, outliers | Monthly trend and limitations documented |
| **6** | Compare processing stages: order→approval→carrier→customer | Datetime differences, median versus mean, invalid sequence checks | Stage-duration comparison table with sample sizes |
| **7** | Summarise Week 1; select 2–3 strongest questions for deeper investigation | Analyst judgment, story selection, note-taking | One-page interim findings log; no causal overclaims |

## Week 2 — Test patterns, build dashboard, communicate decisions

| Day | Practical tasks | New skills | Evidence gate |
|---|---|---|---|
| **8** | Compare customer states and eligible single-seller groups | Segmentation, filtering, minimum volume thresholds | Region/seller comparisons include denominators |
| **9** | Explore late delivery and review-score association | JOIN, descriptive stats, response bias, confounding | Review comparison reports coverage and caveats |
| **10** | Run two sensitivity checks (e.g. segment volume cutoffs and timestamp exclusions) | Robustness checks, uncertainty, evidence standards | Check whether main findings change materially |
| **11** | Import curated tables to Power BI; build model and validated KPI measures | Power Query, relationships, DAX, filter contexts | Power BI KPI totals match SQL/Python |
| **12** | Finish executive, operations and customer-experience report pages | Power BI layout, slicers, storytelling | 2–3 pages, clear definitions and source period |
| **13** | Write business memo: findings, alternative explanations, priority actions, monitoring KPIs | Recommendation writing, prioritisation, avoiding causal fallacies | Each recommendation references verifiable evidence |
| **14** | QA dashboard/figures, polish README, publish portfolio and rehearse explanation | Git/GitHub, reproducibility, interview storytelling | Ready-to-show case study and 2-minute walkthrough |

## Non-negotiable scope
- Keep **one row per order** in the analysis fact table; never double-count order items/reviews.
- Late delivery = **actual delivery calendar date after estimated calendar date** among eligible delivered orders.
- Report missingness and exclusion reasons before claiming any rates.
- Seller comparison should use eligible **single-seller** orders and show group sample sizes.
- Describe associations, not proven causes (dataset lacks carrier exceptions and real-time tracking).
- Findings must be from **actual Olist data**, not the six-order synthetic demo.

## Deliberately postponed to keep the deadline
- ML delay prediction; web application; Airflow/cloud deployment; production API; real-time monitoring; automatic notifications; detailed causal attribution.
- Advanced confidence-interval and forecasting work can be optional, after the complete portfolio case study exists.

## First 60 minutes today
1. Unzip and open the project in VS Code.
2. Run setup/tests/demo from README. If PowerShell blocks activation, use a terminal configuration you control, or call the venv Python directly.
3. Download five official CSVs and place them under `data/raw/`.
4. Run the real pipeline and compare `data_quality.json` and `kpis.json`.
5. Record one question about the findings rather than immediately designing a dashboard.
