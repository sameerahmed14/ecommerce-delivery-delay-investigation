# Why Are Customers Receiving Orders Late?
### A data-driven Olist e-commerce delivery investigation

**Project status: Day 1 starter ready - repository, data-quality rules, pipeline and analyses scaffolded.**

**Business question:** Which delivered orders missed their promised delivery date, which observed factors are associated with delays, and how does late delivery relate to customer reviews?

## Evidence boundary
- Use the historical, anonymized **Olist Brazilian E-Commerce Public Dataset**, approximately 100k orders from **2016-2018**. Source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- The downloaded raw CSVs are **not included in this repository**. Obtain them from the source and observe the source's licensing conditions.
- `data/sample/` contains **six synthetic orders** solely to run and test the code. Do not use demo data as empirical findings.
- Public data has **no reliable carrier identity, exception reason, real-time tracking, or experimental assignment**. We can study stage duration associations, not prove why a courier failed.

## Get started (Windows / VS Code)
```powershell
cd Delivery_Investigation_Starter
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python scripts/create_demo_data.py
python -m pytest -q
python -m delivery_investigation.cli run --raw-dir data/sample --output-dir outputs/demo --min-group-size 1
```

Now load **actual Olist data**:
1. Download and unzip the official dataset from Kaggle.
2. Copy the **five** CSVs below into `data/raw/` (keep original filenames).
3. Run:
```powershell
python -m delivery_investigation.cli run --raw-dir data/raw --output-dir outputs/real
```

Required files:
- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_customers_dataset.csv`
- `olist_sellers_dataset.csv`
- `olist_order_reviews_dataset.csv`

## Outputs
`outputs/real/` contains `fact_orders.csv`, `delivery_analytics.sqlite`, `kpis.json`, `data_quality.json`, and group summaries: `monthly.csv`, `customer_states.csv`, `single_sellers.csv`, `reviews.csv`, `stages.csv`.

The analytic fact contains **exactly one row per order**. Duplicate reviews are aggregated to an order-level mean; item records are first aggregated to order level; multi-seller orders are **not assigned** to a single seller.

## Business rules (don't skip)
1. Eligible denominator: `order_status='delivered'`, actual delivery and promised delivery timestamps present, and delivery is not before purchase.
2. **Late** means `DATE(actual_delivery) > DATE(estimated_delivery)`, not clock time on the same promised day.
3. Canceled or incomplete orders do **not** enter the late-delivery denominator. Their exclusions are reported.
4. Stage durations with absent or reversed timestamps are marked unknown, not silently treated as zero.
5. Seller comparisons only include single-seller orders and minimum sample-size checks. A seller association is **not** proof the seller caused a delay.
6. Review comparisons are descriptive, not causal. Data are historic and anonymized.

## Project plan and learning
**14-day sprint (3–5 hours per day).** Follow `docs/learning_roadmap.md` for the day-by-day plan, and begin with `docs/days_01_02_workshop.md`. The priority is an **evidence-led SQL + Python investigation, 2–3-page Power BI report, and decision memo**. Machine-learning and production scheduling are deferred. Also see `docs/data_dictionary.md` and `docs/power_bi_blueprint.md`. Full updated report is provided separately as Word/PDF.

## Code structure
```
src/delivery_investigation/pipeline.py  # load, validate, transform
src/delivery_investigation/analysis.py  # group, compare, summarise
src/delivery_investigation/cli.py       # run and export
sql/analysis_queries.sql               # auditable SQL queries
tests/test_pipeline.py                 # sample business-rule checks
docs/                               # roadmap, data dictionary and BI design
```

## Next milestones
- Run on official Olist data and profile missing values/statuses.
- Reconcile SQL figures with Python outputs.
- Explore demand/mix/geography, compare temporal stage differences, test robustness.
- Construct a Power BI report with validated DAX, sample-size guardrails and caveats.
- Write the **final findings section only after** evaluating real data.

## References
- Olist data: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- Microsoft star schema: https://learn.microsoft.com/en-us/power-bi/guidance/star-schema
- pandas datetime parsing: https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
