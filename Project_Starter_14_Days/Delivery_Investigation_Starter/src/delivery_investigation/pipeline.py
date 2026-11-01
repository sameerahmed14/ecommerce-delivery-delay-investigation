"""Build a validated, one-row-per-order analytical dataset from Olist CSVs."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

FILES = {
    "orders": "olist_orders_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "items": "olist_order_items_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
}
REQUIRED = {
    "orders": ["order_id", "customer_id", "order_status", "order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"],
    "customers": ["customer_id", "customer_state", "customer_city"],
    "items": ["order_id", "order_item_id", "seller_id", "price", "freight_value"],
    "sellers": ["seller_id", "seller_state", "seller_city"],
    "reviews": ["order_id", "review_score"],
}
DATES = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]


def load_csvs(raw_dir: Path) -> dict[str, pd.DataFrame]:
    """Load five tables; fail clearly if the dataset is absent or malformed."""
    raw_dir = Path(raw_dir)
    missing = [filename for filename in FILES.values() if not (raw_dir / filename).exists()]
    if missing:
        raise FileNotFoundError(
            "Missing Olist CSVs in " + str(raw_dir) + ": " + ", ".join(missing)
            + ". Download the dataset from Kaggle (link in README)."
        )
    frames = {}
    for table, filename in FILES.items():
        df = pd.read_csv(raw_dir / filename, low_memory=False)
        absent = sorted(set(REQUIRED[table]) - set(df.columns))
        if absent:
            raise ValueError(f"{filename} missing required columns: {absent}")
        frames[table] = df
    for table, key in [("orders", ["order_id"]), ("customers", ["customer_id"]),
                       ("sellers", ["seller_id"]), ("items", ["order_id", "order_item_id"])]:
        if frames[table].duplicated(key).any():
            raise ValueError(f"Duplicated key in {table}: {key}; resolve before analysis")
    return frames


def _review_summary(reviews: pd.DataFrame) -> pd.DataFrame:
    rev = reviews[["order_id", "review_score"]].copy()
    rev["review_score"] = pd.to_numeric(rev["review_score"], errors="coerce")
    # A given order may have multiple review records. Never join the raw 1-to-many table to orders.
    return (rev.groupby("order_id", as_index=False)
            .agg(review_score_mean=("review_score", "mean"), review_count=("review_score", "count")))


def _item_summary(items: pd.DataFrame) -> pd.DataFrame:
    work = items[["order_id", "seller_id", "order_item_id", "price", "freight_value"]].copy()
    for col in ("price", "freight_value"):
        work[col] = pd.to_numeric(work[col], errors="coerce")
    per_order = (work.groupby("order_id", as_index=False)
        .agg(item_count=("order_item_id", "size"), seller_count=("seller_id", "nunique"),
             item_value_brl=("price", "sum"), freight_value_brl=("freight_value", "sum")))
    # Seller attribution is only possible unambiguously when an order has one unique seller.
    single = work.drop_duplicates(["order_id", "seller_id"])[["order_id", "seller_id"]]
    single_map = (single.groupby("order_id")["seller_id"].agg(
        lambda ids: ids.iloc[0] if len(ids) == 1 else None).rename("single_seller_id").reset_index())
    return per_order.merge(single_map, on="order_id", how="left", validate="one_to_one")


def build_fact_orders(frames: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, dict]:
    """Return one row per order and a transparent data-quality report."""
    orders = frames["orders"].copy()
    for col in DATES:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")
    customer = (frames["customers"][["customer_id", "customer_city", "customer_state"]]
                .rename(columns={"customer_city": "customer_city", "customer_state": "customer_state"}))
    sellers = frames["sellers"][["seller_id", "seller_city", "seller_state"]].rename(
        columns={"seller_id": "single_seller_id"})
    f = orders.merge(customer, how="left", on="customer_id", validate="many_to_one")
    f = f.merge(_item_summary(frames["items"]), how="left", on="order_id", validate="one_to_one")
    f = f.merge(sellers, how="left", on="single_seller_id", validate="many_to_one")
    f = f.merge(_review_summary(frames["reviews"]), how="left", on="order_id", validate="one_to_one")
    assert len(f) == len(orders), "Join altered order count"
    assert f["order_id"].is_unique, "Order grain violated"

    f["customer_state"] = f["customer_state"].fillna("Unknown")
    f["seller_state"] = f["seller_state"].fillna("Unknown")
    f["review_count"] = f["review_count"].fillna(0).astype(int)
    f["item_count"] = f["item_count"].fillna(0).astype(int)
    f["seller_count"] = f["seller_count"].fillna(0).astype(int)
    f["single_seller_order"] = (f["seller_count"] == 1).astype(int)
    f["is_delivered"] = f["order_status"].eq("delivered").astype(int)
    delivered = f["order_delivered_customer_date"]
    purchased = f["order_purchase_timestamp"]
    promised = f["order_estimated_delivery_date"]
    # Date-level comparison: the Olist estimate is a date, often midnight. A package
    # arriving at 18:00 on the promised date should count as on time.
    f["valid_delivery_chronology"] = (purchased.notna() & delivered.notna() &
                                       (delivered >= purchased)).astype(int)
    eligible = (f["is_delivered"].eq(1) & promised.notna() &
                f["valid_delivery_chronology"].eq(1))
    f["eligible_sla"] = eligible.astype(int)
    f["is_late"] = (eligible & (delivered.dt.normalize() > promised.dt.normalize())).astype(int)
    f["is_on_time"] = (eligible & f["is_late"].eq(0)).astype(int)
    days = (delivered.dt.normalize() - promised.dt.normalize()).dt.days
    f["late_days"] = days.where(eligible).clip(lower=0)
    f["order_month"] = purchased.dt.to_period("M").astype("string")
    f["purchase_date"] = purchased.dt.date.astype("string")

    approval = f["order_approved_at"]
    handoff = f["order_delivered_carrier_date"]
    def stage_days(start: pd.Series, end: pd.Series) -> pd.Series:
        delta = (end - start).dt.total_seconds() / 86400.0
        return delta.where(start.notna() & end.notna() & delta.ge(0))
    f["approval_days"] = stage_days(purchased, approval)
    f["pre_handoff_days"] = stage_days(approval, handoff)
    f["in_transit_days"] = stage_days(handoff, delivered)
    f["end_to_end_days"] = stage_days(purchased, delivered)
    f["bad_stage_sequence"] = (
        ((approval < purchased) & approval.notna() & purchased.notna()) |
        ((handoff < approval) & handoff.notna() & approval.notna()) |
        ((delivered < handoff) & delivered.notna() & handoff.notna())
    ).astype(int)

    audit = {
        "source_order_rows": int(len(orders)),
        "fact_order_rows": int(len(f)),
        "eligible_delivered_orders": int(eligible.sum()),
        "late_orders": int(f["is_late"].sum()),
        "excluded_from_sla": int((~eligible).sum()),
        "delivered_missing_actual_date": int((f["is_delivered"].eq(1) & delivered.isna()).sum()),
        "delivered_missing_estimated_date": int((f["is_delivered"].eq(1) & promised.isna()).sum()),
        "delivered_invalid_chronology": int((f["is_delivered"].eq(1) & f["valid_delivery_chronology"].eq(0)).sum()),
        "orders_with_bad_stage_sequence": int(f["bad_stage_sequence"].sum()),
        "orders_without_customer_match": int(f["customer_city"].isna().sum()),
        "orders_without_items": int(f["item_count"].eq(0).sum()),
        "orders_with_multiple_sellers": int(f["seller_count"].gt(1).sum()),
        "orders_without_review": int(f["review_count"].eq(0).sum()),
    }
    return f, audit
