# Before / After Summary

All numbers below are the **real counted results** from running
`python3 clean_sales_data.py` on this project. Nothing here is guessed.

## Row counts

| Measure | Count |
|---|---|
| Rows before cleaning | 500 |
| Rows after cleaning | 432 |
| Rows removed in total | 68 |

## What was fixed / removed

| Measure | Count |
|---|---|
| Blank cells in the messy file | 80 |
| Exact duplicate rows removed | 27 |
| Rows dropped for invalid dates | 15 |
| Rows dropped for missing quantity or unit price | 26 |
| Missing customer names filled with `Unknown` | 23 |
| Missing cities filled with `Unknown` | 7 |
| Missing `total_amount` values calculated as quantity x unit_price | 20 |

Check: 15 (bad dates) + 26 (missing quantity/price) + 27 (duplicates) = 68 rows removed.

## Cleaned file — verified

- Rows in `data/sales_orders_cleaned.csv`: 432
- Duplicate rows left: 0
- Blank / missing cells left: 0
- Dates: all in `YYYY-MM-DD` format, from 2026-01-01 to 2026-03-31
- Total quantity: 1,279
- Total of `total_amount`: 794,568.73

## Rules used (no sales invented)

- A row with an unreadable date was dropped, not guessed.
- A row with no quantity or no unit price was dropped, not guessed.
- A missing `total_amount` was only calculated from that row's own
  quantity and unit price.
- Missing customer / city names were filled with `Unknown`, which adds
  no sales numbers.
