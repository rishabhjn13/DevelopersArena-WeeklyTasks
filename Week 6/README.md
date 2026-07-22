# Customer Sales Analysis

Week 5 project — pandas grouping/aggregation, multi-condition filtering, string ops,
datetime handling, merging, and pivot tables, applied to a customer + sales dataset.

## Goal

Merge customer (churn) data with sales transaction data to find top customers,
monthly/regional sales patterns, and retention by contract type, then summarize
it all in a dashboard and a written report.

## Data

- `customer_churn.csv` — 500 customers: tenure, charges, contract type, churn flag
- `sales_data.csv` — 100 sales transactions: date, product, quantity, price, region

The two files use different ID formats (`C00001` vs `CUST001`), so the notebook
extracts the numeric part of each ID to join them.

## Setup

```bash
pip install -r requirements.txt
jupyter notebook customer_analysis.ipynb
```

## Structure

```
customer_analysis.ipynb   - main analysis, day-by-day (see below)
sales_data.csv
customer_data.csv         - alias of customer_churn.csv, kept for submission naming
customer_churn.csv
analysis_report.pdf       - written report with charts, tables, findings, recommendations
outputs/dashboard.png     - the 6-chart dashboard on its own
requirements.txt
```

## Notebook flow

1. Load & explore both files
2. Clean IDs, parse dates, normalize text columns
3. Customer analysis — top customers, spend, regional split
4. Sales patterns — monthly totals, best sellers, filtered subsets
5. Pivot tables — region x product, month x region, churn/retention by contract
6. Dashboard — 6 charts (line, bar, pie, horizontal bar, bar, heatmap)
7. Summary stats for the report

## Headline numbers

Total Revenue: $12,365,048 (see report for full figures — pulled straight from
the notebook, not hardcoded)

## Notes

- Only 100 of the 500 customers have matching sales records in this sample,
  so "total customers" and "customers with purchase activity" are reported
  separately rather than conflated.
- Retention rate is derived from the `Churn` column already present in the
  customer file, not calculated from repeat-purchase behavior (there isn't
  enough transaction history per customer for that here).
