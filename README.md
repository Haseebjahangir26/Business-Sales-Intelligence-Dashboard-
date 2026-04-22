# 📊 Business Sales Intelligence Dashboard

> **Tools:** Python · Pandas · Matplotlib · Seaborn · Power BI  
> **Dataset:** 10,000+ row synthetic sales dataset with intentional data quality issues

---

## 🎯 Project Overview

Raw sales data had inconsistent formats, duplicates, and missing revenue fields with no clear way to identify which products were actually profitable.

### What This Project Does

| Stage | Description |
|-------|-------------|
| **Data Generation** | 10,500+ row synthetic dataset with baked-in quality issues |
| **Data Cleaning** | Deduplication, date normalization, null imputation, invalid-row removal |
| **Feature Engineering** | Monthly revenue, profit margin %, revenue bands |
| **Analysis** | Monthly trends, top-10 products, top-10 customers, regional breakdowns |
| **Key Insight** | Identified 2 underperforming SKUs → removing them lifts overall profit margin by **~12 pp** |
| **Reporting** | Self-contained HTML executive report + 8 publication-ready charts |

---

## 📁 Project Structure

```
Business Sales Intelligence Dashboard/
├── data/
│   ├── raw/
│   │   └── generate_raw_data.py    # Generates raw_sales_data.csv
│   └── processed/
│       ├── clean_sales_data.csv
│       ├── monthly_summary.csv
│       ├── product_summary.csv
│       ├── customer_summary.csv
│       └── sku_removal_impact.csv
├── src/
│   ├── clean_and_engineer.py       # Stage 1 & 2: Clean + Feature Eng.
│   ├── eda_and_charts.py           # Stage 3: 8 publication-ready charts
│   └── generate_report.py          # Stage 4: HTML executive report
├── notebooks/
│   └── sales_analysis.ipynb        # Full walkthrough notebook
├── reports/
│   ├── figures/                    # 8 chart PNGs
│   └── sales_intelligence_report.html
├── powerbi/
│   └── POWERBI_SETUP.md            # Step-by-step Power BI guide
├── run_pipeline.py                 # 🚀 Master runner
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd "Business Sales Intelligence Dashboard"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the full pipeline
python run_pipeline.py
```

The pipeline will:
1. Generate `data/raw/raw_sales_data.csv` (10,500+ messy rows)
2. Clean and engineer features → `data/processed/`
3. Generate 8 charts → `reports/figures/`
4. Write HTML report → `reports/sales_intelligence_report.html`

---

## 🔍 Data Quality Issues Handled

| Issue | Count | Treatment |
|-------|-------|-----------|
| Exact duplicate rows | ~315 | Dropped |
| Inconsistent date formats | 4 formats | Parsed & normalized to `YYYY-MM-DD` |
| Mixed category casing | ~30% rows | `.str.title()` normalization |
| Negative quantities | ~105 rows | Dropped (invalid returns) |
| Missing revenue | ~525 cells | Imputed: `unit_price × quantity` |
| Missing cost | ~420 cells | Imputed: category median cost-% |
| Null customer names | ~210 cells | Filled with `"Unknown Customer"` |

---

## 💡 Key Insight

> **Removing SKU-098 and SKU-099 improves overall profit margin by ~12 percentage points.**

These two SKUs have cost ratios between **88–97%** (near-zero or negative margin) while the healthy portfolio runs at **35–50%** cost ratio. They represent only ~3.7% of revenue but disproportionately drag down portfolio profitability.

**Recommendation:** Discontinue both SKUs or renegotiate supplier costs before the next quarter.

---

## 📊 Power BI Dashboard

See [`powerbi/POWERBI_SETUP.md`](powerbi/POWERBI_SETUP.md) for step-by-step instructions to build the Power BI dashboard using the processed CSVs.

**Dashboard pages:**
1. **Executive Summary** — Revenue, Profit, Margin KPI cards + monthly trend
2. **Product Performance** — Top-10 by revenue & margin, SKU deep-dive
3. **Customer Rankings** — Top-10 customers, regional breakdown
4. **SKU Rationalization** — What-if analysis for removing bottom SKUs

---

## 📈 Charts Generated

| # | Chart |
|---|-------|
| 01 | Monthly Revenue Trend (2023) |
| 02 | Monthly Profit Margin % |
| 03 | Top-10 Products by Revenue |
| 04 | Top-10 Products by Profit Margin |
| 05 | Top-10 Customers by Revenue |
| 06 | Revenue by Category (Pie) |
| 07 | SKU Removal Waterfall (Key Insight) |
| 08 | Revenue Heatmap: Region × Category |

---

## 🛠 Tech Stack

- **Python 3.12** — core language
- **Pandas** — data wrangling & aggregation  
- **NumPy** — numerical operations  
- **Matplotlib + Seaborn** — data visualization  
- **Faker** — realistic synthetic data generation  
- **Power BI Desktop** — interactive dashboard

---

## 📄 License

MIT — free to use for portfolio and educational purposes.
