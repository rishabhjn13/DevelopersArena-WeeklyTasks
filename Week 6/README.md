# Interactive Sales Dashboard

Week 6 project — Seaborn statistical charts + Plotly interactivity, built on the
same `sales_data.csv` used in Week 5 (100 transactions: date, product, quantity,
price, customer, region).

## Project Overview

Goal: go beyond static charts and build a dashboard that supports both statistical
exploration (distribution, correlation) and interactive exploration (hover detail,
filtering) of sales trends, product performance, and regional/customer patterns.

## Setup Instructions

```bash
pip install -r requirements.txt
jupyter notebook dashboard.ipynb
```

To regenerate everything (all PNGs + interactive HTML files + the GIF) from the
command line instead of the notebook:

```bash
python dashboard.py
```

Both `dashboard.ipynb` and `dashboard.py` contain the same logic — the notebook
is the day-by-day walkthrough version, `dashboard.py` is the plain script version
for the GitHub structure requirement.

## Code Structure

```
dashboard.ipynb                          - day-by-day notebook (documented below)
dashboard.py                             - standalone script, same logic
sales_data.csv                           - source data
requirements.txt
dashboard_demo.gif                       - animated preview cycling through the charts
visualizations/
  01_region_bar.png                      - total sales by region (bar)
  02_price_boxplot.png                   - price distribution by product (box)
  03_region_violin.png                   - order value distribution by region (violin)
  04_correlation_heatmap.png             - Quantity/Price/Total_Sales correlation
  05_region_product_heatmap.png          - revenue by region x product (heatmap)
  06_dashboard_2x2.png                   - static 2x2 combined dashboard
  07_interactive_dashboard_preview.png   - static preview of the interactive layout
  interactive_monthly_trend.html         - Plotly line chart, hover tooltips
  interactive_product_by_region.html     - Plotly bar chart with region dropdown
  interactive_quantity_price.html        - Plotly bubble scatter, hover detail
  interactive_dashboard.html             - all interactive charts combined, 2x2
```

## Dashboard Guide - what each visualization shows

**01 - Total Sales by Region (bar)**
Quick read on where revenue is concentrated. North leads; use this as the
starting point before drilling into product or customer detail.

**02 - Price Distribution by Product (box plot)**
Shows the spread and outliers in unit price per product category. Wide boxes or
long whiskers flag products with inconsistent pricing (worth checking discounting
or bundling behavior).

**03 - Order Value Distribution by Region (violin plot)**
Combines a box plot with a density curve, so you see not just the median order
value per region but where order values cluster. A region with a fat lower bulge
is doing a lot of small orders even if its total revenue looks fine.

**04 - Correlation Heatmap (Quantity, Price, Total_Sales)**
Sanity-check on the numeric relationships — confirms Total_Sales is driven by
both quantity and price, and that quantity and price aren't strongly correlated
with each other (i.e., no obvious "expensive items get bought in bulk" pattern
here).

**05 - Revenue Heatmap: Region x Product**
The real cross-tab — which product is winning in which region. More actionable
than the region-only or product-only bar charts alone.

**06 - Static 2x2 Dashboard**
Box plot + violin + correlation heatmap + monthly trend line, one static image,
same color palette throughout — the "print this and hand it to someone" version.

**07 / interactive_dashboard.html - Interactive Dashboard**
Same four-panel idea as 06, but live: hover any point/bar for exact values.
`interactive_dashboard.html` is the file to open for the actual interactive
experience; `07_...preview.png` is a static fallback image of the same layout
(this environment doesn't have headless Chrome, which Plotly needs to export
interactive charts to PNG directly — see Technical Details below).

**interactive_monthly_trend.html**
Line chart of monthly revenue with hover tooltips showing exact dollar
values per month.

**interactive_product_by_region.html**
Bar chart of product revenue with a dropdown to filter by region (or view all
regions combined) — lets you answer "what sells best in the North?" without
a separate chart per region.

**interactive_quantity_price.html**
Bubble scatter of quantity vs. price, bubble size = order value, colored by
product, with customer/region/date on hover — useful for spotting whether big
orders are high-quantity, high-price, or both.

## Technical Details

- **Data prep**: `Date` parsed to datetime; `Month`/`MonthNum` extracted for
  grouping and chart ordering (`MonthNum` keeps months in calendar order since
  string month names would sort alphabetically).
- **Aggregations**: region totals, product totals, region x product pivot table,
  and a numeric correlation matrix — covers grouping, pivoting, and correlation
  in one pass.
- **Static charts**: seaborn on top of matplotlib, one consistent palette
  (`PALETTE` list) and `whitegrid` theme reused across every chart so the
  dashboard doesn't look like five different tools were used.
- **Interactive charts**: Plotly Express for the simple ones (line, scatter),
  `graph_objects` + `updatemenus` for the dropdown-filtered bar chart, and
  `make_subplots` to combine four chart types (scatter, bar, bar, heatmap) into
  one interactive figure.
- **GIF**: built by resizing and padding the six static PNGs to a common canvas
  and writing them as animation frames with `imageio` (1.5s per frame, looping).
  It's a slideshow-style preview of the chart set, not a screen recording of
  live interaction — Plotly's hover/dropdown behavior only exists in the HTML
  files, which can't be captured as a GIF without a real browser session.

## Testing Evidence

- `dashboard.ipynb` was executed end-to-end with `jupyter nbconvert --execute`;
  0 errors across all cells (checked programmatically by scanning cell outputs
  for `error` output types).
- Confirmed `sales_data.csv` has no missing values and 100/100 rows before
  aggregating (`df.isna().sum()` all zero, `df.describe()` count columns full).
- Spot-checked that `region_rev` and `product_rev` totals sum to the same
  overall total revenue figure as a cross-check on the groupby logic.
- Verified the region x product pivot table used for the heatmap sums back to
  the same total as the region-only and product-only aggregations.

## Headline Numbers

Total Revenue: $12,365,048 | Average Order Value: $123,650 | Top Region: North
($3,983,635) | Top Product: Laptop ($3,889,210)
