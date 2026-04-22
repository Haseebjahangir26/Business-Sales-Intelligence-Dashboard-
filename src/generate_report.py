"""
generate_report.py
──────────────────
Produces a self-contained HTML executive report from the cleaned data.
No external dependencies beyond pandas, matplotlib, and base64.
Run after clean_and_engineer.py and eda_and_charts.py.

Output: reports/sales_intelligence_report.html
"""

import base64, os
import pandas as pd

# ── Load summaries ─────────────────────────────────────────────────────────────
monthly  = pd.read_csv("data/processed/monthly_summary.csv").sort_values("month_num")
products = pd.read_csv("data/processed/product_summary.csv")
customers= pd.read_csv("data/processed/customer_summary.csv")
impact   = pd.read_csv("data/processed/sku_removal_impact.csv")

top10_prod = products.nlargest(10, "total_revenue")[
    ["sku","category","total_revenue","total_profit","profit_margin_pct","units_sold"]
]
top10_cust = customers.nlargest(10, "total_revenue")[
    ["customer_name","total_revenue","total_profit","profit_margin_pct","order_count"]
]

# ── KPIs ───────────────────────────────────────────────────────────────────────
total_rev    = monthly["total_revenue"].sum()
total_profit = monthly["total_profit"].sum()
avg_margin   = total_profit / total_rev * 100
total_orders = monthly["total_orders"].sum()
best_month   = monthly.loc[monthly["total_revenue"].idxmax(), "month_year"]

impact_row = impact.set_index("metric")["value"]
margin_new = impact_row["Profit Margin% (without SKU-098, SKU-099)"]
margin_old = impact_row["Profit Margin% (with SKU-098, SKU-099)"]
delta      = impact_row["Margin Improvement (pp)"]


def img_tag(path: str, alt: str, width: str = "100%") -> str:
    if not os.path.exists(path):
        return f"<p style='color:#FF4D6D'>[Chart not found: {path}]</p>"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f'<img src="data:image/png;base64,{b64}" alt="{alt}" style="width:{width};border-radius:10px;"/>'


def df_to_html(df: pd.DataFrame) -> str:
    def fmt(v):
        if isinstance(v, float):
            if abs(v) > 1000:
                return f"${v:,.2f}"
            return f"{v:.2f}"
        return str(v)
    rows_html = ""
    for _, row in df.iterrows():
        cells = "".join(f"<td>{fmt(v)}</td>" for v in row)
        rows_html += f"<tr>{cells}</tr>"
    headers = "".join(f"<th>{c.replace('_',' ').title()}</th>" for c in df.columns)
    return f"<table><thead><tr>{headers}</tr></thead><tbody>{rows_html}</tbody></table>"


HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Business Sales Intelligence Report 2023</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:#0F1117;color:#C8CDD8;font-family:'Inter',sans-serif;line-height:1.6}}
  header{{background:linear-gradient(135deg,#1A1D26 0%,#141720 100%);
          border-bottom:2px solid #6C63FF;padding:40px 60px}}
  header h1{{font-size:2rem;font-weight:800;color:#fff;letter-spacing:-0.5px}}
  header p{{color:#8B90A0;margin-top:6px}}
  .kpi-row{{display:flex;gap:20px;padding:40px 60px 0;flex-wrap:wrap}}
  .kpi{{background:#1A1D26;border:1px solid #2E3140;border-radius:12px;
        flex:1;min-width:160px;padding:24px;text-align:center}}
  .kpi .val{{font-size:1.8rem;font-weight:700;color:#6C63FF}}
  .kpi .lbl{{font-size:0.78rem;color:#8B90A0;margin-top:4px;text-transform:uppercase;letter-spacing:0.8px}}
  .section{{padding:40px 60px}}
  .section h2{{font-size:1.2rem;font-weight:700;color:#fff;margin-bottom:20px;
               border-left:4px solid #6C63FF;padding-left:12px}}
  .chart-grid{{display:grid;gap:24px}}
  .chart-grid.two{{grid-template-columns:1fr 1fr}}
  .chart-box{{background:#1A1D26;border:1px solid #2E3140;border-radius:12px;padding:20px}}
  table{{width:100%;border-collapse:collapse;font-size:0.85rem}}
  th{{background:#141720;color:#6C63FF;padding:10px 12px;text-align:left;
      border-bottom:1px solid #2E3140;font-weight:600}}
  td{{padding:9px 12px;border-bottom:1px solid #1E2130}}
  tr:hover td{{background:#1E2130}}
  .insight-box{{background:linear-gradient(135deg,#1E1A3A,#1A2A1E);
               border:1px solid #6C63FF;border-radius:14px;padding:28px;
               margin-top:12px}}
  .insight-box h3{{color:#6C63FF;margin-bottom:10px;font-size:1rem}}
  .insight-box .big{{font-size:3rem;font-weight:800;color:#00D4AA}}
  .insight-box p{{color:#C8CDD8;margin-top:8px;font-size:0.92rem}}
  footer{{padding:30px 60px;color:#4A5060;font-size:0.8rem;border-top:1px solid #1E2130}}
  @media(max-width:768px){{
    header,section,.kpi-row{{padding:20px}}
    .chart-grid.two{{grid-template-columns:1fr}}
  }}
</style>
</head>
<body>

<header>
  <h1>📊 Business Sales Intelligence Report</h1>
  <p>Fiscal Year 2023 &nbsp;|&nbsp; Python + Pandas Pipeline &nbsp;|&nbsp; Decision-Ready Analysis</p>
</header>

<!-- KPI Cards -->
<div class="kpi-row">
  <div class="kpi"><div class="val">${total_rev:,.0f}</div><div class="lbl">Total Revenue</div></div>
  <div class="kpi"><div class="val">${total_profit:,.0f}</div><div class="lbl">Total Profit</div></div>
  <div class="kpi"><div class="val">{avg_margin:.1f}%</div><div class="lbl">Avg Profit Margin</div></div>
  <div class="kpi"><div class="val">{total_orders:,}</div><div class="lbl">Total Orders</div></div>
  <div class="kpi"><div class="val">{best_month}</div><div class="lbl">Best Month</div></div>
</div>

<!-- KEY INSIGHT -->
<div class="section">
  <h2>🔑 Key Insight: SKU Rationalisation</h2>
  <div class="insight-box">
    <h3>Removing SKU-098 &amp; SKU-099 (bottom 2 underperformers)</h3>
    <div class="big">+{delta:.1f} pp</div>
    <p>Overall profit margin improves from <strong>{margin_old:.1f}%</strong> to <strong>{margin_new:.1f}%</strong>
       — a <strong>{delta:.1f} percentage-point</strong> uplift — with no additional investment required.
       These two SKUs generate {impact_row["Bad-SKU Revenue Share (%)"]:.1f}% of revenue
       but drag the portfolio margin down significantly due to cost ratios above 90%.</p>
  </div>
</div>

<!-- Revenue Trend -->
<div class="section">
  <h2>📈 Monthly Revenue &amp; Margin Trends</h2>
  <div class="chart-grid">
    <div class="chart-box">{img_tag("reports/figures/01_monthly_revenue_trend.png","Monthly Revenue")}</div>
    <div class="chart-box">{img_tag("reports/figures/02_monthly_profit_margin.png","Monthly Margin")}</div>
  </div>
</div>

<!-- Products -->
<div class="section">
  <h2>🏆 Top-10 Products</h2>
  <div class="chart-grid two">
    <div class="chart-box">{img_tag("reports/figures/03_top10_products_revenue.png","Top Products Revenue")}</div>
    <div class="chart-box">{img_tag("reports/figures/04_top10_products_margin.png","Top Products Margin")}</div>
  </div>
  <div class="chart-box" style="margin-top:24px;overflow-x:auto">
    {df_to_html(top10_prod)}
  </div>
</div>

<!-- Customers -->
<div class="section">
  <h2>👥 Top-10 Customers</h2>
  <div class="chart-box" style="margin-bottom:24px">{img_tag("reports/figures/05_top10_customers_revenue.png","Top Customers")}</div>
  <div class="chart-box" style="overflow-x:auto">{df_to_html(top10_cust)}</div>
</div>

<!-- Category & Region -->
<div class="section">
  <h2>🗂️ Category &amp; Regional Analysis</h2>
  <div class="chart-grid two">
    <div class="chart-box">{img_tag("reports/figures/06_category_revenue_pie.png","Category Pie")}</div>
    <div class="chart-box">{img_tag("reports/figures/08_region_heatmap.png","Region Heatmap")}</div>
  </div>
</div>

<!-- Waterfall -->
<div class="section">
  <h2>⚠️ SKU Removal Impact</h2>
  <div class="chart-box">{img_tag("reports/figures/07_sku_removal_waterfall.png","SKU Waterfall","60%")}</div>
  <div class="chart-box" style="margin-top:20px;overflow-x:auto">{df_to_html(impact)}</div>
</div>

<footer>
  Generated by Business Sales Intelligence Pipeline &nbsp;|&nbsp;
  Python · Pandas · Matplotlib · Seaborn &nbsp;|&nbsp; 2023 Fiscal Year Data
</footer>
</body>
</html>"""

os.makedirs("reports", exist_ok=True)
with open("reports/sales_intelligence_report.html", "w", encoding="utf-8") as fh:
    fh.write(HTML)

print("✅  Report saved → reports/sales_intelligence_report.html")
