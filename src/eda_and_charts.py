"""
eda_and_charts.py
─────────────────
Generates all charts used in the dashboard documentation and README.
Saves PNGs to reports/figures/.

Charts produced:
  01_monthly_revenue_trend.png
  02_monthly_profit_margin.png
  03_top10_products_revenue.png
  04_top10_products_margin.png
  05_top10_customers_revenue.png
  06_category_revenue_pie.png
  07_sku_removal_waterfall.png
  08_region_heatmap.png
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import seaborn as sns

# ── Style ──────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "#0F1117",
    "axes.facecolor":    "#1A1D26",
    "axes.edgecolor":    "#2E3140",
    "axes.labelcolor":   "#C8CDD8",
    "axes.titlecolor":   "#FFFFFF",
    "xtick.color":       "#8B90A0",
    "ytick.color":       "#8B90A0",
    "text.color":        "#C8CDD8",
    "grid.color":        "#2E3140",
    "grid.linestyle":    "--",
    "grid.linewidth":    0.6,
    "font.family":       "DejaVu Sans",
    "font.size":         10,
    "axes.titlesize":    13,
    "axes.titleweight":  "bold",
    "figure.dpi":        130,
})

ACCENT   = "#6C63FF"
ACCENT2  = "#00D4AA"
DANGER   = "#FF4D6D"
GOLD     = "#FFB347"
PALETTE  = [ACCENT, ACCENT2, GOLD, "#FF6B9D", "#45B7D1", "#96CEB4",
            "#FFEAA7", "#DDA0DD", "#98FB98", "#F0E68C"]

# ── Load data ──────────────────────────────────────────────────────────────────
monthly  = pd.read_csv("data/processed/monthly_summary.csv").sort_values("month_num")
products = pd.read_csv("data/processed/product_summary.csv")
customers= pd.read_csv("data/processed/customer_summary.csv")
clean    = pd.read_csv("data/processed/clean_sales_data.csv")

FIGDIR = "reports/figures"
import os; os.makedirs(FIGDIR, exist_ok=True)

def save(name: str):
    plt.tight_layout()
    plt.savefig(f"{FIGDIR}/{name}", bbox_inches="tight")
    plt.close()
    print(f"  ✓  {name}")

print("Generating charts …")

# ── 01 Monthly Revenue Trend ──────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 4.5))
x = range(len(monthly))
ax.fill_between(x, monthly["total_revenue"], alpha=0.15, color=ACCENT)
ax.plot(x, monthly["total_revenue"], color=ACCENT, lw=2.5, marker="o", ms=5)
ax.set_xticks(x)
ax.set_xticklabels(monthly["month_year"], rotation=45, ha="right", fontsize=8)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v,_: f"${v:,.0f}"))
ax.set_title("Monthly Revenue Trend  (2023)")
ax.set_ylabel("Revenue (USD)")
ax.grid(axis="y")
save("01_monthly_revenue_trend.png")

# ── 02 Monthly Profit Margin ──────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 4))
bars = ax.bar(x, monthly["profit_margin_pct"], color=[
    ACCENT2 if v >= monthly["profit_margin_pct"].median() else DANGER
    for v in monthly["profit_margin_pct"]
], alpha=0.85, width=0.6)
ax.axhline(monthly["profit_margin_pct"].median(), color=GOLD, lw=1.5, ls="--", label="Median")
ax.set_xticks(x)
ax.set_xticklabels(monthly["month_year"], rotation=45, ha="right", fontsize=8)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.set_title("Monthly Profit Margin %  (2023)")
ax.set_ylabel("Margin %")
ax.legend(facecolor="#1A1D26")
for bar, val in zip(bars, monthly["profit_margin_pct"]):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.2,
            f"{val:.1f}%", ha="center", va="bottom", fontsize=7.5, color="#C8CDD8")
save("02_monthly_profit_margin.png")

# ── 03 Top-10 Products by Revenue ─────────────────────────────────────────────
top10_rev = products.nlargest(10, "total_revenue")
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(top10_rev["sku"], top10_rev["total_revenue"],
               color=PALETTE[:10], alpha=0.88)
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v,_: f"${v:,.0f}"))
ax.set_title("Top 10 Products by Total Revenue")
ax.invert_yaxis()
for bar, val in zip(bars, top10_rev["total_revenue"]):
    ax.text(val + 500, bar.get_y()+bar.get_height()/2,
            f"${val:,.0f}", va="center", fontsize=8)
save("03_top10_products_revenue.png")

# ── 04 Top-10 Products by Profit Margin ───────────────────────────────────────
top10_mg = products[~products["sku"].isin(["SKU-098","SKU-099"])].nlargest(10, "profit_margin_pct")
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(top10_mg["sku"], top10_mg["profit_margin_pct"], color=ACCENT2, alpha=0.85)
ax.xaxis.set_major_formatter(mtick.PercentFormatter())
ax.set_title("Top 10 Products by Profit Margin %  (excl. bad SKUs)")
ax.invert_yaxis()
save("04_top10_products_margin.png")

# ── 05 Top-10 Customers by Revenue ────────────────────────────────────────────
top10_cust = customers.nlargest(10, "total_revenue")
fig, ax = plt.subplots(figsize=(11, 5))
ax.bar(range(len(top10_cust)), top10_cust["total_revenue"], color=PALETTE[:10], alpha=0.88)
ax.set_xticks(range(len(top10_cust)))
ax.set_xticklabels(top10_cust["customer_name"], rotation=35, ha="right", fontsize=8)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v,_: f"${v:,.0f}"))
ax.set_title("Top 10 Customers by Total Revenue")
save("05_top10_customers_revenue.png")

# ── 06 Category Revenue Pie ───────────────────────────────────────────────────
cat_rev = clean.groupby("category")["revenue"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(7, 7))
wedges, texts, autotexts = ax.pie(
    cat_rev,
    labels=cat_rev.index,
    autopct="%1.1f%%",
    colors=PALETTE[:len(cat_rev)],
    startangle=140,
    pctdistance=0.82,
    wedgeprops=dict(linewidth=2, edgecolor="#0F1117"),
)
for t in autotexts:
    t.set_color("white"); t.set_fontsize(9)
ax.set_title("Revenue by Category")
save("06_category_revenue_pie.png")

# ── 07 SKU-Removal Waterfall ──────────────────────────────────────────────────
impact = pd.read_csv("data/processed/sku_removal_impact.csv").set_index("metric")["value"]
margin_with    = impact["Profit Margin% (with SKU-098, SKU-099)"]
margin_without = impact["Profit Margin% (without SKU-098, SKU-099)"]
delta          = impact["Margin Improvement (pp)"]

fig, ax = plt.subplots(figsize=(7, 4))
bars_data = [margin_with, delta, margin_without]
labels    = ["Current Margin", f"+{delta:.1f}pp\n(Remove SKU-098/099)", "New Margin"]
colors    = [ACCENT, ACCENT2, GOLD]
bottoms   = [0, margin_with, 0]

for i, (label, val, bottom, col) in enumerate(zip(labels, bars_data, bottoms, colors)):
    ax.bar(i, val, bottom=bottom, color=col, alpha=0.85, width=0.5)
    ax.text(i, bottom + val/2, f"{bottom+val:.1f}%", ha="center", va="center",
            fontweight="bold", color="white", fontsize=11)

ax.set_xticks([0,1,2])
ax.set_xticklabels(labels)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.set_title("Profit Margin Impact: Removing Bottom 2 SKUs")
ax.set_ylim(0, margin_without * 1.25)
save("07_sku_removal_waterfall.png")

# ── 08 Region × Category Revenue Heatmap ─────────────────────────────────────
pivot = clean.pivot_table(values="revenue", index="region",
                          columns="category", aggfunc="sum")
fig, ax = plt.subplots(figsize=(10, 4.5))
cmap = sns.color_palette("mako", as_cmap=True)
sns.heatmap(pivot, ax=ax, cmap=cmap, fmt=",.0f", annot=True,
            linewidths=0.5, linecolor="#0F1117",
            cbar_kws={"label": "Revenue (USD)"})
ax.set_title("Revenue Heatmap: Region × Category")
ax.set_xlabel("")
ax.set_ylabel("")
save("08_region_heatmap.png")

print("\n✅  All charts saved to reports/figures/")
