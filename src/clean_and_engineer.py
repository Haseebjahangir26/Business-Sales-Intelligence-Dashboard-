"""
clean_and_engineer.py
─────────────────────
Stage 1 – Data Cleaning
  1. Drop exact duplicates
  2. Standardize sale_date to YYYY-MM-DD
  3. Normalize category casing
  4. Drop rows with invalid (negative) quantities
  5. Impute missing revenue   = unit_price × quantity
  6. Impute missing cost      = median cost-pct per category × revenue
  7. Impute missing customer  = "Unknown Customer"

Stage 2 – Feature Engineering
  • month_year      → "2023-01" string (for Power BI time axis)
  • month_num       → integer 1-12 (for sorting)
  • profit          → revenue - cost
  • profit_margin_pct → profit / revenue × 100
  • revenue_band    → Low / Medium / High (quartile-based)

Outputs
  data/processed/clean_sales_data.csv   ← full cleaned dataset
  data/processed/monthly_summary.csv   ← monthly aggregated KPIs
  data/processed/product_summary.csv   ← per-SKU aggregated KPIs
  data/processed/customer_summary.csv  ← per-customer aggregated KPIs
  data/processed/sku_removal_impact.csv← what-if: drop bottom 2 SKUs
"""

import re
import numpy as np
import pandas as pd

# ── 0. Load raw data ───────────────────────────────────────────────────────────
df = pd.read_csv("raw_sales_data.csv")
raw_count = len(df)
print(f"Raw rows loaded : {raw_count:,}")
print("=" * 55)

# ── 1. Drop exact duplicates ───────────────────────────────────────────────────
df.drop_duplicates(inplace=True)
print(f"[1] Dropped duplicates  → {raw_count - len(df):,} removed  |  {len(df):,} remain")

# ── 2. Standardise sale_date ───────────────────────────────────────────────────
def parse_date(val):
    """Try multiple common formats; return NaT if all fail."""
    if pd.isna(val):
        return pd.NaT
    for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%d-%b-%Y", "%d/%m/%Y"):
        try:
            return pd.to_datetime(val, format=fmt)
        except (ValueError, TypeError):
            pass
    return pd.to_datetime(val, errors="coerce")

df["sale_date"] = df["sale_date"].apply(parse_date)
null_dates = df["sale_date"].isna().sum()
df.dropna(subset=["sale_date"], inplace=True)
print(f"[2] Parsed dates        → {null_dates} unparseable rows dropped  |  {len(df):,} remain")

# ── 3. Normalise category casing ──────────────────────────────────────────────
df["category"] = df["category"].str.strip().str.title()
print(f"[3] Normalised category → unique values: {sorted(df['category'].unique())}")

# ── 4. Drop invalid quantities ────────────────────────────────────────────────
neg_mask = df["quantity"] < 0
print(f"[4] Negative qty rows   → {neg_mask.sum()} removed")
df = df[~neg_mask].copy()

# ── 5. Impute missing revenue ─────────────────────────────────────────────────
missing_rev = df["revenue"].isna().sum()
df.loc[df["revenue"].isna(), "revenue"] = (
    df["unit_price"] * df["quantity"]
)
print(f"[5] Imputed revenue     → {missing_rev} cells filled (unit_price × quantity)")

# ── 6. Impute missing cost ────────────────────────────────────────────────────
# Compute median cost-pct per category from known rows
df["_cost_pct"] = df["cost"] / df["revenue"]
cat_median_pct = df.groupby("category")["_cost_pct"].median()
missing_cost = df["cost"].isna().sum()
for cat, pct in cat_median_pct.items():
    mask = df["cost"].isna() & (df["category"] == cat)
    df.loc[mask, "cost"] = df.loc[mask, "revenue"] * pct
# Fallback for any still-null
global_pct = df["_cost_pct"].median()
still_null = df["cost"].isna().sum()
df["cost"] = df["cost"].fillna(df["revenue"] * global_pct)
df.drop(columns=["_cost_pct"], inplace=True)
print(f"[6] Imputed cost        → {missing_cost} cells filled (category median cost-pct)")

# ── 7. Impute missing customer names ──────────────────────────────────────────
missing_cust = df["customer_name"].isna().sum()
df["customer_name"] = df["customer_name"].fillna("Unknown Customer")
print(f"[7] Imputed customers   → {missing_cust} cells filled with 'Unknown Customer'")

# ── 8. Feature engineering ────────────────────────────────────────────────────
df["sale_date"]        = pd.to_datetime(df["sale_date"])
df["month_year"]       = df["sale_date"].dt.to_period("M").astype(str)   # "2023-01"
df["month_num"]        = df["sale_date"].dt.month
df["profit"]           = (df["revenue"] - df["cost"]).round(2)
df["profit_margin_pct"]= ((df["profit"] / df["revenue"]) * 100).round(2)

rev_q1 = df["revenue"].quantile(0.33)
rev_q2 = df["revenue"].quantile(0.66)

def rev_band(r):
    if r <= rev_q1:   return "Low"
    elif r <= rev_q2: return "Medium"
    return "High"

df["revenue_band"] = df["revenue"].apply(rev_band)
df["sale_date"]    = df["sale_date"].dt.strftime("%Y-%m-%d")   # back to string for CSV

print(f"\n[8] Feature engineering complete")
print(f"    profit range       : {df['profit'].min():,.2f}  →  {df['profit'].max():,.2f}")
print(f"    margin range       : {df['profit_margin_pct'].min():.1f}%  →  {df['profit_margin_pct'].max():.1f}%")
print(f"    Cleaned rows total : {len(df):,}")

# ── 9. Save cleaned master ────────────────────────────────────────────────────
df.to_csv("data/processed/clean_sales_data.csv", index=False)
print(f"\n✅  Saved clean_sales_data.csv  ({len(df):,} rows)")

# ── 10. Monthly summary ───────────────────────────────────────────────────────
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
    .reset_index()
    .sort_values("month_num")
)
monthly["profit_margin_pct"] = (
    (monthly["total_profit"] / monthly["total_revenue"]) * 100
).round(2)
monthly["revenue_mom_pct"] = monthly["total_revenue"].pct_change() * 100
monthly.to_csv("data/processed/monthly_summary.csv", index=False)
print(f"✅  Saved monthly_summary.csv   ({len(monthly)} rows)")

# ── 11. Product (SKU) summary ─────────────────────────────────────────────────
product = (
    df.groupby(["sku", "product_name", "category"])
    .agg(
        total_revenue  = ("revenue", "sum"),
        total_cost     = ("cost",    "sum"),
        total_profit   = ("profit",  "sum"),
        units_sold     = ("quantity","sum"),
        order_count    = ("order_id","count"),
    )
    .reset_index()
)
product["profit_margin_pct"] = (
    (product["total_profit"] / product["total_revenue"]) * 100
).round(2)
product["revenue_rank"]       = product["total_revenue"].rank(ascending=False).astype(int)
product["profit_rank"]        = product["total_profit"].rank(ascending=False).astype(int)
product.sort_values("total_revenue", ascending=False, inplace=True)
product.to_csv("data/processed/product_summary.csv", index=False)
print(f"✅  Saved product_summary.csv   ({len(product)} rows)")

# ── 12. Customer summary ──────────────────────────────────────────────────────
customer = (
    df.groupby("customer_name")
    .agg(
        total_revenue = ("revenue", "sum"),
        total_profit  = ("profit",  "sum"),
        order_count   = ("order_id","count"),
        regions       = ("region",  lambda x: "/".join(sorted(x.unique()))),
    )
    .reset_index()
)
customer["profit_margin_pct"] = (
    (customer["total_profit"] / customer["total_revenue"]) * 100
).round(2)
customer["revenue_rank"] = customer["total_revenue"].rank(ascending=False).astype(int)
customer.sort_values("total_revenue", ascending=False, inplace=True)
customer.to_csv("data/processed/customer_summary.csv", index=False)
print(f"✅  Saved customer_summary.csv  ({len(customer)} rows)")

# ── 13. SKU-Removal What-If Analysis ─────────────────────────────────────────
bad_skus   = ["SKU-098", "SKU-099"]
df_with    = df.copy()
df_without = df[~df["sku"].isin(bad_skus)].copy()

total_profit_with    = df_with["profit"].sum()
total_profit_without = df_without["profit"].sum()
total_rev_with       = df_with["revenue"].sum()
total_rev_without    = df_without["revenue"].sum()

margin_with    = total_profit_with / total_rev_with * 100
margin_without = total_profit_without / total_rev_without * 100
margin_delta   = margin_without - margin_with

bad_revenue_share = df[df["sku"].isin(bad_skus)]["revenue"].sum() / total_rev_with * 100
bad_profit_share  = df[df["sku"].isin(bad_skus)]["profit"].sum() / total_profit_with * 100

impact = pd.DataFrame([
    {"metric": "Total Revenue  (with SKU-098, SKU-099)",    "value": round(total_rev_with, 2)},
    {"metric": "Total Revenue  (without SKU-098, SKU-099)", "value": round(total_rev_without, 2)},
    {"metric": "Total Profit   (with SKU-098, SKU-099)",    "value": round(total_profit_with, 2)},
    {"metric": "Total Profit   (without SKU-098, SKU-099)", "value": round(total_profit_without, 2)},
    {"metric": "Profit Margin% (with SKU-098, SKU-099)",    "value": round(margin_with, 2)},
    {"metric": "Profit Margin% (without SKU-098, SKU-099)", "value": round(margin_without, 2)},
    {"metric": "Margin Improvement (pp)",                   "value": round(margin_delta, 2)},
    {"metric": "Bad-SKU Revenue Share (%)",                 "value": round(bad_revenue_share, 2)},
    {"metric": "Bad-SKU Profit  Share (%)",                 "value": round(bad_profit_share, 2)},
])
impact.to_csv("data/processed/sku_removal_impact.csv", index=False)

print(f"\n✅  Saved sku_removal_impact.csv")
print(f"\n{'='*55}")
print(f"  KEY INSIGHT:")
print(f"  Removing SKU-098 & SKU-099 improves profit margin by")
print(f"  {margin_delta:.1f} pp  ({margin_with:.1f}%  →  {margin_without:.1f}%)")
print(f"{'='*55}\n")
