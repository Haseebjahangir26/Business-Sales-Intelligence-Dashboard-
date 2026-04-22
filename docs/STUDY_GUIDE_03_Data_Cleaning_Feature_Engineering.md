# STUDY GUIDE — Chapter 3: Data Cleaning & Feature Engineering
# The Core Data Science Work

---

## 3.1 What is Data Cleaning?

In the real world, raw data is almost always **dirty**. It has:
- Missing values (blanks, NaN)
- Duplicate rows
- Inconsistent formatting (upper/lowercase, date formats)
- Invalid values (negative quantities, future dates)
- Outliers (extreme values that skew results)

Data cleaning is the process of fixing all of this so your analysis is based on accurate data.

> Rule of thumb: In a real data job, you'll spend **60–80% of your time cleaning data**.

---

## 3.2 The Data Cleaning Checklist

Every time you get a new dataset, do these in order:

### Step 1: Shape Check
```python
print(df.shape)          # how many rows and columns?
print(df.dtypes)         # what type is each column?
print(df.head())         # what does the data actually look like?
```

### Step 2: Missing Value Audit
```python
print(df.isnull().sum())              # nulls per column
print(df.isnull().sum() / len(df) * 100)  # null % per column
```

### Step 3: Duplicate Check
```python
print(df.duplicated().sum())   # number of duplicate rows
```

### Step 4: Value Distribution Check
```python
print(df.describe())           # stats for numeric columns
print(df["category"].value_counts())  # frequency of each category
```

### Step 5: Fix Issues (in order)
1. Drop duplicates
2. Parse/fix data types (especially dates)
3. Normalize text (casing, whitespace)
4. Remove invalid rows
5. Impute (fill in) missing values

---

## 3.3 Why Order Matters

You must handle duplicates **before** imputing nulls.

Why? If row A is a duplicate of row B, and row A has a null but row B doesn't, imputing first would fill the null in row A, making it look like a valid unique row. Then you'd fail to drop it as a duplicate.

**Always: drop duplicates → fix types → fix text → remove invalids → impute nulls.**

---

## 3.4 Types of Missing Data

| Type | What it means | Example |
|------|--------------|---------|
| MCAR | Missing Completely At Random | Server randomly dropped rows |
| MAR | Missing At Random (related to other columns) | Online orders more likely to miss phone number |
| MNAR | Missing Not At Random | High-value customers hid income |

For this project: mostly MCAR (random simulation). In real life, understanding *why* data is missing changes how you fill it.

---

## 3.5 Imputation Strategies

**Imputation** = filling in missing values with an estimate.

| Strategy | When to use | Code |
|----------|-----------|------|
| Known formula | You can calculate the value exactly | `unit_price × quantity` |
| Mean | Normal distribution, no outliers | `df["col"].mean()` |
| Median | Skewed data, has outliers | `df["col"].median()` |
| Mode | Categorical data | `df["col"].mode()[0]` |
| Forward fill | Time-series (carry last known value forward) | `df["col"].ffill()` |
| Group median | Different categories have different distributions | `df.groupby("cat")["col"].transform("median")` |
| Constant | Categorical missing, no better info | `"Unknown"` |

**Why median over mean for cost?**

Mean is affected by outliers. If most products have a 50% cost ratio but 2 bad SKUs have a 96% ratio, the mean gets pulled high. Median ignores extremes — it's the middle value when sorted.

```python
mean_cost = [50, 50, 52, 48, 96, 95]
# mean: 65.2  ← inflated by the outliers
# median: 51  ← more representative of typical cost
```

In our project:
```python
# Group median by category — each category gets its own median cost ratio
cat_cost_pct = df.groupby("category")["cost_pct"].transform("median")
df.loc[df["cost"].isna(), "cost"] = (
    df["revenue"] * cat_cost_pct
).round(2)
```

`transform("median")` — unlike `agg`, transform returns a Series with the **same length as the original DataFrame**, so you can use it directly to fill values.

---

## 3.6 Date Parsing — The Hardest Cleaning Task

Dates are the most error-prone column. Real datasets have multiple date formats because data comes from different systems.

Common formats:
```
MM/DD/YYYY  → 01/15/2023   (American)
YYYY-MM-DD  → 2023-01-15   (ISO standard)
DD-Mon-YYYY → 15-Jan-2023  (abbreviated month)
DD/MM/YYYY  → 15/01/2023   (European)
```

The challenge: `01/02/2023` is **ambiguous** — is it January 2nd or February 1st?

Our solution — try each format, use the first one that works:
```python
def parse_date(val):
    if pd.isna(val):
        return pd.NaT
    for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%d-%b-%Y", "%d/%m/%Y"):
        try:
            return pd.to_datetime(val, format=fmt)
        except (ValueError, TypeError):
            pass
    return pd.to_datetime(val, errors="coerce")   # last resort
```

`errors="coerce"` means: if parsing still fails, return `NaT` instead of crashing.

Then apply to every row:
```python
df["sale_date"] = df["sale_date"].apply(parse_date)
df = df.dropna(subset=["sale_date"])   # drop rows where date is still NaT
```

---

## 3.7 Normalization vs Standardization

Two common transformations for making data consistent:

**Normalization (text):** Making text consistent. In our project — category names.
```python
# These are all the same category:
"electronics", "ELECTRONICS", "Electronics", " Electronics "

# Fix all at once:
df["category"] = df["category"].str.strip().str.title()
# Result: all become "Electronics"
```

**Standardization (numbers):** Scaling numbers to the same range.
```python
# Min-Max scaling → range becomes 0 to 1
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df["revenue_scaled"] = scaler.fit_transform(df[["revenue"]])
```

Not used in this project (we didn't need it), but you'll see it in machine learning.

---

## 3.8 Outlier Detection

**Outliers** are values that are far from the rest. They can skew your analysis.

IQR Method (used in statistics):
```python
Q1 = df["revenue"].quantile(0.25)   # 25th percentile
Q3 = df["revenue"].quantile(0.75)   # 75th percentile
IQR = Q3 - Q1                       # interquartile range

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df["revenue"] < lower_bound) | (df["revenue"] > upper_bound)]
```

In our project — negative quantities are our "outliers":
```python
neg_mask = df["quantity"] < 0
print(f"Negative qty rows: {neg_mask.sum()}")
df = df[~neg_mask].copy()   # remove them
```

---

## 3.9 What is Feature Engineering?

Feature engineering is creating new columns (features) from existing data to make analysis easier or more powerful.

Raw data doesn't always have the columns you need. You derive them.

| Original Column | Engineered Feature | How |
|----------------|-------------------|-----|
| `sale_date` | `month_year` | Extract month from date |
| `sale_date` | `month_num` | Extract month number for sorting |
| `revenue`, `cost` | `profit` | Subtraction |
| `profit`, `revenue` | `profit_margin_pct` | Division × 100 |
| `revenue` | `revenue_band` | Classify into Low/Medium/High |

---

## 3.10 Why Feature Engineering Matters

Example: You have `revenue` and `cost` but not `profit_margin_pct`.

Without it:
- SKU-A: Revenue $10,000, Cost $9,500 ← barely profitable but high revenue
- SKU-B: Revenue $1,000, Cost $400   ← 60% margin, very profitable

Sorted by revenue alone, SKU-A looks better. Sorted by margin, SKU-B is clearly better.
**Margin is the feature that reveals the truth.**

---

## 3.11 Profit Margin — The Key Business Metric

```
Profit = Revenue - Cost
Profit Margin % = (Profit / Revenue) × 100
```

Example:
```
Revenue = $500
Cost    = $300
Profit  = $200
Margin  = ($200 / $500) × 100 = 40%
```

A 40% margin means for every $100 sold, $40 is actual profit.

**Industry benchmarks:**
- Retail: 20–40% is healthy
- Software: 60–80% (low cost, high margin)
- Grocery: 1–5% (very thin margins — high volume business)

Our bad SKUs had margins of 1–6% — for a mixed retail business, that's terrible.

---

## 3.12 Cost Ratio / Cost Percentage

```
Cost Ratio = Cost / Revenue
```

A cost ratio of 0.94 means 94 cents of every dollar in revenue goes to cost.
Only 6 cents is profit. That's nearly break-even.

In our project:
```python
# generate_raw_data.py
CATEGORIES = {
    "Electronics": {"cost_pct_range": (0.45, 0.65)},  # 45-65% cost ratio
}
# Bad SKUs:
if sku in BAD_SKUS:
    cost_pct = random.uniform(0.94, 0.99)   # 94-99% cost ratio → terrible
    cost = round(revenue * cost_pct, 2)
```

---

## 3.13 Revenue Bands (Bucketing / Binning)

Instead of working with exact revenue numbers, sometimes you classify them into buckets:
- Low revenue transactions
- Medium revenue transactions
- High revenue transactions

```python
# Method 1: Using quantiles
rev_q1 = df["revenue"].quantile(0.33)   # 33rd percentile
rev_q2 = df["revenue"].quantile(0.67)   # 67th percentile

def rev_band(r):
    if r <= rev_q1:   return "Low"
    elif r <= rev_q2: return "Medium"
    return "High"

df["revenue_band"] = df["revenue"].apply(rev_band)
```

This means each band has roughly equal numbers of rows (not equal revenue ranges).

---

## 3.14 What is EDA (Exploratory Data Analysis)?

EDA is the process of **exploring** the data to understand it before drawing conclusions.

It answers:
- What's the distribution of each variable?
- Are there correlations between variables?
- Are there any surprising patterns or anomalies?
- What questions does this data raise?

EDA tools:
- Summary statistics (`describe()`)
- Value counts (`value_counts()`)
- Charts (histograms, boxplots, scatter plots, bar charts)
- Correlation matrices

In our project, the 8 charts are the EDA output:
1. Monthly revenue → trend analysis
2. Monthly margin → margin volatility
3/4. Top products → ranking analysis
5. Top customers → customer analysis
6. Category pie → portfolio composition
7. SKU waterfall → what-if analysis
8. Region heatmap → geographic analysis

---

## 3.15 What-If Analysis (SKU Rationalization)

"What if we removed the two worst-performing SKUs? How would that change our total margin?"

```python
# Full portfolio margin:
full_revenue = df["revenue"].sum()
full_profit  = df["profit"].sum()
full_margin  = full_profit / full_revenue * 100

# Portfolio without bad SKUs:
df_clean = df[~df["sku"].isin(["SKU-098", "SKU-099"])].copy()
clean_revenue = df_clean["revenue"].sum()
clean_profit  = df_clean["profit"].sum()
clean_margin  = clean_profit / clean_revenue * 100

# Impact:
improvement = clean_margin - full_margin
print(f"Margin improvement: +{improvement:.2f} percentage points")
```

This is **business intelligence** — using data to make a specific, actionable recommendation.

The key output:
- Before: X% overall margin
- After removing 2 SKUs: X + improvement% margin
- Recommendation: Discontinue SKU-098 and SKU-099

---

## 3.16 The Full Pipeline Pattern

Professional data projects follow a pipeline pattern:

```
Raw Data
   ↓
[Stage 1] Data Generation     → Creates realistic messy data
   ↓
[Stage 2] Clean + Engineer    → Fixes issues, creates new features
   ↓
[Stage 3] EDA + Visualize     → Explores data, creates charts
   ↓
[Stage 4] Report              → Packages insights for stakeholders
```

Each stage reads from the previous stage's output (saved as CSV files).

Why save to CSV between stages?
- You can run stages independently (don't regenerate data every time)
- Easy to inspect intermediate results
- Stages are decoupled — one stage failing doesn't break another

In our project:
```python
# Each stage saves its output:
df.to_csv("data/processed/clean_sales_data.csv", index=False)

# The next stage reads it:
df = pd.read_csv("data/processed/clean_sales_data.csv")
```

---

## 3.17 Data Quality Metrics (Professional Standard)

When you present your cleaning work, use these metrics:

```
Dataset: 10,815 raw rows
After cleaning:
  - Duplicates removed: 315 rows (2.9%)
  - Invalid quantities removed: 108 rows (1.0%)
  - Revenue imputed: 536 cells (5.0%)
  - Cost imputed: 429 cells (4.0%)
  - Customer names filled: 212 cells (2.0%)
Final clean dataset: 10,392 rows (96.1% of original)
```

Always report: what you did, how many rows/cells were affected, what % of the data was impacted.

---

## 3.18 What You Now Know

You now understand:
- The complete data cleaning workflow
- Why cleaning order matters
- Types of missing data and imputation strategies
- Date parsing — the hardest cleaning problem
- Text normalization
- Outlier detection
- Feature engineering — deriving useful metrics
- Profit margin, cost ratio — the key business metrics
- EDA — exploring data before analyzing
- What-if / scenario analysis
- The pipeline pattern in professional projects

**Next:** Chapter 4 — Matplotlib & Seaborn (building the 8 charts).
