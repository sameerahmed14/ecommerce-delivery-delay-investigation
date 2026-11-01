
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "outputs" / "real" / "fact_orders.csv"
OUTPUT = ROOT / "outputs" / "real"

df = pd.read_csv(DATA)

# Convert important columns
for col in [
    "eligible_sla",
    "is_late",
    "single_seller_order",
    "review_score_mean"
]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

for col in [
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# Keep orders eligible for delivery analysis
df = df[df["eligible_sla"] == 1].copy()

# Calculate delay in calendar days
df["delay_days"] = (
    df["order_delivered_customer_date"].dt.normalize()
    - df["order_estimated_delivery_date"].dt.normalize()
).dt.days

# Classify orders by delay severity
df["delay_category"] = np.select(
    [
        df["delay_days"] <= 0,
        df["delay_days"].between(1, 7),
        df["delay_days"] > 7
    ],
    [
        "On time",
        "1-7 days late",
        "Over 7 days late"
    ],
    default="Unknown"
)

# Validate review scores
df.loc[
    ~df["review_score_mean"].between(1, 5),
    "review_score_mean"
] = np.nan

# Check review availability before excluding missing reviews
print("\nREVIEW COVERAGE")
print("Eligible orders:", len(df))
print(
    "Orders with valid reviews:",
    df["review_score_mean"].notna().sum()
)
print(
    "Orders missing valid reviews:",
    df["review_score_mean"].isna().sum()
)

# Keep valid review scores for satisfaction analysis
reviewed = df.dropna(
    subset=["review_score_mean"]
).copy()

reviewed["low_rating"] = (
    reviewed["review_score_mean"] <= 2
).astype(int)

# Overall customer satisfaction
result = reviewed.groupby(
    "delay_category",
    as_index=False
).agg(
    reviewed_orders=("order_id", "count"),
    average_review=("review_score_mean", "mean"),
    median_review=("review_score_mean", "median"),
    low_ratings=("low_rating", "sum")
)

result["low_rating_pct"] = (
    result["low_ratings"]
    / result["reviewed_orders"] * 100
)

order = [
    "On time",
    "1-7 days late",
    "Over 7 days late"
]

result["delay_category"] = pd.Categorical(
    result["delay_category"],
    categories=order,
    ordered=True
)

result = result.sort_values("delay_category")

print("\nOVERALL CUSTOMER SATISFACTION")
print(result.round(2).to_string(index=False))

# Focus on SP sellers and RJ customers
route = reviewed[
    (reviewed["seller_state"] == "SP")
    & (reviewed["customer_state"] == "RJ")
    & (reviewed["single_seller_order"] == 1)
    & (reviewed["order_month"].isin([
        "2018-02", "2018-03", "2018-04"
    ]))
].copy()

route_result = route.groupby(
    "order_month",
    as_index=False
).agg(
    reviewed_orders=("order_id", "count"),
    average_review=("review_score_mean", "mean"),
    low_rating_pct=("low_rating", "mean"),
    late_rate=("is_late", "mean")
)

route_result["low_rating_pct"] *= 100
route_result["late_rate"] *= 100

print("\nSP TO RJ CUSTOMER SATISFACTION")
print(route_result.round(2).to_string(index=False))

# Save outputs
OUTPUT.mkdir(parents=True, exist_ok=True)

result.to_csv(
    OUTPUT / "customer_satisfaction.csv",
    index=False
)

route_result.to_csv(
    OUTPUT / "sp_rj_customer_satisfaction.csv",
    index=False
)

print("\nAnalysis completed and results saved.")
