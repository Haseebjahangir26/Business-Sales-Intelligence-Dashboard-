# 🎤 Project Demo & Interview Guide
## Business Sales Intelligence Dashboard

> **Who this is for:** You — before an interview, a college presentation, or a peer showcase.
> Read this once the night before. You'll know exactly what to say and click.

---

## PART 1 — THE 60-SECOND ELEVATOR PITCH

> Memorize this. Say it exactly like this when someone asks *"tell me about your project."*

---

*"I built an end-to-end data pipeline in Python. I started with a raw sales CSV — over 10,000 rows — that had real data quality problems: four different date formats in the same column, missing revenue values, duplicate rows, and inconsistent product category names like 'ELECTRONICS' and 'electronics' mixed together.*

*I wrote Python scripts using Pandas to clean all of that, engineer new features like monthly profit and profit margin percentage, and then ran an analysis. The most important finding was that two specific products — SKU-098 and SKU-099 — had a cost ratio of over 94%, meaning the company was barely breaking even on them. Removing those two SKUs from the portfolio would improve the overall profit margin.*

*I visualized everything with Matplotlib and Seaborn — 8 charts total — and packaged it into an HTML executive report that you can just open in a browser. I also documented how to replicate the dashboard in Power BI.*

*The whole pipeline runs with one command: `python run_pipeline.py`."*

---

## PART 2 — THE LIVE DEMO (Step by Step)

> Follow these steps **in order**. Each step has what to do AND what to say.

---

### STEP 0 — Before You Start (Setup, do this once)

Open your terminal / PowerShell and run these:

```bash
# Go to the project folder
cd "C:\Users\X390\Desktop\Business Sales Intelligence Dashboard"

# Activate the virtual environment (if you made one)
.venv\Scripts\activate

# Confirm everything is installed
pip install -r requirements.txt
```

✅ You should see no errors.

---

### STEP 1 — Show the GitHub Repo First (30 seconds)

**Open:** `https://github.com/Haseebjahangir26/Business-Sales-Intelligence-Dashboard-`

**Say:**
> *"This is the GitHub repository. You can see it has a proper structure — source code, data, notebooks, reports. The README renders like documentation. It has badges showing Python version, license, and status. This is what a production-style data project looks like on GitHub."*

**Point out:**
- The badges at the top
- The 4 sample chart images in the README
- The folder structure section
- The 2 commits in the history (clean, logical commits — not "update update update")

---

### STEP 2 — Show the Raw Data Problem (1 minute)

**Open** `data/raw/generate_raw_data.py` in VS Code (or just talk through it).

**Say:**
> *"The first thing I did was create a realistic messy dataset. In real jobs, you never get clean data. So I intentionally baked in every common data quality problem you'd face."*

**Then open** the terminal and run:

```bash
python data/raw/generate_raw_data.py
```

**Output you'll see:**
```
Generated raw_sales_data.csv  →  10,815 rows × 12 columns
    Nulls in revenue : 541
    Nulls in cost    : 433
    Null customers   : 216
    Negative qty rows: 108
```

**Say:**
> *"Look at this — 541 missing revenue values, 108 invalid negative quantities, over 200 missing customer names. And the dates? They're in four different formats — some MM/DD/YYYY, some YYYY-MM-DD, some like 15-Jan-2023. This is what real data looks like."*

**Optionally open raw_sales_data.csv in Excel** to show the mess visually (messy dates in column B, casing issues in category column, NaN gaps).

---

### STEP 3 — Run the Full Pipeline (2 minutes)

**In the terminal:**

```bash
python run_pipeline.py
```

**While it runs, narrate each step:**

```
Step 1/4  :  Generating raw data
```
> *"Step 1 generates the raw messy data."*

```
Step 2/4  :  Cleaning & engineering features
[1] Dropped duplicates  → 243 removed
[2] Parsed dates        → 0 unparseable rows dropped
[3] Normalised category → ['Clothing', 'Electronics', 'Food & Beverage', 'Furniture', 'Office Supplies']
[4] Negative qty rows   → 108 removed
[5] Imputed revenue     → 536 cells filled
[6] Imputed cost        → 429 cells filled
[7] Imputed customers   → 212 cells filled
```
> *"Step 2 is the cleaning pipeline. You can see each action logged: 243 duplicates removed, dates normalized, categories standardized. Missing revenue was filled using the formula: unit price times quantity. Missing cost was filled using the median cost ratio for that category. I didn't just delete nulls — I recovered the data intelligently."*

```
Step 3/4  :  Building EDA charts
  ✓  01_monthly_revenue_trend.png
  ✓  02_monthly_profit_margin.png
  ...
  ✓  08_region_heatmap.png
```
> *"Step 3 generates 8 charts — all saved as PNGs."*

```
Step 4/4  :  Writing HTML report
✓  Report saved → reports/sales_intelligence_report.html
Pipeline complete in 17.9s
```
> *"And in under 20 seconds, the entire pipeline ran — from raw messy data to a full report."*

---

### STEP 4 — Open the HTML Report (2 minutes)

**Open:** `reports/sales_intelligence_report.html` (double-click, opens in browser)

**Walk through each section:**

#### KPI Cards (top of page)
> *"These are the headline numbers — total revenue, total profit, average margin, total orders. This is what a CEO looks at first."*

#### Key Insight Box
> *"This is the most important part of the whole project. This is the finding that makes it a decision-ready report, not just charts. Two SKUs — 098 and 099 — have a cost ratio above 94%. They're being sold at a discount and barely making any money. Removing them improves overall portfolio profit margin. That's an actionable business recommendation."*

#### Monthly Revenue Trend Chart
> *"This shows revenue across all 12 months of 2023. A business can use this to identify peak seasons, plan inventory, or set sales targets."*

#### Profit Margin Chart
> *"The green bars are months above the median margin, red bars are below. Immediately you can see which months the business performed well and which didn't."*

#### Top-10 Products Table
> *"Ranked by revenue — so the sales team knows which products to push. And on the right, ranked by profit margin — so the finance team knows which products are actually efficient."*

#### Region × Category Heatmap
> *"This shows which product categories perform in which regions. For example, if Electronics is high in the North but low in the South, that's an opportunity for the sales team to target."*

---

### STEP 5 — Show the Jupyter Notebook (1 minute)

**Open:** `notebooks/sales_analysis.ipynb` in VS Code or Jupyter

**Say:**
> *"The notebook is the interactive version — same pipeline, but cell by cell so you can see what each piece of code does and why. This is how a data scientist would explore data before writing the final scripts."*

Show a couple of cells — the data quality audit cell and the SKU waterfall chart cell.

---

### STEP 6 — Show the Power BI Guide (30 seconds)

**Open:** `powerbi/POWERBI_SETUP.md`

**Say:**
> *"I documented every step to replicate this in Power BI — how to import the data, how to create relationships between tables, and here are the actual DAX formulas ready to copy-paste. Power BI makes it interactive — users can filter by region, by month, by category. The Python pipeline generates the data; Power BI presents it."*

---

### STEP 7 — Show the Code Quality (1 minute)

**Open** `src/clean_and_engineer.py`

**Point out:**
- The module-level docstring at the top explaining what each stage does
- Numbered steps `[1]`, `[2]` etc. matching the printed output
- `try/except` in the date parser (handles all 4 formats gracefully)
- No hardcoded magic numbers
- Comments explaining the *why*, not just the *what*

**Say:**
> *"Clean, readable code matters. Every function is documented. The output is logged so you always know what happened. This is production-style Python — not a messy notebook."*

---

## PART 3 — INTERVIEW Q&A PREP

> Practice answering these out loud. Your answers are already written.

---

### Q: "Walk me through your project."
**A:** Use the 60-second pitch from Part 1. Then offer to demo it live.

---

### Q: "What was the biggest challenge?"
**A:**
> *"The date parsing. The same column had four completely different date formats — MM/DD/YYYY, YYYY-MM-DD, DD-Mon-YYYY, and DD/MM/YYYY. A simple `pd.to_datetime()` would fail. I wrote a custom parser that tries each format in sequence and uses `pd.NaT` as a fallback if all fail. Then I dropped any rows where the date was still unparseable. Zero data loss for valid rows, clean handling of actually invalid ones."*

---

### Q: "How did you handle missing data?"
**A:**
> *"It depended on what was missing. For missing revenue, I could reconstruct it exactly: unit price times quantity. For missing cost, I didn't have enough info to reconstruct it exactly, so I used the median cost ratio for that product's category — a statistically sound imputation. For missing customer names, I filled with 'Unknown Customer' because the transaction was still valid, just unattributed."*

---

### Q: "What is feature engineering?"
**A:**
> *"It's creating new columns from existing data that make analysis easier or more meaningful. For example, I had a raw sale_date column. From that I engineered month_year — like '2023-01' — so I could group by month for trend analysis. I also calculated profit as revenue minus cost, and profit_margin_pct as profit divided by revenue times 100. These didn't exist in the raw data — I created them."*

---

### Q: "Why did you use Pandas?"
**A:**
> *"Pandas is the standard library for tabular data in Python. It's optimized for row/column operations on datasets of this size — tens of thousands of rows. It handles reading CSVs, filtering, grouping, aggregating, and handling nulls all in one tool. For larger datasets — say, hundreds of millions of rows — I'd use PySpark or DuckDB instead."*

---

### Q: "What does profit margin mean and why does it matter?"
**A:**
> *"Profit margin is the percentage of revenue that's actually profit after costs. A 40% margin means for every $100 in sales, $40 is profit. It matters because revenue alone is misleading — a product generating $1 million in revenue but costing $990,000 to produce has only a 1% margin and is nearly worthless to the business. Margin tells you how efficient a product actually is."*

---

### Q: "What would you do differently or add next?"
**A:**
> *"A few things. First, I'd add proper unit tests — pytest — to validate that the cleaning functions handle edge cases correctly. Second, I'd build an automated pipeline using Apache Airflow so it runs on a schedule — daily or weekly — without manual intervention. Third, I'd add a forecasting component — using Prophet or scikit-learn — to predict next quarter's revenue based on historical trends."*

---

### Q: "What's the difference between your Python report and a Power BI dashboard?"
**A:**
> *"My Python report is static — it's an HTML snapshot generated at a point in time. Power BI is interactive — users can filter, drill down, and explore the data themselves without any code. For a data analyst presenting findings to executives, Power BI is better. For a repeatable automated pipeline that runs overnight and emails a report, Python is better. They complement each other."*

---

### Q: "Can you explain your git commit history?"
**A:**
> *"I kept it to two logical commits. The first commit — 'feat: initial commit' — added the entire working project. The second — 'chore: make project fully GitHub-ready' — added professional polish: LICENSE, CONTRIBUTING.md, .gitattributes for cross-platform compatibility, fixed the .gitignore to exclude generated files. Real teams use Conventional Commits — feat, fix, chore, docs — so the history is readable."*

---

## PART 4 — QUICK REFERENCE CARD

> Print this or keep it open during your demo.

```
TERMINAL COMMANDS (run from project folder)
────────────────────────────────────────────
Run full pipeline:        python run_pipeline.py
Generate data only:       python data/raw/generate_raw_data.py
Clean data only:          python src/clean_and_engineer.py
Charts only:              python src/eda_and_charts.py
Report only:              python src/generate_report.py

FILES TO OPEN
────────────────────────────────────────────
GitHub repo:              https://github.com/Haseebjahangir26/Business-Sales-Intelligence-Dashboard-
Raw data script:          data/raw/generate_raw_data.py
Cleaning pipeline:        src/clean_and_engineer.py
HTML Report:              reports/sales_intelligence_report.html  (open in browser)
Notebook:                 notebooks/sales_analysis.ipynb
Power BI guide:           powerbi/POWERBI_SETUP.md

KEY NUMBERS TO REMEMBER
────────────────────────────────────────────
Dataset size:             10,000+ rows, 12 columns
Duplicates removed:       ~315 rows
Nulls imputed:            ~1,000+ cells across revenue, cost, customer
Date formats handled:     4 different formats
Charts generated:         8 publication-ready PNGs
Pipeline runtime:         ~18 seconds end to end
Key insight:              SKU-098 & SKU-099 → 94-99% cost ratio → drag on margin
```

---

## PART 5 — DEMO ORDER CHEAT SHEET

> The fastest, most impressive 8-minute demo:

| Time | Action |
|------|--------|
| 0:00 | Say the 60-second pitch |
| 1:00 | Open GitHub repo, point out structure + badges + chart previews |
| 1:45 | Open terminal, run `python run_pipeline.py`, narrate each step |
| 3:30 | Open `reports/sales_intelligence_report.html` in browser |
| 4:00 | Walk through KPI cards → Key Insight box → Revenue trend → Top-10 table |
| 6:00 | Open `src/clean_and_engineer.py`, show date parser and imputation logic |
| 7:00 | Open `powerbi/POWERBI_SETUP.md`, mention DAX measures |
| 7:30 | "Any questions?" |

---

*That's your full demo. You know this project inside out — you built it. Be confident.*
