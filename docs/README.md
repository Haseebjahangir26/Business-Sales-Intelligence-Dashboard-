# 📚 Complete Study Guide — Business Sales Intelligence Dashboard
## From Absolute Zero to Job-Ready

This guide teaches you every concept used in this project, from scratch.
Read the chapters in order. Each one builds on the previous.

---

## How to Use This Guide

1. **Read actively** — open the project files in VS Code at the same time
2. **Run the code** — every example here, type it yourself and run it
3. **Relate back** — after each section, find where that concept appears in the project
4. **Don't rush** — one chapter per day is plenty

---

## Chapters

| # | File | Topics Covered |
|---|------|---------------|
| 1 | [STUDY_GUIDE_01_Python_Basics.md](STUDY_GUIDE_01_Python_Basics.md) | Variables, data types, strings, lists, dicts, loops, functions, try/except, imports, f-strings, list comprehensions |
| 2 | [STUDY_GUIDE_02_NumPy_Pandas.md](STUDY_GUIDE_02_NumPy_Pandas.md) | NumPy arrays, Pandas DataFrames, reading CSVs, filtering, groupby, agg, dates, strings, merge, pivot tables |
| 3 | [STUDY_GUIDE_03_Data_Cleaning_Feature_Engineering.md](STUDY_GUIDE_03_Data_Cleaning_Feature_Engineering.md) | Cleaning workflow, missing data, imputation, date parsing, normalization, outliers, feature engineering, EDA, what-if analysis |
| 4 | [STUDY_GUIDE_04_Matplotlib_Seaborn.md](STUDY_GUIDE_04_Matplotlib_Seaborn.md) | Figure/axes model, bar charts, line charts, pie charts, waterfall charts, heatmaps, styling, annotations, saving |
| 5 | [STUDY_GUIDE_05_Statistics_Git_PowerBI_Career.md](STUDY_GUIDE_05_Statistics_Git_PowerBI_Career.md) | Statistics (mean, median, percentiles, correlation), Git & GitHub, Power BI & DAX, virtual environments, Jupyter, career roadmap |

---

## Quick Lookup — Where Each Concept Appears in the Project

| Concept | Chapter | Project File |
|---------|---------|-------------|
| Variables, loops, functions | 1 | All `.py` files |
| List comprehensions | 1 | `generate_raw_data.py` line ~25 |
| Try/except | 1 | `clean_and_engineer.py` — date parser |
| F-strings | 1 | `run_pipeline.py` — print statements |
| NumPy random + seed | 2 | `generate_raw_data.py` top |
| pd.read_csv | 2 | `clean_and_engineer.py` |
| Boolean filtering | 2 | `clean_and_engineer.py` — neg qty removal |
| .str accessor | 2 | `clean_and_engineer.py` — category normalization |
| .dt accessor | 2 | `clean_and_engineer.py` — date features |
| groupby + agg | 2 | `clean_and_engineer.py` — monthly summary |
| pivot_table | 2 | `eda_and_charts.py` — heatmap data |
| Data cleaning order | 3 | `clean_and_engineer.py` — stages 1–4 |
| Median imputation | 3 | `clean_and_engineer.py` — cost imputation |
| Date parsing | 3 | `clean_and_engineer.py` — `parse_date()` |
| Feature engineering | 3 | `clean_and_engineer.py` — profit, margin, bands |
| What-if analysis | 3 | `clean_and_engineer.py` — SKU removal section |
| Dark theme + color palette | 4 | `eda_and_charts.py` — top constants |
| Bar charts | 4 | `eda_and_charts.py` — charts 01, 02 |
| Horizontal bar charts | 4 | `eda_and_charts.py` — charts 03, 04, 05 |
| Pie chart | 4 | `eda_and_charts.py` — chart 06 |
| Waterfall chart | 4 | `eda_and_charts.py` — chart 07 |
| Seaborn heatmap | 4 | `eda_and_charts.py` — chart 08 |
| Number formatters | 4 | `eda_and_charts.py` — mticker.FuncFormatter |
| Profit margin math | 5 | `clean_and_engineer.py` |
| Cost ratio | 5 | `generate_raw_data.py` — BAD_SKUS config |
| Median vs mean | 5 | `clean_and_engineer.py` — cost imputation |
| Git add/commit/push | 5 | Terminal commands (repo history) |
| .gitignore | 5 | `.gitignore` file |
| DAX measures | 5 | `powerbi/POWERBI_SETUP.md` |
| Virtual environment | 5 | `requirements.txt` |
| Jupyter notebook | 5 | `notebooks/sales_analysis.ipynb` |

---

## The Big Picture — What You Built

```
[Problem]
Raw sales data: 10,815 rows, 4 date formats, missing values,
duplicates, bad SKUs, no profit columns

         ↓ Python Pipeline (run_pipeline.py)

[Stage 1] Generate dirty data    (generate_raw_data.py)
[Stage 2] Clean + engineer       (clean_and_engineer.py)
[Stage 3] Visualize              (eda_and_charts.py)
[Stage 4] Report                 (generate_report.py)

         ↓ Output

✓  10,392 clean rows saved to CSV
✓  8 publication-ready chart PNGs
✓  1 self-contained HTML executive report
✓  Power BI dashboard instructions + DAX

[Insight]
SKU-098 and SKU-099 have 94–99% cost ratios.
Removing them improves portfolio profit margin.
Recommendation: Discontinue or renegotiate before next quarter.
```

---

*Built with Python 3.12 | Pandas | Matplotlib | Seaborn | Power BI*
