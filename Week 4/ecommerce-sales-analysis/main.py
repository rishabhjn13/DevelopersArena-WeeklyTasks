"""
This script implements a full pipeline:
    1. Load raw sales data (with validation)
    2. Clean the data (missing values, invalid entries, duplicates, mismatches)
    3. Analyze sales patterns
    4. Visualize results with 3 chart types (bar, pie, line)
    5. Generate a written insights report
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
RAW_DATA_PATH = os.path.join("data", "sales_raw.csv")
CLEAN_DATA_PATH = os.path.join("data", "sales_clean.csv")
VIS_DIR = "visualizations"
REPORT_DIR = "report"
REPORT_PATH = os.path.join(REPORT_DIR, "analysis_report.md")

VALID_REGIONS = {"East", "West", "North", "South"}

REQUIRED_COLS = {"Date", "Product", "Quantity", "Price", "Customer_ID", "Region", "Total_Sales"}


# ----------------------------------------------------------------------
# Step 1: Load data (with error handling)
# ----------------------------------------------------------------------
def load_data(path: str) -> pd.DataFrame:
    """Load the raw CSV, raising a clear error if it's missing, empty, or malformed."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Could not find data file at '{path}'. "
            f"Run 'python data/generate_data.py' first, or add your own "
            f"sales_raw.csv with columns: {sorted(REQUIRED_COLS)}."
        )
    try:
        df = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        raise ValueError(f"The data file at '{path}' is empty.")

    missing_cols = REQUIRED_COLS - set(df.columns)
    if missing_cols:
        raise ValueError(f"Data file is missing required columns: {missing_cols}")

    if df.empty:
        raise ValueError("Data file contains no rows.")

    return df


# ----------------------------------------------------------------------
# Step 2: Clean data
# ----------------------------------------------------------------------
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw sales data:
      - drop rows with missing Product/Region
      - standardize region casing
      - drop invalid regions
      - convert Quantity, Price, Total_Sales to numeric
      - drop non-positive Quantity/Price
      - recompute Total_Sales and flag/fix rows where it doesn't match Quantity * Price
      - parse dates, drop unparseable rows
      - drop exact duplicate rows
    Returns a clean copy; never mutates the input in place.
    """
    df = df.copy()
    initial_count = len(df)
    issues = []

    # Standardize region text
    df["Region"] = df["Region"].astype(str).str.strip().str.title()
    df.loc[df["Region"].isin(["", "Nan", "None"]), "Region"] = pd.NA

    # Standardize product text and flag blanks
    df["Product"] = df["Product"].astype(str).str.strip()
    df.loc[df["Product"].isin(["", "Nan", "None"]), "Product"] = pd.NA

    # Drop rows missing Product or Region
    before = len(df)
    df = df.dropna(subset=["Product", "Region"])
    if before - len(df) > 0:
        issues.append(f"Dropped {before - len(df)} rows with missing Product/Region")

    # Coerce numeric columns
    for col in ["Quantity", "Price", "Total_Sales"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    before = len(df)
    df = df.dropna(subset=["Quantity", "Price", "Total_Sales"])
    if before - len(df) > 0:
        issues.append(f"Dropped {before - len(df)} rows with non-numeric Quantity/Price/Total_Sales")

    # Drop non-positive Quantity or Price (invalid transactions)
    before = len(df)
    df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]
    if before - len(df) > 0:
        issues.append(f"Dropped {before - len(df)} rows with zero/negative Quantity or Price")

    # Keep only known regions
    before = len(df)
    df = df[df["Region"].isin(VALID_REGIONS)]
    if before - len(df) > 0:
        issues.append(f"Dropped {before - len(df)} rows with unrecognized Region")

    # Recompute Total_Sales where it doesn't match Quantity * Price (data entry error)
    expected_total = df["Quantity"] * df["Price"]
    mismatch = (df["Total_Sales"] - expected_total).abs() > 1  # allow tiny float rounding
    mismatch_count = mismatch.sum()
    if mismatch_count > 0:
        df.loc[mismatch, "Total_Sales"] = expected_total[mismatch]
        issues.append(f"Recalculated Total_Sales for {mismatch_count} rows where it didn't match Quantity x Price")

    # Parse dates
    before = len(df)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    if before - len(df) > 0:
        issues.append(f"Dropped {before - len(df)} rows with unparseable Date")

    # Drop exact duplicates
    before = len(df)
    df = df.drop_duplicates()
    if before - len(df) > 0:
        issues.append(f"Dropped {before - len(df)} exact duplicate rows")

    df = df.sort_values("Date").reset_index(drop=True)
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    print(f"Cleaning summary: {initial_count} raw rows -> {len(df)} clean rows")
    for issue in issues:
        print(f"  - {issue}")

    if df.empty:
        raise ValueError("No valid rows remained after cleaning. Check the raw data file.")

    return df


# ----------------------------------------------------------------------
# Step 3: Analyze
# ----------------------------------------------------------------------
def analyze_data(df: pd.DataFrame) -> dict:
    """Compute summary metrics used for both the charts and the report."""
    total_revenue = df["Total_Sales"].sum()
    total_units = df["Quantity"].sum()
    num_orders = len(df)
    avg_order_value = df["Total_Sales"].mean()

    by_product = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
    by_region = df.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False)
    by_month = df.groupby("Month")["Total_Sales"].sum().sort_index()
    units_by_product = df.groupby("Product")["Quantity"].sum().sort_values(ascending=False)

    top_product = by_product.index[0]
    top_product_amount = by_product.iloc[0]
    top_product_pct = (top_product_amount / total_revenue) * 100

    top_region = by_region.index[0]
    top_region_amount = by_region.iloc[0]
    top_region_pct = (top_region_amount / total_revenue) * 100

    best_selling_product_by_units = units_by_product.index[0]

    num_customers = df["Customer_ID"].nunique()
    revenue_per_customer = total_revenue / num_customers

    mom_change_pct = None
    if len(by_month) >= 2:
        prev, latest = by_month.iloc[-2], by_month.iloc[-1]
        mom_change_pct = ((latest - prev) / prev) * 100

    return {
        "total_revenue": total_revenue,
        "total_units": total_units,
        "num_orders": num_orders,
        "avg_order_value": avg_order_value,
        "by_product": by_product,
        "by_region": by_region,
        "by_month": by_month,
        "top_product": top_product,
        "top_product_amount": top_product_amount,
        "top_product_pct": top_product_pct,
        "top_region": top_region,
        "top_region_amount": top_region_amount,
        "top_region_pct": top_region_pct,
        "best_selling_product_by_units": best_selling_product_by_units,
        "num_customers": num_customers,
        "revenue_per_customer": revenue_per_customer,
        "mom_change_pct": mom_change_pct,
    }


# ----------------------------------------------------------------------
# Step 4: Visualize
# ----------------------------------------------------------------------
def create_bar_chart(stats: dict, out_dir: str) -> str:
    """Bar chart: total revenue by product."""
    by_product = stats["by_product"]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.bar(by_product.index, by_product.values, color="#4C72B0")

    ax.set_title("Total Revenue by Product", fontsize=14, fontweight="bold")
    ax.set_xlabel("Product")
    ax.set_ylabel("Revenue (INR)")
    plt.xticks(rotation=35, ha="right")

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:,.0f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha="center", fontsize=8)

    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()

    path = os.path.join(out_dir, "revenue_by_product_bar.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def create_pie_chart(stats: dict, out_dir: str) -> str:
    """Pie chart: revenue distribution across regions."""
    by_region = stats["by_region"]

    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    colors = plt.cm.Set3.colors
    ax.pie(
        by_region.values,
        labels=by_region.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        pctdistance=0.8,
    )
    ax.set_title("Revenue Distribution by Region", fontsize=14, fontweight="bold")
    ax.axis("equal")
    fig.tight_layout()

    path = os.path.join(out_dir, "revenue_by_region_pie.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def create_line_chart(stats: dict, out_dir: str) -> str:
    """Line chart: monthly revenue trend."""
    by_month = stats["by_month"]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(by_month.index, by_month.values, marker="o", linewidth=2, color="#DD8452")

    for x, y in zip(by_month.index, by_month.values):
        ax.annotate(f"{y:,.0f}", xy=(x, y), xytext=(0, 8),
                    textcoords="offset points", ha="center", fontsize=8)

    ax.set_title("Monthly Revenue Trend", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Revenue (INR)")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()

    path = os.path.join(out_dir, "monthly_revenue_trend_line.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


# ----------------------------------------------------------------------
# Step 5: Report
# ----------------------------------------------------------------------
def write_report(stats: dict, chart_paths: dict, report_path: str) -> None:
    by_product = stats["by_product"]
    by_region = stats["by_region"]
    by_month = stats["by_month"]

    mom_line = (
        f"Revenue changed by **{stats['mom_change_pct']:+.1f}%** from the previous month to the latest month."
        if stats["mom_change_pct"] is not None
        else "Not enough months of data to compute a month-over-month change."
    )

    lines = [
        "# E-commerce Sales Analysis Report",
        "",
        "## Overview",
        "This report summarizes e-commerce sales performance based on transaction-level "
        "order data, covering data loading, cleaning, analysis, and visualization.",
        "",
        "## Key Metrics",
        f"- **Total revenue analyzed:** ₹{stats['total_revenue']:,.0f}",
        f"- **Total units sold:** {stats['total_units']:,.0f}",
        f"- **Number of orders:** {stats['num_orders']}",
        f"- **Average order value:** ₹{stats['avg_order_value']:,.0f}",
        f"- **Unique customers:** {stats['num_customers']}",
        f"- **Revenue per customer:** ₹{stats['revenue_per_customer']:,.0f}",
        f"- **Top product by revenue:** {stats['top_product']} "
        f"(₹{stats['top_product_amount']:,.0f}, {stats['top_product_pct']:.1f}% of total)",
        f"- **Top region by revenue:** {stats['top_region']} "
        f"(₹{stats['top_region_amount']:,.0f}, {stats['top_region_pct']:.1f}% of total)",
        f"- **Best-selling product by units:** {stats['best_selling_product_by_units']}",
        "",
        "## Revenue by Product",
        "",
        "| Product | Revenue (INR) | % of Total |",
        "|---|---|---|",
    ]

    for prod, amt in by_product.items():
        pct = (amt / stats["total_revenue"]) * 100
        lines.append(f"| {prod} | {amt:,.0f} | {pct:.1f}% |")

    lines += [
        "",
        "## Revenue by Region",
        "",
        "| Region | Revenue (INR) | % of Total |",
        "|---|---|---|",
    ]
    for region, amt in by_region.items():
        pct = (amt / stats["total_revenue"]) * 100
        lines.append(f"| {region} | {amt:,.0f} | {pct:.1f}% |")

    lines += [
        "",
        "## Monthly Trend",
        "",
        "| Month | Total Revenue (INR) |",
        "|---|---|",
    ]
    for month, amt in by_month.items():
        lines.append(f"| {month} | {amt:,.0f} |")

    lines += [
        "",
        "## Visualizations",
        "",
        f"![Revenue by Product]({os.path.relpath(chart_paths['bar'], REPORT_DIR)})",
        "",
        f"![Revenue by Region]({os.path.relpath(chart_paths['pie'], REPORT_DIR)})",
        "",
        f"![Monthly Revenue Trend]({os.path.relpath(chart_paths['line'], REPORT_DIR)})",
        "",
        "## Insights",
        "",
        f"1. **{stats['top_product']} drives the most revenue**, contributing "
        f"{stats['top_product_pct']:.1f}% of total sales. Combined with it being "
        f"{'also' if stats['top_product'] == stats['best_selling_product_by_units'] else 'not'} "
        f"the best-selling product by units ({stats['best_selling_product_by_units']} sells the most units), "
        f"this shows whether revenue leadership comes from price or from volume.",
        f"2. **{stats['top_region']} is the strongest region**, generating "
        f"{stats['top_region_pct']:.1f}% of total revenue. Regions significantly below this "
        f"level may be under-served or under-marketed.",
        f"3. {mom_line}",
        f"4. Average order value is ₹{stats['avg_order_value']:,.0f} across "
        f"{stats['num_orders']} orders from {stats['num_customers']} unique customers "
        f"(₹{stats['revenue_per_customer']:,.0f} revenue per customer on average).",
        "",
        "## Data Quality Notes",
        "The raw dataset contained missing values (Product/Region), invalid or negative "
        "Quantity/Price, unrecognized region names, inconsistent casing, rows where "
        "`Total_Sales` didn't match `Quantity * Price`, and duplicate rows. All of these "
        "were detected and handled during the cleaning step (missing/invalid rows dropped, "
        "mismatched totals recalculated) — see console output / `data/sales_clean.csv` for "
        "the cleaned dataset, and `main.py::clean_data()` for the exact rules applied.",
    ]

    os.makedirs(REPORT_DIR, exist_ok=True)
    with open(report_path, "w") as f:
        f.write("\n".join(lines))


# ----------------------------------------------------------------------
# Main pipeline
# ----------------------------------------------------------------------
def main():
    print("=" * 60)
    print("E-COMMERCE SALES ANALYSIS — ANALYSIS PIPELINE")
    print("=" * 60)

    try:
        print("\n[1/5] Loading raw data...")
        raw_df = load_data(RAW_DATA_PATH)
        print(f"  Loaded {len(raw_df)} raw rows from {RAW_DATA_PATH}")

        print("\n[2/5] Cleaning data...")
        clean_df = clean_data(raw_df)
        clean_df.to_csv(CLEAN_DATA_PATH, index=False)
        print(f"  Saved cleaned data to {CLEAN_DATA_PATH}")

        print("\n[3/5] Analyzing sales patterns...")
        stats = analyze_data(clean_df)
        print(f"  Total revenue: Rs.{stats['total_revenue']:,.0f} across {stats['num_orders']} orders")
        print(f"  Top product: {stats['top_product']} ({stats['top_product_pct']:.1f}%)")
        print(f"  Top region: {stats['top_region']} ({stats['top_region_pct']:.1f}%)")

        print("\n[4/5] Creating visualizations...")
        os.makedirs(VIS_DIR, exist_ok=True)
        chart_paths = {
            "bar": create_bar_chart(stats, VIS_DIR),
            "pie": create_pie_chart(stats, VIS_DIR),
            "line": create_line_chart(stats, VIS_DIR),
        }
        for name, path in chart_paths.items():
            print(f"  Saved {name} chart -> {path}")

        print("\n[5/5] Writing report...")
        write_report(stats, chart_paths, REPORT_PATH)
        print(f"  Saved report -> {REPORT_PATH}")

        print("\n" + "=" * 60)
        print("DONE. Pipeline completed successfully.")
        print("=" * 60)

    except (FileNotFoundError, ValueError) as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[UNEXPECTED ERROR] {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
