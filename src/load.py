"""Data loading and analysis-dataframe build.

Encapsulates the data preparation steps every analysis notebook needs:
load all source tables from SQLite, apply the Day 1 data quality findings,
and construct the denormalised order-item dataframe used by hypothesis
tests and the trust-score work downstream.
"""
from typing import Dict, Optional
import pandas as pd

from src.db import get_engine

# SQLite stores datetimes as TEXT, so columns must be re-parsed on read.
DATE_COLS = {
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

# Operating window from Day 1 findings (notebooks/01_data_quality.ipynb).
WINDOW_START = pd.Timestamp("2016-09-04")
WINDOW_END = pd.Timestamp("2018-10-17")


def load_tables() -> Dict[str, pd.DataFrame]:
    """Load all 9 source tables with Day 1 DQ findings applied.

    Returns a dict of DataFrames keyed by table name:
    customers, geolocation, order_items, order_payments, order_reviews,
    orders (filtered to operating window), products (null categories
    tagged as "unknown"), sellers, product_category_name_translation.

    Plus a derived 'geo' table with one row per zip prefix
    (median lat/lng and modal state).
    """
    engine = get_engine()

    def _load(table: str) -> pd.DataFrame:
        return pd.read_sql(f"SELECT * FROM {table}", engine, parse_dates=DATE_COLS.get(table))

    tables = {
        "customers":                         _load("customers"),
        "geolocation":                       _load("geolocation"),
        "order_items":                       _load("order_items"),
        "order_payments":                    _load("order_payments"),
        "order_reviews":                     _load("order_reviews"),
        "orders":                            _load("orders"),
        "products":                          _load("products"),
        "sellers":                           _load("sellers"),
        "product_category_name_translation": _load("product_category_name_translation"),
    }

    # Filter orders to the operating window.
    orders = tables["orders"]
    tables["orders"] = orders[
        (orders["order_purchase_timestamp"] >= WINDOW_START)
        & (orders["order_purchase_timestamp"] <= WINDOW_END)
    ].copy()

    # Tag null product categories as "unknown".
    tables["products"]["product_category_name"] = (
        tables["products"]["product_category_name"].fillna("unknown")
    )

    # Collapse geolocation to one row per zip prefix.
    geo_raw = tables["geolocation"]
    tables["geo"] = (geo_raw
                     .groupby("geolocation_zip_code_prefix", as_index=False)
                     .agg(lat=("geolocation_lat", "median"),
                          lng=("geolocation_lng", "median"),
                          state=("geolocation_state", lambda s: s.mode().iloc[0])))

    return tables


def load_analysis_df(tables: Optional[Dict[str, pd.DataFrame]] = None) -> pd.DataFrame:
    """Build the denormalised order-item dataframe used by hypothesis tests.

    One row per (order, item) pair. Includes columns from orders, customers,
    sellers, products, reviews, and the English category translation, plus
    three derived columns:

    - promise_gap_days: estimated minus actual delivery date, in days.
      Positive values mean the order arrived early. Null when undelivered.
    - actual_delivery_days: actual delivery date minus purchase date, in days.
      Null when undelivered.
    - category_en: English category name, falling back to the Portuguese name
      for products whose category has no translation entry.

    Pass an existing dict from load_tables() to avoid re-loading from SQLite.
    """
    if tables is None:
        tables = load_tables()

    # One review per order. Day 1 found review_id is not unique across orders;
    # take the earliest review per order to be deterministic.
    review_by_order = (tables["order_reviews"]
                       .sort_values("review_creation_date")
                       .drop_duplicates("order_id", keep="first")
                       [["order_id", "review_score", "review_creation_date"]])

    base = (tables["orders"]
            .merge(tables["customers"], on="customer_id", how="left")
            .merge(review_by_order, on="order_id", how="left"))

    df = (tables["order_items"]
          .merge(base, on="order_id", how="inner")
          .merge(tables["sellers"], on="seller_id", how="left")
          .merge(tables["products"][["product_id", "product_category_name"]],
                 on="product_id", how="left")
          .merge(tables["product_category_name_translation"],
                 on="product_category_name", how="left"))

    df["promise_gap_days"] = (
        df["order_estimated_delivery_date"] - df["order_delivered_customer_date"]
    ).dt.days

    df["actual_delivery_days"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.days

    df["category_en"] = (
        df["product_category_name_english"].fillna(df["product_category_name"])
    )

    return df
