# STUDY GUIDE — Chapter 2: NumPy & Pandas
# The Core Data Science Libraries

---

## 2.1 What is NumPy?

NumPy (Numerical Python) is a library for fast math on large arrays of numbers.
Pandas is built on top of NumPy — so understanding NumPy basics helps you understand Pandas.

```python
import numpy as np
```

---

## 2.2 NumPy Arrays

A NumPy array is like a Python list, but faster and supports math operations on the whole array at once.

```python
import numpy as np

# Create an array
arr = np.array([1, 2, 3, 4, 5])

# Math on the whole array at once:
arr * 2          # array([2, 4, 6, 8, 10])
arr + 10         # array([11, 12, 13, 14, 15])
arr ** 2         # array([1, 4, 9, 16, 25])

# Statistics:
np.mean(arr)     # 3.0
np.median(arr)   # 3.0
np.std(arr)      # 1.41...  (standard deviation)
np.min(arr)      # 1
np.max(arr)      # 5
np.sum(arr)      # 15
```

---

## 2.3 NumPy Random (used in our project)

```python
np.random.seed(42)              # reproducible randomness
np.random.random()              # random float 0.0 to 1.0
np.random.uniform(0.4, 0.6)    # random float in range
np.random.randint(1, 50)       # random int in range
```

In our project:
```python
# generate_raw_data.py
np.random.seed(42)    # seed set at the top — all randomness reproducible
```

---

## 2.4 NaN in NumPy

```python
np.nan           # the "Not a Number" value
np.isnan(np.nan) # True
np.isnan(0)      # False
```

In our project:
```python
# Inject missing values into the dataset:
df.loc[mask_rev, "revenue"] = np.nan    # set selected cells to NaN
```

---

## 2.5 What is Pandas?

Pandas is the most important data science library. It gives you the **DataFrame** — a table of data with rows and columns, like an Excel spreadsheet but in Python.

```python
import pandas as pd
```

Two core objects:
- **Series** — a single column (1D)
- **DataFrame** — a full table (2D, rows × columns)

---

## 2.6 Creating a DataFrame

```python
import pandas as pd

# From a list of dicts (each dict = one row):
data = [
    {"name": "Alice", "score": 90, "grade": "A"},
    {"name": "Bob",   "score": 75, "grade": "B"},
    {"name": "Carol", "score": 82, "grade": "B"},
]
df = pd.DataFrame(data)
```

This creates:
```
    name  score grade
0  Alice     90     A
1    Bob     75     B
2  Carol     82     B
```

The numbers on the left (0, 1, 2) are the **index** — row labels.

---

## 2.7 Reading CSV Files

```python
df = pd.read_csv("raw_sales_data.csv")
```

This reads the file and creates a DataFrame automatically.

In our project:
```python
# clean_and_engineer.py
df = pd.read_csv("raw_sales_data.csv")
print(f"Raw rows loaded : {len(df):,}")
```

---

## 2.8 Exploring a DataFrame (First Things to Do)

```python
df.shape           # (rows, columns) — e.g., (10815, 12)
df.head()          # first 5 rows
df.head(10)        # first 10 rows
df.tail()          # last 5 rows
df.info()          # column names, data types, non-null counts
df.describe()      # stats: count, mean, std, min, max, quartiles
df.columns         # list of column names
df.dtypes          # data type of each column
len(df)            # number of rows
```

---

## 2.9 Selecting Data

```python
# Single column → returns a Series
df["revenue"]              # the revenue column
df.revenue                 # same thing (dot notation)

# Multiple columns → returns a DataFrame
df[["sku", "revenue", "cost"]]

# Single row by index number
df.iloc[0]                 # first row
df.iloc[-1]                # last row
df.iloc[0:5]               # first 5 rows

# Row by label/condition
df.loc[df["sku"] == "SKU-001"]    # rows where sku is SKU-001
```

---

## 2.10 Filtering Rows (Boolean Indexing)

This is the most important Pandas skill. You create a True/False mask and apply it.

```python
# Mask: True for rows where revenue > 1000
mask = df["revenue"] > 1000

# Apply mask — keep only True rows:
df[mask]
# or in one line:
df[df["revenue"] > 1000]
```

Combining conditions:
```python
# AND — both must be true
df[(df["revenue"] > 1000) & (df["category"] == "Electronics")]

# OR — either can be true
df[(df["category"] == "Electronics") | (df["category"] == "Furniture")]

# NOT — invert
df[~(df["sku"].isin(["SKU-098", "SKU-099"]))]
```

In our project:
```python
# clean_and_engineer.py
neg_mask = df["quantity"] < 0
df = df[~neg_mask].copy()    # keep rows where quantity is NOT negative
```

```python
# sku_removal_impact analysis
df_clean = df[~df["sku"].isin(["SKU-098", "SKU-099"])]
```

---

## 2.11 The `.isin()` Method

Check if values are in a list:
```python
df["sku"].isin(["SKU-098", "SKU-099"])
# Returns True for every row where sku is SKU-098 or SKU-099
```

---

## 2.12 Adding New Columns

```python
# Simple math:
df["profit"] = df["revenue"] - df["cost"]

# Percentage:
df["margin_pct"] = df["profit"] / df["revenue"] * 100

# Round it:
df["margin_pct"] = (df["profit"] / df["revenue"] * 100).round(2)

# From existing column:
df["month_num"] = df["sale_date"].dt.month
```

In our project:
```python
# clean_and_engineer.py — feature engineering section
df["profit"]            = (df["revenue"] - df["cost"]).round(2)
df["profit_margin_pct"] = ((df["profit"] / df["revenue"]) * 100).round(2)
df["month_year"]        = df["sale_date"].dt.to_period("M").astype(str)
df["month_num"]         = df["sale_date"].dt.month
```

---

## 2.13 Handling Missing Data (Nulls)

```python
# Check for nulls:
df.isnull()                  # DataFrame of True/False
df.isnull().sum()            # count nulls per column
df["revenue"].isna().sum()   # count nulls in one column

# Drop rows with any null:
df.dropna()

# Drop rows with null in specific column:
df.dropna(subset=["sale_date"])

# Fill nulls with a value:
df["customer_name"] = df["customer_name"].fillna("Unknown Customer")

# Fill nulls with math:
df.loc[df["revenue"].isna(), "revenue"] = df["unit_price"] * df["quantity"]
```

The key imputation strategies used in our project:

| Column | Strategy | Why |
|--------|---------|-----|
| `revenue` | `unit_price × quantity` | We have both inputs, can calculate exactly |
| `cost` | Category median cost ratio | Best estimate without exact info |
| `customer_name` | `"Unknown Customer"` | Transaction is valid, just unattributed |

---

## 2.14 Dropping Duplicates

```python
df.duplicated()               # True/False for each row
df.duplicated().sum()         # count of duplicate rows
df.drop_duplicates()          # return df with duplicates removed
df.drop_duplicates(inplace=True)   # modify df directly
```

In our project:
```python
before = len(df)
df.drop_duplicates(inplace=True)
print(f"Dropped {before - len(df)} duplicates")
```

---

## 2.15 String Operations on Columns

Pandas has a `.str` accessor that applies string methods to every row in a column:

```python
df["category"].str.upper()          # all caps
df["category"].str.lower()          # all lowercase
df["category"].str.title()          # Title Case
df["category"].str.strip()          # remove leading/trailing spaces
df["category"].str.contains("Elec") # True/False — does it contain this?
df["category"].str.replace("old","new")
df["customer_name"].str.split(" ")  # split on space
```

Chain them:
```python
df["category"] = df["category"].str.strip().str.title()
# First strip whitespace, then title-case
```

---

## 2.16 Working with Dates

Pandas has powerful date/time support. First convert a column to datetime type:

```python
df["sale_date"] = pd.to_datetime(df["sale_date"])
```

Then access date parts with `.dt`:

```python
df["sale_date"].dt.year          # 2023
df["sale_date"].dt.month         # 1-12
df["sale_date"].dt.day           # 1-31
df["sale_date"].dt.day_name()    # "Monday", "Tuesday", etc.
df["sale_date"].dt.to_period("M")  # "2023-01", "2023-02", etc.
```

Converting back to string for CSV output:
```python
df["sale_date"] = df["sale_date"].dt.strftime("%Y-%m-%d")
# "2023-01-15"
```

---

## 2.17 groupby — The Most Powerful Pandas Tool

`groupby` splits the data into groups, applies a function to each group, and combines the results.
Think of it like pivot tables in Excel.

```python
# Sum of revenue for each category:
df.groupby("category")["revenue"].sum()

# Multiple aggregations at once:
summary = df.groupby("category").agg(
    total_revenue = ("revenue", "sum"),
    total_profit  = ("profit",  "sum"),
    order_count   = ("order_id","count"),
    avg_margin    = ("profit_margin_pct", "mean"),
)
```

`agg()` takes: `new_column_name = ("source_column", "function")`

Functions you can use: `"sum"`, `"mean"`, `"count"`, `"min"`, `"max"`, `"median"`, `"nunique"`, `"std"`

In our project:
```python
# clean_and_engineer.py — monthly summary
monthly = (
    df.groupby(["month_year", "month_num"])
    .agg(
        total_revenue    = ("revenue", "sum"),
        total_cost       = ("cost",    "sum"),
        total_profit     = ("profit",  "sum"),
        total_orders     = ("order_id","count"),
        avg_order_value  = ("revenue", "mean"),
        unique_customers = ("customer_name", "nunique"),
    )
    .reset_index()       # moves group keys back to regular columns
    .sort_values("month_num")   # sort by month number
)
```

---

## 2.18 reset_index()

After `groupby`, the group keys become the index. `reset_index()` moves them back to regular columns.

```python
result = df.groupby("category")["revenue"].sum()
# category is now the index — accessing it is awkward

result = df.groupby("category")["revenue"].sum().reset_index()
# Now category is a normal column again
```

---

## 2.19 sort_values()

```python
df.sort_values("revenue")                      # ascending (low to high)
df.sort_values("revenue", ascending=False)     # descending (high to low)
df.sort_values(["category", "revenue"])        # sort by multiple columns

# nlargest / nsmallest — shortcut for top N
df.nlargest(10, "revenue")    # top 10 by revenue
df.nsmallest(5, "profit")     # bottom 5 by profit
```

---

## 2.20 Applying a Custom Function to a Column

```python
def classify(revenue):
    if revenue < 100:
        return "Low"
    elif revenue < 500:
        return "Medium"
    else:
        return "High"

df["revenue_band"] = df["revenue"].apply(classify)
```

Or with a lambda (anonymous function):
```python
df["revenue_band"] = df["revenue"].apply(lambda r: "Low" if r < 100 else "High")
```

In our project:
```python
def rev_band(r):
    if r <= rev_q1:   return "Low"
    elif r <= rev_q2: return "Medium"
    return "High"

df["revenue_band"] = df["revenue"].apply(rev_band)
```

---

## 2.21 pd.cut() — Binning / Bucketing

A cleaner way to classify numerical values into categories:

```python
df["revenue_band"] = pd.cut(
    df["revenue"],
    bins=[-1, 100, 500, float("inf")],    # bin edges
    labels=["Low", "Medium", "High"]      # labels for each bin
)
```

---

## 2.22 Saving a DataFrame to CSV

```python
df.to_csv("output.csv", index=False)
# index=False means don't write the row numbers (0,1,2,...) to the file
```

In our project:
```python
df.to_csv("data/processed/clean_sales_data.csv", index=False)
monthly.to_csv("data/processed/monthly_summary.csv", index=False)
```

---

## 2.23 The .copy() Method

When you filter a DataFrame, you get a **view** of the original — not an independent copy.
Modifying a view can cause warnings. Use `.copy()` to get a real independent copy.

```python
df_clean = df[~df["sku"].isin(["SKU-098","SKU-099"])].copy()
df_clean["new_column"] = 100   # safe — modifying the copy, not the original
```

---

## 2.24 .loc[] vs .iloc[]

| | What it does | Example |
|--|--|--|
| `.loc[]` | Select by **label** (column name or index label) | `df.loc[df["x"] > 5, "y"]` |
| `.iloc[]` | Select by **position** (integer number) | `df.iloc[0:5, 1:3]` |

```python
# Set values in specific rows using .loc:
df.loc[df["revenue"].isna(), "revenue"] = df["unit_price"] * df["quantity"]
# "For rows where revenue is NaN, set revenue to unit_price * quantity"
```

---

## 2.25 pct_change() — Month-over-Month Growth

```python
monthly["revenue_mom_pct"] = monthly["total_revenue"].pct_change() * 100
# Calculates % change from previous row
# January: NaN (no previous month)
# February: ((Feb - Jan) / Jan) * 100
```

---

## 2.26 rank()

Rank values within a column:
```python
products["revenue_rank"] = products["total_revenue"].rank(ascending=False).astype(int)
# ascending=False means rank 1 = highest value
```

---

## 2.27 pivot_table()

Like groupby but in a 2D grid format — like Excel pivot tables.

```python
pivot = df.pivot_table(
    values="revenue",       # what to aggregate
    index="region",         # rows
    columns="category",     # columns
    aggfunc="sum"           # how to aggregate
)
```

Result — a table where rows = regions, columns = categories, values = sum of revenue.
This is what the heatmap in our project uses.

---

## 2.28 What You Now Know

You now understand every Pandas and NumPy operation used in this project:
- Creating and reading DataFrames
- Selecting rows and columns
- Filtering with boolean masks
- Adding new columns
- Handling nulls (isna, fillna, dropna)
- String operations (.str accessor)
- Date operations (.dt accessor)
- groupby + agg (the pivot table of Python)
- sort_values, nlargest, nsmallest
- apply() for custom functions
- to_csv, copy, loc, iloc, pct_change, rank, pivot_table

**Next:** Chapter 3 — Data Cleaning Concepts (the theory behind what we did).
