"""
Clean the messy sales orders file.

What it does, in plain steps:
  1. Read data/sales_orders_messy.csv
  2. Trim extra spaces and fix the case of names (title case)
  3. Parse dates written in different formats into YYYY-MM-DD
  4. Strip currency symbols ($, Rs.) and commas from money, keep plain numbers
  5. Drop rows we cannot fix honestly (bad date, missing quantity or price)
  6. Fill missing customer / city with "Unknown" (no sales numbers are invented)
  7. If total_amount is missing, calculate it as quantity * unit_price
  8. Remove exact duplicate rows
  9. Save data/sales_orders_cleaned.csv and print before / after counts

Run it with:  python3 clean_sales_data.py
Needs: pandas, numpy
"""

import re
import pandas as pd
import numpy as np
from datetime import datetime

INPUT_FILE = "data/sales_orders_messy.csv"
OUTPUT_FILE = "data/sales_orders_cleaned.csv"

# Dates in the messy file look like: 2026-01-05, 05/01/2026, Jan 5 2026
DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%b %d %Y", "%B %d %Y"]


def parse_date(text):
    """Try each known date format. Return None if none of them fit."""
    text = str(text).strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def clean_money(text):
    """Turn '$1,200.50', 'Rs. 1,200' or ' 1200 ' into a plain number."""
    text = str(text).strip()
    text = text.replace("$", "").replace("Rs.", "").replace("Rs", "")
    text = text.replace(",", "").strip()
    if text == "":
        return np.nan
    try:
        return float(text)
    except ValueError:
        return np.nan


def clean_text(text):
    """Trim spaces, collapse double spaces, and use title case."""
    text = str(text).strip()
    text = re.sub(r"\s+", " ", text)
    return text.title()


def main():
    # 1. Read everything as text, so messy values are not lost on load.
    df = pd.read_csv(INPUT_FILE, dtype=str, keep_default_na=False)
    rows_before = len(df)
    print(f"Rows before cleaning: {rows_before}")

    # Count blank cells in the raw file.
    blank_cells = int((df == "").sum().sum())
    print(f"Blank cells in messy file: {blank_cells}")

    # 2. Trim spaces and fix case for the text columns.
    for col in ["customer_name", "product", "city"]:
        df[col] = df[col].apply(clean_text)

    # Missing customer / city: fill with "Unknown" (no sales data invented).
    missing_customer = int((df["customer_name"] == "").sum())
    missing_city = int((df["city"] == "").sum())
    df.loc[df["customer_name"] == "", "customer_name"] = "Unknown"
    df.loc[df["city"] == "", "city"] = "Unknown"
    print(f"Missing customer names filled with 'Unknown': {missing_customer}")
    print(f"Missing cities filled with 'Unknown': {missing_city}")

    # 3. Parse the dates. Rows with a date we cannot read are dropped.
    df["order_date"] = df["order_date"].apply(parse_date)
    invalid_dates = int(df["order_date"].isna().sum())
    df = df.dropna(subset=["order_date"])
    df["order_date"] = pd.to_datetime(df["order_date"]).dt.strftime("%Y-%m-%d")
    print(f"Rows dropped for invalid dates: {invalid_dates}")

    # 4. Clean the money columns.
    df["unit_price"] = df["unit_price"].apply(clean_money)
    df["total_amount"] = df["total_amount"].apply(clean_money)

    # Quantity must be a whole number.
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    # 5. Drop rows with no quantity or no unit price.
    #    We do not invent sales, so we cannot guess these numbers.
    bad_qty_price = int(df["quantity"].isna().sum() + df["unit_price"].isna().sum()
                        - int(((df["quantity"].isna()) & (df["unit_price"].isna())).sum()))
    df = df.dropna(subset=["quantity", "unit_price"])
    df["quantity"] = df["quantity"].astype(int)
    print(f"Rows dropped for missing quantity or unit price: {bad_qty_price}")

    # 6. If total_amount is missing, calculate it from quantity * unit_price.
    missing_total = int(df["total_amount"].isna().sum())
    df["total_amount"] = df["total_amount"].fillna(df["quantity"] * df["unit_price"])
    print(f"Missing total_amount values calculated (quantity x unit_price): {missing_total}")

    # Round money to 2 decimal places.
    df["unit_price"] = df["unit_price"].round(2)
    df["total_amount"] = df["total_amount"].round(2)

    # 7. Remove exact duplicate rows.
    rows_before_dedup = len(df)
    df = df.drop_duplicates()
    duplicates_removed = rows_before_dedup - len(df)
    print(f"Exact duplicate rows removed: {duplicates_removed}")

    # 8. Sort by date, then order id, and save.
    df = df.sort_values(["order_date", "order_id"]).reset_index(drop=True)
    df.to_csv(OUTPUT_FILE, index=False)

    rows_after = len(df)
    print(f"Rows after cleaning: {rows_after}")
    print(f"Rows removed in total: {rows_before - rows_after}")
    print(f"Saved cleaned file to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
