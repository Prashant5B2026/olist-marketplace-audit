"""Load the 9 Olist Kaggle CSVs into a SQLite database.

Idempotent: rerunning replaces all tables.
"""
from pathlib import Path
import pandas as pd
from sqlalchemy import text

from src.db import get_engine, PROJECT_ROOT

RAW_DIR = PROJECT_ROOT / "data" / "raw"

TABLE_MAP = {
    "olist_customers_dataset.csv":           "customers",
    "olist_geolocation_dataset.csv":         "geolocation",
    "olist_order_items_dataset.csv":         "order_items",
    "olist_order_payments_dataset.csv":      "order_payments",
    "olist_order_reviews_dataset.csv":       "order_reviews",
    "olist_orders_dataset.csv":              "orders",
    "olist_products_dataset.csv":            "products",
    "olist_sellers_dataset.csv":             "sellers",
    "product_category_name_translation.csv": "product_category_name_translation",
}

DATE_COLUMNS = {
    "orders": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "order_items": ["shipping_limit_date"],
    "order_reviews": ["review_creation_date", "review_answer_timestamp"],
}


def load_table(csv_path: Path, table_name: str, engine) -> int:
    parse_dates = DATE_COLUMNS.get(table_name, [])
    df = pd.read_csv(csv_path, parse_dates=parse_dates)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    return len(df)


def main() -> None:
    engine = get_engine()
    print(f"Writing to {engine.url}")
    for csv_name, table_name in TABLE_MAP.items():
        csv_path = RAW_DIR / csv_name
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing raw CSV: {csv_path}")
        rows = load_table(csv_path, table_name, engine)
        print(f"  {table_name:<32} {rows:>10,} rows")

    with engine.connect() as conn:
        tables = conn.execute(text(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )).all()
    print(f"\n{len(tables)} tables in olist.db: {[t[0] for t in tables]}")


if __name__ == "__main__":
    main()
