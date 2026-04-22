# Power BI Dashboard Setup Guide

## Prerequisites
- Power BI Desktop (free download: https://powerbi.microsoft.com/desktop)
- Processed CSVs from the Python pipeline (`python run_pipeline.py`)

---

## Step 1 — Import Data Sources

Open Power BI Desktop → **Get Data → Text/CSV**

Import all four files from `data/processed/`:
| File | Purpose |
|------|---------|
| `clean_sales_data.csv` | Transaction-level fact table |
| `monthly_summary.csv` | Pre-aggregated monthly KPIs |
| `product_summary.csv` | Per-SKU aggregated KPIs |
| `customer_summary.csv` | Per-customer aggregated KPIs |
| `sku_removal_impact.csv` | What-if scenario data |

---

## Step 2 — Data Model

In **Model View**, create these relationships:

```
clean_sales_data[sku]           →  product_summary[sku]
clean_sales_data[customer_name] →  customer_summary[customer_name]
clean_sales_data[month_year]    →  monthly_summary[month_year]
```

Set all relationships as **Many-to-One**, **Single direction**.

---

## Step 3 — DAX Measures

In any table, create these measures:

```dax
Total Revenue =
    SUM(clean_sales_data[revenue])

Total Profit =
    SUM(clean_sales_data[profit])

Profit Margin % =
    DIVIDE([Total Profit], [Total Revenue], 0) * 100

Avg Order Value =
    AVERAGEX(
        VALUES(clean_sales_data[order_id]),
        CALCULATE(SUM(clean_sales_data[revenue]))
    )

Revenue Excl Bad SKUs =
    CALCULATE(
        [Total Revenue],
        NOT clean_sales_data[sku] IN {"SKU-098","SKU-099"}
    )

Margin Excl Bad SKUs =
    DIVIDE(
        CALCULATE([Total Profit], NOT clean_sales_data[sku] IN {"SKU-098","SKU-099"}),
        [Revenue Excl Bad SKUs],
        0
    ) * 100
```

---

## Step 4 — Dashboard Pages

### Page 1: Executive Summary
| Visual | Data |
|--------|------|
| KPI Card | Total Revenue |
| KPI Card | Total Profit |
| KPI Card | Profit Margin % |
| KPI Card | Total Orders (COUNT order_id) |
| Line Chart | monthly_summary → month_year (X), total_revenue (Y) |
| Clustered Bar | monthly_summary → month_year (X), profit_margin_pct (Y) |

### Page 2: Product Performance
| Visual | Data |
|--------|------|
| Bar Chart | product_summary → top 10 by total_revenue |
| Bar Chart | product_summary → top 10 by profit_margin_pct |
| Table | product_summary all columns, conditional formatting on profit_margin_pct |
| Slicer | category |

### Page 3: Customer Rankings
| Visual | Data |
|--------|------|
| Bar Chart | customer_summary → top 10 by total_revenue |
| Table | customer_summary with conditional formatting |
| Map / Filled Map | clean_sales_data → region, revenue |
| Treemap | clean_sales_data → category (group), revenue (size) |

### Page 4: SKU Rationalization
| Visual | Data |
|--------|------|
| KPI Card | Profit Margin % (current) |
| KPI Card | Margin Excl Bad SKUs |
| Waterfall Chart | sku_removal_impact.csv → metric, value |
| Table | sku_removal_impact.csv |

---

## Step 5 — Theme & Formatting

1. **View → Themes → Browse for themes** or apply custom JSON
2. Recommended dark theme colors:
   - Background: `#0F1117`
   - Card background: `#1A1D26`
   - Accent: `#6C63FF`
   - Positive: `#00D4AA`
   - Negative: `#FF4D6D`
3. Font: **Segoe UI** (Power BI default, matches design intent)

---

## Step 6 — Publish & Share

1. **File → Publish → Publish to Power BI** (requires Power BI account)
2. Or **File → Export → Export to PDF** for offline sharing
3. Screenshots recommended: capture each page at **1920×1080**

---

## Quick Tip: Conditional Formatting

In any table visual → select a column → Format → Conditional Formatting:
- **profit_margin_pct**: Color scale Red (0%) → Green (50%+)
- **total_revenue**: Data bars
