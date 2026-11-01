"""Descriptive analyses. Association != causation. Do not infer carrier fault."""
from __future__ import annotations
import pandas as pd


def _late_agg(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    relevant = df[df["eligible_sla"].eq(1)].copy()
    grouped = relevant.groupby(cols, dropna=False, as_index=False).agg(
        delivered_orders=("order_id", "size"), late_orders=("is_late", "sum"),
        average_delay_days_all_delivered=("late_days", "mean"))
    grouped["late_rate_pct"] = (100 * grouped["late_orders"] / grouped["delivered_orders"]).round(2)
    return grouped.sort_values(["late_rate_pct", "delivered_orders"], ascending=[False, False])


def analyze(fact: pd.DataFrame, *, min_group_size: int = 30) -> dict[str, pd.DataFrame | dict]:
    eligible = fact[fact["eligible_sla"].eq(1)].copy()
    n = len(eligible)
    late_n = int(eligible["is_late"].sum())
    summary = {
        "eligible_delivered_orders": n,
        "late_orders": late_n,
        "on_time_orders": n - late_n,
        "late_rate_pct": round(late_n / n * 100, 2) if n else None,
        "average_delay_days_for_late_orders": round(float(eligible.loc[eligible["is_late"].eq(1), "late_days"].mean()), 2)
            if late_n else None,
        "orders_with_review_in_eligible_population": int(eligible["review_score_mean"].notna().sum()),
    }
    monthly = _late_agg(fact, ["order_month"]).sort_values("order_month")
    state = _late_agg(fact, ["customer_state"])
    state = state[state["delivered_orders"].ge(min_group_size)]
    # Multi-seller orders excluded; a single order cannot otherwise be assigned to one seller.
    sellers = _late_agg(fact[(fact["single_seller_order"].eq(1)) & fact["single_seller_id"].notna()],
                        ["single_seller_id", "seller_state"])
    sellers = sellers[sellers["delivered_orders"].ge(min_group_size)]
    reviewed = eligible[eligible["review_score_mean"].notna()].copy()
    reviewed["delivery_group"] = reviewed["is_late"].map({1: "Late", 0: "On time"})
    reviewed["low_review"] = reviewed["review_score_mean"].le(2).astype(int)
    if len(reviewed):
        reviews = reviewed.groupby("delivery_group", as_index=False).agg(
            orders_with_reviews=("order_id", "size"), average_review_score=("review_score_mean", "mean"),
            low_review_orders=("low_review", "sum"))
        reviews["average_review_score"] = reviews["average_review_score"].round(2)
        reviews["low_review_pct"] = (reviews["low_review_orders"] / reviews["orders_with_reviews"] * 100).round(2)
    else:
        reviews = pd.DataFrame(columns=["delivery_group", "orders_with_reviews", "average_review_score", "low_review_orders", "low_review_pct"])
    # Each stage is measured only where non-negative and timestamps are present.
    stage = eligible.copy()
    stage["delivery_group"] = stage["is_late"].map({1: "Late", 0: "On time"})
    def summarize_stage(g):
        return pd.Series({
            "orders": len(g),
            "median_approval_days": g["approval_days"].median(),
            "median_pre_handoff_days": g["pre_handoff_days"].median(),
            "median_in_transit_days": g["in_transit_days"].median(),
            "missing_or_invalid_handoff_stages": int(g["pre_handoff_days"].isna().sum()),
            "missing_or_invalid_transit_stages": int(g["in_transit_days"].isna().sum()),
        })
    stages = pd.DataFrame([{"delivery_group": label, **summarize_stage(g).to_dict()} for label, g in stage.groupby("delivery_group")])
    return {"summary": summary, "monthly": monthly, "customer_states": state,
            "single_sellers": sellers, "reviews": reviews, "stages": stages}
