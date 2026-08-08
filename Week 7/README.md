# Statistical Business Analysis - Week 7

Statistics project on two business datasets - a sales log and a customer churn
extract. Covers descriptive stats, distribution checks, correlation, hypothesis
testing, confidence intervals and regression, wrapped up with business
recommendations.

## Project Overview

Goal: pull statistically backed insights out of raw sales and churn data rather
than eyeballing charts and guessing. Two questions drove the work:

- Does region, product or contract type actually move the numbers, or does it
  just look that way in a quick glance at the data?
- Which customer segments are most likely to churn, and does the sales data
  support any regional or product-level story worth acting on?

Everything in `statistical_analysis.ipynb` is reproducible from the two source
CSVs, no manual data edits were made outside of pandas code.

## Setup Instructions

1. Clone or download this repository.
2. Create a virtual environment (optional but recommended):
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Launch Jupyter and open the notebook:
   ```
   jupyter notebook statistical_analysis.ipynb
   ```
5. Run all cells top to bottom. The notebook reads `business_data.csv` and
   `customer_churn.csv` from the same directory, so keep the folder structure
   intact.

## Code Structure

```
.
├── statistical_analysis.ipynb      main notebook, all analysis and charts
├── business_data.csv               sales dataset (100 rows)
├── customer_churn.csv              churn dataset (500 rows)
├── statistical_report.pdf          write-up with methodology and results
├── hypothesis_tests_results.txt    plain-text log of all 5 hypothesis tests
├── requirements.txt                pinned package versions
├── screenshots/                    exported charts used in the notebook and report
│   ├── sales_distributions.png
│   ├── correlation_heatmap.png
│   ├── regression_fit.png
│   └── churn_boxplot.png
└── README.md                       this file
```

The notebook is organized day by day, matching the project brief:

1. Descriptive statistics
2. Distribution analysis (histograms, Shapiro-Wilk normality test)
3. Correlation analysis (Pearson correlation, heatmap)
4. Hypothesis testing (3 t-tests, 1 ANOVA, 1 chi-square)
5. Confidence intervals (sales average, churn rate, monthly charges)
6. Regression analysis (linear regression, logistic regression)
7. Business insights and recommendations

## Technical Details

- **Descriptive statistics**: computed with `pandas.DataFrame.describe()` plus
  `.mode()` for the mode, since `describe()` does not include it by default.
- **Distribution checks**: histograms with a KDE overlay via seaborn, tested
  for normality with `scipy.stats.shapiro`. All three sales metrics
  (Quantity, Price, Total_Sales) failed the normality check, which is why
  Welch's t-test was used downstream instead of assuming equal variances.
- **Correlation**: Pearson correlation via `scipy.stats.pearsonr`, since all
  variables involved are continuous and roughly linear in their relationship.
- **Hypothesis tests**: `scipy.stats.ttest_ind(..., equal_var=False)` for the
  three t-tests, `statsmodels.formula.api.ols` plus `anova_lm` for the
  one-way ANOVA, and `scipy.stats.chi2_contingency` for the chi-square test
  of independence between contract type and churn.
- **Confidence intervals**: t-distribution based intervals
  (`scipy.stats.t.interval`) for continuous metrics with unknown population
  variance, and a normal approximation (`scipy.stats.norm.interval`) for the
  churn rate proportion.
- **Regression**: ordinary least squares (`statsmodels.api.OLS`) for
  Total_Sales as a function of Quantity and Price, and a logistic regression
  (`statsmodels.api.Logit`) for Churn as a function of Tenure,
  MonthlyCharges and SeniorCitizen status.

## Testing Evidence

Manual validation performed while building this project:

- Row counts confirmed after load: `sales.shape` returns (100, 7),
  `churn.shape` returns (500, 9), matching the raw CSV line counts.
- Descriptive statistics cross-checked against `pandas.describe()` output
  directly, no discrepancies.
- t-test results checked against the raw group means printed alongside each
  test (see `hypothesis_tests_results.txt`) to confirm the direction of each
  effect matches the sign of the test statistic.
- Chi-square contingency table inspected manually (`pd.crosstab`) before
  running the test, to confirm no cell had an expected count below 5, which
  would have made the chi-square approximation unreliable.
- Regression assumptions spot-checked: residuals for the OLS model were
  visually inspected for the fitted vs actual plot in `screenshots/regression_fit.png`,
  and the logistic regression's pseudo R-squared and coefficient signs were
  checked against the boxplot in `screenshots/churn_boxplot.png` for
  consistency (higher charges and lower tenure line up with more churn in
  both the plot and the model).
- Notebook re-run from a clean kernel before submission to confirm every
  cell executes top to bottom without errors and outputs match what is
  reported in `statistical_report.pdf`.

## Visual Documentation

See `screenshots/` for the exported charts, also embedded directly in the
notebook and the PDF report:

- `sales_distributions.png` - histograms with density curves for Quantity,
  Price and Total_Sales
- `correlation_heatmap.png` - Pearson correlation matrix for the sales metrics
- `regression_fit.png` - actual vs predicted Total_Sales from the linear
  regression model
- `churn_boxplot.png` - monthly charges by contract type, split by churn
  status
