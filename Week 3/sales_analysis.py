import pandas as pd

# 1. Setup & Load Data
# Assuming 'sales_data.csv' exists with columns like 'Product', 'Quantity', 'Price'
df = pd.read_csv('sales_data.csv')

# 2. Explore Data
print("--- Data Overview ---")
print(df.head())
print(f"\nDimensions: {df.shape[0]} rows, {df.shape[1]} columns")
print("\nData Types:")
print(df.dtypes)

# 3. Clean Data
# Fill missing numeric values with 0 and categorical with 'Unknown'
df['Quantity'] = df['Quantity'].fillna(0)
df['Product'] = df['Product'].fillna('Unknown')
df.drop_duplicates(inplace=True)

# 4. Analyze Sales
# Calculate Total Revenue per row
df['Total_Sales'] = df['Quantity'] * df['Price']

total_revenue = df['Total_Sales'].sum()
avg_sales = df['Total_Sales'].mean()
highest_sale = df['Total_Sales'].max()

# Find best-selling product by quantity
best_product = df.groupby('Product')['Quantity'].sum().idxmax()

# 5. Create Report
print("\n" + "="*30)
print("SALES ANALYSIS REPORT")
print("="*30)
print(f"Total Revenue:      ₹{total_revenue:,.2f}")
print(f"Average Sale Value: ₹{avg_sales:,.2f}")
print(f"Highest Single Sale: ₹{highest_sale:,.2f}")
print(f"Best-Selling Product: {best_product}")
print("="*30)