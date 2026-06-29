# 📊 Sales Data Analysis — Week 3

A Python data analysis script that loads a CSV sales dataset, cleans it, analyzes key metrics, and prints a formatted summary report. Built as the Week 3 project covering **Pandas** for real-world data analysis.

## 📖 About

This project applies Week 3 concepts using the Pandas library:

| Concept | Where it's used |
|---|---|
| `pd.read_csv()` | Load sales data from a CSV file |
| `df.head()`, `df.shape`, `df.dtypes` | Explore and understand the dataset |
| `fillna()`, `drop_duplicates()` | Clean missing values and remove duplicate rows |
| Column arithmetic | Create a `Total_Sales` column from `Quantity × Price` |
| `groupby()` + `idxmax()` | Find the best-selling product by quantity |
| Aggregations | Calculate total revenue, average sale, and highest single sale |

## 🛠️ Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## ▶️ How to Run

1. Place your `sales_data.csv` file in the same folder as the script.
2. Run:

```bash
python3 sales_analysis.py
```

## 📁 Expected CSV Format

Your `sales_data.csv` should have at least these columns:

| Product | Quantity | Price |
|---|---|---|
| Laptop | 5 | 45000 |
| Mouse | 20 | 500 |
| Monitor | 8 | 12000 |

> Missing `Quantity` values are filled with `0`. Missing `Product` values are filled with `"Unknown"`. Duplicate rows are removed automatically.

## 📊 Sample Output

```
--- Data Overview ---
  Product  Quantity    Price
0  Laptop       5.0  45000.0
1   Mouse      20.0    500.0
2 Monitor       8.0  12000.0

Dimensions: 3 rows, 3 columns

Data Types:
Product      object
Quantity    float64
Price       float64

==============================
SALES ANALYSIS REPORT
==============================
Total Revenue:        ₹331,000.00
Average Sale Value:   ₹110,333.33
Highest Single Sale:  ₹225,000.00
Best-Selling Product: Mouse
==============================
```

## 📁 Project Structure

```
.
├── README.md            # Project documentation
├── sales_analysis.py    # Main analysis script
├── sales_data.csv       # Input dataset (add your own)
├── requirements.txt     # Python dependencies
└── screenshots/         # Terminal screenshots of the output
```

