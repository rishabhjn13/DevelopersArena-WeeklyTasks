"""
generate_data.py
-----------------
One-time helper script used to generate the sample raw dataset
(data/sales_raw.csv) for the E-commerce Sales Analysis project.

Schema (as provided):
    Date, Product, Quantity, Price, Customer_ID, Region, Total_Sales

This is NOT part of the analysis pipeline. It exists only so the
dataset is reproducible. The real pipeline (main.py) reads
sales_raw.csv, cleans it, and writes sales_clean.csv.
"""

import random
import csv
from datetime import date, timedelta

random.seed(42)

# product -> typical unit price (INR)
products = {
    "Phone": 37300,
    "Laptop": 62500,
    "Tablet": 24800,
    "Headphones": 3200,
    "Smartwatch": 8900,
    "Charger": 900,
    "Speaker": 4500,
    "Camera": 45600,
}

regions = ["East", "West", "North", "South"]
customer_ids = [f"CUST{str(i).zfill(3)}" for i in range(1, 61)]

start_date = date(2024, 1, 1)
end_date = date(2024, 6, 30)

rows = []
current = start_date
while current <= end_date:
    num_transactions = random.choice([2, 3, 3, 4, 5])
    for _ in range(num_transactions):
        product = random.choice(list(products.keys()))
        price = products[product]
        quantity = random.randint(1, 10)
        total_sales = quantity * price
        rows.append([
            current.isoformat(),
            product,
            quantity,
            price,
            random.choice(customer_ids),
            random.choice(regions),
            total_sales,
        ])
    current += timedelta(days=1)

# --- Intentionally introduce messy / dirty data ---
# so the cleaning step in main.py has real work to do.

# 1. A few missing quantities
for i in [10, 80, 250]:
    if i < len(rows):
        rows[i][2] = ""

# 2. A few missing regions
for i in [20, 200]:
    if i < len(rows):
        rows[i][5] = ""

# 3. A negative quantity (return/refund logged incorrectly)
if len(rows) > 60:
    rows[60][2] = -3

# 4. A duplicate row
if len(rows) > 70:
    rows.append(rows[70][:])

# 5. Inconsistent region casing
for i in [25, 150]:
    if i < len(rows):
        rows[i][5] = rows[i][5].lower()

# 6. Total_Sales that doesn't match Quantity * Price (data entry error)
if len(rows) > 100:
    rows[100][6] = rows[100][6] + 999999

# 7. A missing product name
if len(rows) > 300:
    rows[300][1] = ""

# 8. A zero price (invalid)
if len(rows) > 400:
    rows[400][3] = 0
    rows[400][6] = 0

random.shuffle(rows)

with open("sales_raw.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Date", "Product", "Quantity", "Price", "Customer_ID", "Region", "Total_Sales"])
    writer.writerows(rows)

print(f"Generated {len(rows)} raw transaction rows -> sales_raw.csv")
