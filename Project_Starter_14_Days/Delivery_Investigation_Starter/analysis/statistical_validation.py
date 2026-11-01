
from pathlib import Path
import pandas as pd
from scipy.stats import chi2_contingency

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "outputs/real/fact_orders.csv")

# Prepare the data
for column in [
    "eligible_sla", "is_late", "review_score_mean"
]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

for column in [
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]:
    df[column] = pd.to_datetime(df[column], errors="coerce")

df = df[df["eligible_sla"] == 1].copy()

df["delay_days"] = (
    df["order_delivered_customer_date"].dt.normalize()
    - df["order_estimated_delivery_date"].dt.normalize()
).dt.days

# Check missing reviews by delivery status
print("\nREVIEW COVERAGE BY DELIVERY STATUS")
coverage = df.groupby("is_late").agg(
    orders=("order_id", "count"),
    valid_reviews=("review_score_mean", "count")
)
coverage["coverage_pct"] = (
    coverage["valid_reviews"] / coverage["orders"] * 100
)
print(coverage.round(2))

# Keep valid reviews
df = df[df["review_score_mean"].between(1, 5)].copy()

df["delay_group"] = pd.cut(
    df["delay_days"],
    bins=[float("-inf"), 0, 7, float("inf")],
    labels=["On time", "1-7 days late", "Over 7 days late"]
)

df["low_rating"] = (df["review_score_mean"] <= 2).astype(int)

# Compare customer ratings
summary = df.groupby(
    "delay_group", observed=True
).agg(
    orders=("order_id", "count"),
    average_rating=("review_score_mean", "mean"),
    low_rating_pct=("low_rating", "mean")
)

summary["low_rating_pct"] *= 100

print("\nCUSTOMER RATING COMPARISON")
print(summary.round(2))

# Chi-square test: delivery severity vs low ratings
table = pd.crosstab(df["delay_group"], df["low_rating"])

chi2, p_value, dof, expected = chi2_contingency(table)

print("\nSTATISTICAL TEST RESULTS")
print("Chi-square statistic:", round(chi2, 2))
print("Degrees of freedom:", dof)
print("P-value:", f"{p_value:.4g}")

if p_value < 0.05:
    print("Statistically significant association detected.")
else:
    print("Insufficient evidence of an association.")

print("\nNote: Statistical significance does not prove causation.")
