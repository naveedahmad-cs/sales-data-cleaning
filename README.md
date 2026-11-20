# Sales Orders — Data Cleaning Project

A small, honest data-cleaning project in Python. It takes a messy sales-orders
file and turns it into a clean file that is ready to analyse.

## What the messy data contains

`data/sales_orders_messy.csv` (500 rows) has real messiness on purpose:

- Exact duplicate rows
- Missing values
- Dates in different formats: `2026-01-05`, `05/01/2026`, `Jan 5 2026`
- Money in different formats: `$1,200.50`, `1200`, `Rs. 1,200`
- Extra spaces and inconsistent case in names

## What the script does

`clean_sales_data.py`:

1. Trims spaces and fixes name case (title case)
2. Parses all dates into `YYYY-MM-DD`
3. Strips `$`, `Rs.` and commas from money and keeps plain numbers
4. Drops rows with an unreadable date, or with no quantity / unit price
   (no sales numbers are invented)
5. Fills missing customer / city with `Unknown`
6. Calculates a missing `total_amount` only as `quantity x unit_price`
7. Removes exact duplicate rows
8. Saves `data/sales_orders_cleaned.csv`

## Tools

- Python
- Pandas
- NumPy

## How to run it

```bash
python3 clean_sales_data.py
```

It prints the before / after counts. See `SUMMARY.md` for the counted results.

## Files

- `clean_sales_data.py` — the cleaning script
- `data/sales_orders_messy.csv` — messy input (500 rows)
- `data/sales_orders_cleaned.csv` — cleaned output (432 rows)
- `SUMMARY.md` — before / after summary with real counted numbers

## Honest note

This is a **sample dataset created for learning**. It is not real client data,
and no real client, company, or sales result is claimed anywhere in this project.

## Author

Naveed Ahmad — Computer Science student, Government College University Faisalabad,
focused on data engineering.
LinkedIn: https://www.linkedin.com/in/naveedahmad-cs/
GitHub: https://github.com/naveedahmad-cs
