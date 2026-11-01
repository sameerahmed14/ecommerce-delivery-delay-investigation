"""Command-line entrypoint: python -m delivery_investigation.cli run ..."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sqlite3
from .pipeline import load_csvs, build_fact_orders
from .analysis import analyze


def run(raw_dir: Path, output_dir: Path, min_group_size: int = 30) -> None:
    frames = load_csvs(raw_dir)
    fact, audit = build_fact_orders(frames)
    result = analyze(fact, min_group_size=min_group_size)
    output_dir.mkdir(parents=True, exist_ok=True)
    fact.to_csv(output_dir / "fact_orders.csv", index=False)
    with sqlite3.connect(output_dir / "delivery_analytics.sqlite") as conn:
        fact.to_sql("fact_orders", conn, if_exists="replace", index=False)
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_fact_orders_order_id ON fact_orders(order_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_fact_orders_customer_state ON fact_orders(customer_state)")
    for name, df in result.items():
        if name != "summary":
            df.to_csv(output_dir / f"{name}.csv", index=False)
    (output_dir / "kpis.json").write_text(json.dumps(result["summary"], indent=2), encoding="utf-8")
    (output_dir / "data_quality.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print("Project pipeline completed")
    print("Source:", raw_dir)
    print("Outputs:", output_dir)
    print("KPIs:", json.dumps(result["summary"], indent=2))
    print("Quality audit:", json.dumps(audit, indent=2))
    print("Note: demo data is SYNTHETIC; never present demo KPIs as Olist findings.") if "sample" in str(raw_dir).lower() else None


def main():
    p = argparse.ArgumentParser(description="Olist delivery performance investigation")
    p.add_argument("command", choices=["run"])
    p.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    p.add_argument("--output-dir", type=Path, default=Path("outputs/real"))
    p.add_argument("--min-group-size", type=int, default=30)
    args = p.parse_args()
    run(args.raw_dir, args.output_dir, args.min_group_size)


if __name__ == "__main__":
    main()
