# What Drives Property Price? — Real World Business Analysis

Capstone project analyzing 300 property listings to identify which attributes actually drive sale price, using data cleaning, exploratory data analysis, feature engineering, and formal hypothesis testing.

## Overview

Real estate pricing is often guesswork. This project puts that guesswork to the test on a dataset of 300 property listings across 8 attributes — Property_ID, Area, Bedrooms, Bathrooms, Age, Location, Property_Type, and Price — to determine, with statistical validation rather than visual impressions, which factors genuinely move price and which are noise.

**Primary objective:** Identify which property attributes are meaningfully associated with sale price, quantify the strength of those relationships, and validate them statistically.

**Secondary objective:** Produce a clean, documented, reproducible dataset (`clean_data.csv`) and analysis pipeline suitable as a foundation for future predictive modeling.

## Key Findings

| Factor | Effect on Price |
|---|---|
| **Area (size)** | Strong — the single biggest driver |
| **Location** | Strong — City Center > Suburb > Rural |
| **Property Type** | None (not statistically significant, p = 0.062) |
| **Bedrooms / Bathrooms / Age** | Minimal to none |

- Property size (**Area**) is the strongest driver of price, both by correlation strength (**r = 0.80**) and statistical significance (**p < 0.001**).
- **Location** has a significant, ordered effect on price — City Center sells for roughly double Rural on average (ANOVA **p < 0.001**) — confirmed at the price-per-sqft level too, so it isn't just a size artifact.
- **Property_Type** (House, Villa, Apartment) does not meaningfully affect price once other factors are accounted for (**p = 0.062**, just above the significance threshold).
- **Bedrooms, Bathrooms, and Age** show weak or negligible individual relationships with price.
- **Location and Property_Type are statistically independent** of each other (p = 0.978) — no location specializes in a particular property type.

**Business implication:** Pricing and valuation efforts should prioritize Area and Location. Property_Type, bedroom/bathroom count, and age can largely be deprioritized in pricing models — they add complexity without adding predictive value.

## Methodology

The analysis follows a three-stage notebook pipeline, each stage answering a distinct question:

| Stage | Notebook | Question Answered |
|---|---|---|
| 1. Clean | `1_data_cleaning.ipynb` | Is the data trustworthy? |
| 2. Explore | `2_eda.ipynb` | What patterns exist? |
| 3. Test | `3_analysis.ipynb` | Are those patterns statistically real? |

Analysis was conducted in Python using **pandas** for data manipulation, **matplotlib / seaborn** for visualization, and **scipy.stats** for hypothesis testing. Each notebook is independently re-runnable against the source CSV and feeds its output into the next stage.

### 1. Data Cleaning (`1_data_cleaning.ipynb`)

Loads `raw_data.csv` and runs a six-point data quality checklist — missing values, duplicate rows, duplicate IDs, data types, invalid/negative values, and statistical outliers (IQR method) — then exports `clean_data.csv`. The dataset passed all checks as received; the only transformation applied was casting `Location` and `Property_Type` to categorical dtype.

### 2. Exploratory Data Analysis (`2_eda.ipynb`)

- **Univariate:** distribution shape, spread, and skew for each numeric column (Area, Bedrooms, Bathrooms, Age, Price) via histograms and boxplots, plus category balance for Location and Property_Type.
- **Bivariate:** correlation heatmap and scatter plots (numeric vs. numeric), boxplots of price by category (numeric vs. categorical), and a Location × Property_Type crosstab (categorical vs. categorical).

### 3. Feature Engineering

Derived `Price_per_sqft` (Price ÷ Area) to normalize price by size and enable fair comparison across listings of different scale. It preserved the same Location ordering as raw price, confirming the Location effect is a genuine per-unit value difference, not just a byproduct of larger properties.

### 4. Hypothesis Testing (`3_analysis.ipynb`)

Four tests, each matched to the variable types involved, run at significance level **α = 0.05**:

| Test | Question | Statistic | p-value | Conclusion |
|---|---|---|---|---|
| One-way ANOVA | Does Location affect Price? | F = 58.68 | < 0.001 | Significant |
| One-way ANOVA | Does Property_Type affect Price? | F = 2.80 | 0.062 | Not significant |
| Pearson correlation | Is the Area–Price correlation real? | r = 0.80 | < 0.001 | Significant |
| Chi-square | Are Location and Property_Type associated? | χ² = 0.45 | 0.978 | Not significant |

## Dataset

| Column | Type | Description |
|---|---|---|
| Property_ID | Text | Unique identifier per listing |
| Area | Integer | Property size in square feet |
| Bedrooms | Integer | Number of bedrooms (1–5) |
| Bathrooms | Integer | Number of bathrooms (1–3) |
| Age | Integer | Property age in years (0–49) |
| Location | Category | City Center / Suburb / Rural |
| Property_Type | Category | House / Villa / Apartment |
| Price | Integer | Sale price (INR) |

- 300 records, 8 attributes, no missing values, no duplicates, no outliers.
- `clean_data.csv` is content-identical to the raw file except for the categorical dtype adjustment.

## Repository Structure

```
.
├── raw_data.csv              # Original, unmodified source data
├── clean_data.csv            # Validated dataset used throughout the analysis
├── 1_data_cleaning.ipynb     # Data profiling, quality checks, export to clean_data.csv
├── 2_eda.ipynb               # Univariate and bivariate exploratory analysis
├── 3_analysis.ipynb          # Hypothesis testing (ANOVA, Pearson correlation, Chi-square)
├── Technical_Report.docx     # Full methodology and detailed statistical results
├── Executive_Report.docx     # One-page business-facing summary of findings
├── business_presentation.pptx # Slide deck walking through the full analysis
└── README.md                 # This file
```

## Reports

- **[Technical_Report.docx](./Technical_Report.docx)** — full write-up covering methodology, data preparation, EDA, feature engineering, hypothesis testing, limitations, and recommendations. Read this for the complete statistical detail.
- **[Executive_Report.docx](./Executive_Report.docx)** — one-page, business-facing summary of the key findings and their implications for pricing strategy.
- **[business_presentation.pptx](./business_presentation.pptx)** — slide deck summarizing the analysis pipeline and findings for a non-technical audience.

## How to Reproduce

1. Ensure `raw_data.csv` is present in the project root.
2. Run the notebooks in order:
   ```
   1_data_cleaning.ipynb   →   2_eda.ipynb   →   3_analysis.ipynb
   ```
3. Each notebook re-runs independently against the source CSV and regenerates its own outputs (`clean_data.csv`, figures, and test statistics).

**Requirements:** Python 3.x, `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`.

## Limitations

- Dataset size is moderate (n = 300); findings may not generalize beyond this sample's distribution.
- The dataset had no missing values, duplicates, or outliers — cleaner than most real-world data — so the cleaning stage demonstrates methodology more than it reflects a difficult cleaning problem.
- Statistical significance indicates association, not causation — Location's effect on price may be mediated by unmeasured factors such as local demand or infrastructure.
- Only linear correlation (Pearson) was tested for numeric relationships; non-linear relationships were not explored.
- The Property_Type result (p = 0.062) is borderline; a larger sample could shift this conclusion in either direction.

## Recommendations & Next Steps

- Build a regression model predicting Price from Area, Location, and Price_per_sqft to quantify combined variance explained (R²).
- Deprioritize Property_Type, Bedrooms, Bathrooms, and Age as pricing factors given their weak/non-significant individual effects.
- Collect a larger sample to re-test the borderline Property_Type result with greater statistical power.
- Investigate potential interaction effects, e.g. whether the Area–Price relationship differs by Location.

## Author

Rishabh
