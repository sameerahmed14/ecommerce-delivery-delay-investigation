from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "outputs" / "real" / "fact_orders.csv"

print("Loading delivery data...")

df = pd.read_csv(DATA)

for col in ["eligible_sla", "single_seller_order", "is_late"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

for col in [
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]:
    df[col] = pd.to_datetime(df[col], errors="coerce")

df["severe_delay"] = (
    (
        df["order_delivered_customer_date"].dt.normalize()
        - df["order_estimated_delivery_date"].dt.normalize()
    ).dt.days > 7
).astype(int)

df = df[
    (df["eligible_sla"] == 1)
    & (df["single_seller_order"] == 1)
    & (df["customer_state"] == "RJ")
    & (df["order_month"].isin(["2018-02", "2018-03", "2018-04"]))
    & (df["seller_state"].notna())
].copy()

df["in_transit_days"] = pd.to_numeric(
    df["in_transit_days"], errors="coerce"
)
df.loc[df["in_transit_days"] < 0, "in_transit_days"] = float("nan")

result = df.groupby(
    ["seller_state", "order_month"],
    as_index=False
).agg(
    orders=("order_id", "count"),
    late_orders=("is_late", "sum"),
    severe_delays=("severe_delay", "sum"),
    median_transit_days=("in_transit_days", "median")
)

result["late_rate_pct"] = (
    result["late_orders"] / result["orders"] * 100
).round(2)

result["severe_rate_pct"] = (
    result["severe_delays"] / result["orders"] * 100
).round(2)

march = result[
    (result["order_month"] == "2018-03")
    & (result["orders"] >= 30)
]

top_states = march.nlargest(6, "late_orders")["seller_state"]

final = result[
    result["seller_state"].isin(top_states)
].sort_values(["seller_state", "order_month"])

print("\nSELLER-TO-RIO DE JANEIRO ROUTE ANALYSIS\n")
print(final.round(2).to_string(index=False))
