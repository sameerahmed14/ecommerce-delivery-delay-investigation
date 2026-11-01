
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "outputs/real/fact_orders.csv")

# Convert date columns
date_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# Select SP sellers to RJ customers
df = df[
    (df["eligible_sla"] == 1)
    & (df["single_seller_order"] == 1)
    & (df["seller_state"] == "SP")
    & (df["customer_state"] == "RJ")
    & (df["order_month"].isin([
        "2018-02", "2018-03", "2018-04"
    ]))
].copy()

# Calculate promised and actual delivery durations
df["promised_days"] = (
    df["order_estimated_delivery_date"]
    - df["order_purchase_timestamp"]
).dt.total_seconds() / 86400

df["actual_days"] = (
    df["order_delivered_customer_date"]
    - df["order_purchase_timestamp"]
).dt.total_seconds() / 86400

# Calculate severe delivery delays
df["delay_days"] = (
    df["order_delivered_customer_date"].dt.normalize()
    - df["order_estimated_delivery_date"].dt.normalize()
).dt.days

df["severe_delay"] = (df["delay_days"] > 7).astype(int)

# Clean invalid stage durations
for col in ["pre_handoff_days", "in_transit_days"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df.loc[df[col] < 0, col] = float("nan")

# Compare performance across months
result = df.groupby("order_month").agg(
    orders=("order_id", "count"),
    late_orders=("is_late", "sum"),
    severe_delays=("severe_delay", "sum"),
    median_promised_days=("promised_days", "median"),
    median_actual_days=("actual_days", "median"),
    median_handoff_days=("pre_handoff_days", "median"),
    median_transit_days=("in_transit_days", "median"),
    p90_transit_days=(
        "in_transit_days",
        lambda x: x.quantile(0.90)
    ),
    valid_transit_records=("in_transit_days", "count")
).reset_index()

result["late_rate_pct"] = (
    result["late_orders"] / result["orders"] * 100
)

result["severe_rate_pct"] = (
    result["severe_delays"] / result["orders"] * 100
)

print("\nSP TO RJ DELIVERY DIAGNOSTICS\n")
print(result.round(2).to_string(index=False))

# Save results for documentation
output_path = ROOT / "outputs/real/sp_rj_diagnostics.csv"
result.round(2).to_csv(output_path, index=False)

print(f"\nResults saved to: {output_path}")
