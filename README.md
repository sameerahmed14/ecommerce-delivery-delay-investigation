# Why Are Customers Receiving Orders Late?
### E-commerce delivery performance & customer satisfaction — end-to-end data analytics portfolio case study

**Tools:** Python · pandas · SQL/SQLite · SciPy · Power BI · DAX · Git/GitHub  
**Dataset:** Historical, anonymised [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (2016–2018)

> **Business question:** Which orders miss the estimated delivery date, where are delays concentrated, which observable stages accompany late delivery, and how does delivery performance relate to customer reviews?

## Explore the project

- 📊 **[Power BI dashboard (4 pages)](Project_Starter_14_Days/Delivery_Investigation_Starter/dashboards/Delivery_Performance_Dashboard.pbix)** — interactive desktop report: Executive Overview; Regional & Seller Performance; Delivery Diagnostics; Customer Satisfaction
- 📄 **[Final business investigation report](reports/Final_Business_Investigation_Report.md)** — evidence, methods, recommendations, limitations and reproducibility
- 🔍 **[Findings log](docs/findings_log.md)** — individual investigations and validated observations
- 🧪 **[Methodology and KPI definitions](docs/methodology.md)** — definitions and eligibility decisions
- 🐍 **[Code and setup instructions](Project_Starter_14_Days/Delivery_Investigation_Starter/README.md)** — pipeline, analysis scripts, tests, SQL and data instructions

**Note:** GitHub stores the `.pbix` report but does not render its interactive pages in the browser; open the file in Power BI Desktop. Screenshots may be added separately for browser-only previews.

## Key findings

| Metric | Result |
|---|---:|
| Eligible delivered orders | **96,470** |
| Late deliveries | **6,534** |
| Overall late rate | **6.77%** |
| March 2018 late rate (orders purchased that month) | **18.96%** |
| March 2018 RJ customer late rate | **34.49%** |
| March 2018 SP-seller → RJ-customer late rate, single-seller orders | **42.44%** |
| April 2018 SP-seller → RJ-customer late rate | **5.82%** |

- Of the **298** late orders purchased by RJ customers in March 2018, **247** were associated with SP sellers in the single-seller analysis (**82.9% of the broader RJ late-order count**).
- Median transit duration for the SP-seller → RJ-customer group fell from **22.12 days in March** to **9.17 days in April**.
- Among reviewed orders, low ratings (1–2 stars) appeared in **9.23%** of on-time deliveries versus **79.18%** of deliveries more than seven days late.
- A chi-square test found a statistically significant **association**, not causation: **χ²(2) = 16,343.91; p < 0.001**.

## Analytical workflow

1. **Data validation and preparation:** Join five Olist tables to an order-grain fact table; check keys, timestamps and delivery eligibility.
2. **SQL and Python investigation:** Analyse delivery KPIs, stages, months, locations and seller-state segments.
3. **Customer satisfaction and statistics:** Compare review scores, review coverage and severe-delay groups; run a chi-square association test.
4. **Power BI reporting:** Reproduce validated KPIs and present findings across four report pages.
5. **Business recommendations:** Prioritise investigative actions while separating evidence from unverified hypotheses.

## Reproduce the analysis

The public raw dataset is **not** stored in this repository. Follow the [starter setup guide](Project_Starter_14_Days/Delivery_Investigation_Starter/README.md) to download the five original CSVs into `data/raw/`.

From `Project_Starter_14_Days/Delivery_Investigation_Starter`:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest -q
python -m delivery_investigation.cli run --raw-dir data/raw --output-dir outputs/real
python analysis/rj_seller_routes.py
python analysis/sp_rj_diagnostics.py
python analysis/customer_satisfaction.py
python analysis/statistical_validation.py
```

## Scope and limitations

This is a **historical public-data portfolio investigation**, not a commissioned operational study. Seller state is not necessarily the physical dispatch origin. The data does not reveal complete courier-level event histories or reasons for disruptions. Delivery groups and customer reviews can be **associated** without proving that one caused the other. No real cost savings or service improvements were implemented or verified.

**Suggested next operational test:** review carrier-event logs for the SP-seller/RJ-customer segment, monitor the 90th-percentile transit duration and severe-delay rate, and assess delivery-promise accuracy alongside actual speed.
