# Days 1–2 workshop — setup, real data, and data understanding

**Target time:** 6–9 hours total across the first two days.

## Day 1: environment and real dataset
1. Open the extracted project folder in VS Code. Install the Python extension if needed.
2. In a PowerShell terminal, run the following commands:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python scripts/create_demo_data.py
python -m pytest -q
python -m delivery_investigation.cli run --raw-dir data/sample --output-dir outputs/demo --min-group-size 1
```

3. Demo outputs are **synthetic only**. Do not cite them as business evidence.
4. Download https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce and place these files into `data/raw/` without changing names:
   - `olist_orders_dataset.csv`
   - `olist_order_items_dataset.csv`
   - `olist_customers_dataset.csv`
   - `olist_sellers_dataset.csv`
   - `olist_order_reviews_dataset.csv`
5. Run the real dataset:

```powershell
python -m delivery_investigation.cli run --raw-dir data/raw --output-dir outputs/real
```

**Day 1 done:** tests pass, files exist, and real pipeline produces `outputs/real/data_quality.json` and `outputs/real/kpis.json`.

## Day 2: understand order granularity and quality
1. Examine which fields identify a unique order, a customer, a seller, an item, and a review.
2. Check whether one order may contain multiple items or multiple reviews. Explain why raw joins can duplicate orders.
3. Open `outputs/real/data_quality.json`: write down missing timestamps, excluded records, and any invalid stage sequences.
4. Read `docs/data_dictionary.md`, then outline the eligible delivered-order denominator and late definition.
5. Create `docs/analysis_log.md` with sections: Data source, data quality, questions, observations, validation, decisions.

**Day 2 done:** one-page schema/quality explanation written in your own words.

## Optional stretch (only if both days are complete)
Open `outputs/real/delivery_analytics.sqlite` and try the first SQL query from `sql/analysis_queries.sql`. Compare results to `kpis.json`.
