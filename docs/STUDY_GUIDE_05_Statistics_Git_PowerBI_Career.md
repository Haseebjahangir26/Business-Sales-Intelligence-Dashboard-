# STUDY GUIDE — Chapter 5: Statistics, Git & Power BI
# The Business Math, Version Control, and Dashboard Layer

---

# SECTION A: STATISTICS FOR DATA SCIENCE

---

## 5.1 Why Statistics?

Statistics lets you summarize, describe, and understand data.
Without statistics, you're just looking at raw numbers with no context.

---

## 5.2 Measures of Central Tendency

Three ways to describe "the typical value" in a dataset:

### Mean (Average)
```python
values = [10, 20, 30, 40, 500]
mean = sum(values) / len(values)   # = 120
```
Problem: one outlier (500) pulls the mean way up. Is 120 "typical"? No.

### Median (Middle Value)
```python
sorted_values = [10, 20, 30, 40, 500]
median = 30    # the middle value when sorted
```
Median is not affected by outliers. Much more reliable for skewed data.

### Mode (Most Common Value)
```python
from statistics import mode
values = [10, 20, 20, 30, 40]
mode(values)   # 20
```

**Rule of thumb:**
- Use **mean** when data is roughly symmetric (bell curve shaped)
- Use **median** when data is skewed or has outliers
- Use **mode** for categorical data (what's the most common category?)

In our project: used **median cost ratio per category** to impute missing costs — because cost ratios within a category are skewed by outliers (the bad SKUs).

---

## 5.3 Measures of Spread

How spread out are the values?

### Range
```python
data_range = max(values) - min(values)
```

### Variance
Average of squared distances from the mean. High variance = very spread out.
```python
import numpy as np
np.var(values)
```

### Standard Deviation (most useful)
Square root of variance. In the same units as the original data.
```python
np.std(values)
```

Example: if mean revenue is $500 and std dev is $100:
- Most transactions (68%) are between $400 and $600
- Almost all (95%) are between $300 and $700

### IQR (Interquartile Range)
```python
Q1 = np.percentile(values, 25)   # 25th percentile
Q3 = np.percentile(values, 75)   # 75th percentile
IQR = Q3 - Q1                    # middle 50% spread
```

Robust to outliers — preferred when data has outliers.

---

## 5.4 Percentiles and Quantiles

A percentile tells you what % of the data falls below a value.
```python
np.percentile(data, 90)   # 90th percentile: 90% of data is below this
np.percentile(data, 50)   # same as median
```

Quantile = percentile / 100:
```python
df["revenue"].quantile(0.25)   # 25th percentile (first quartile)
df["revenue"].quantile(0.75)   # 75th percentile (third quartile)
```

In our project:
```python
rev_q1 = df["revenue"].quantile(0.33)   # 33rd percentile
rev_q2 = df["revenue"].quantile(0.67)   # 67th percentile
# Used for revenue_band classification: Low / Medium / High
```

---

## 5.5 Correlation

How strongly are two variables related?

Correlation coefficient ranges from -1 to +1:
- `+1` → perfect positive correlation (as X goes up, Y goes up)
- `0`  → no relationship
- `-1` → perfect negative correlation (as X goes up, Y goes down)

```python
df[["revenue", "profit"]].corr()
```

Example output:
```
         revenue   profit
revenue     1.00     0.85
profit      0.85     1.00
```

Revenue and profit have 0.85 correlation — very strongly related (expected: more revenue usually means more profit).

**Important:** Correlation ≠ Causation. Just because two things correlate doesn't mean one causes the other.

---

## 5.6 Distribution Shapes

**Normal distribution (bell curve):**
```
        ████
      ████████
    ████████████
  ████████████████
████████████████████
```
Symmetric around the mean. Many natural phenomena follow this.

**Right-skewed (positive skew):**
```
████
████████
████████████████████
```
Most values are low, a few are very high. Revenue distributions are often like this.

**Left-skewed (negative skew):**
```
                    ████
████████████████████████
```
Most values are high, a few are very low.

In our project: revenue is right-skewed because most transactions are small but a few large orders pull the tail right. This is why we use median (not mean) for imputation.

---

## 5.7 Key Business Metrics Summary

| Metric | Formula | Meaning |
|--------|---------|---------|
| Revenue | price × quantity | Total money received |
| Cost | cost per unit × quantity | Total money spent to produce/buy |
| Gross Profit | revenue - cost | Money left after direct costs |
| Profit Margin % | (profit / revenue) × 100 | % of revenue that's profit |
| Cost Ratio | cost / revenue | % of revenue that's cost |
| YoY Growth | (this year - last year) / last year × 100 | Year-over-year growth % |
| MoM Growth | (this month - last month) / last month × 100 | Month-over-month growth % |
| Avg Order Value | total revenue / number of orders | Average transaction size |

---

# SECTION B: GIT & GITHUB

---

## 5.8 What is Git?

Git is **version control** — it tracks every change you make to code.
Think of it like "track changes" in Word but for code, and much more powerful.

**Why use Git?**
- Go back to any previous version of your code
- Work with others without overwriting each other's work
- Show your work history (proves you actually built it)
- Required for every professional software/data job

---

## 5.9 Git vs GitHub

| | Git | GitHub |
|--|-----|--------|
| What | Tool on your computer | Website on the internet |
| Purpose | Tracks changes locally | Stores code online / shows to others |
| Analogy | Your personal diary | Uploading that diary to a public library |

---

## 5.10 Core Git Concepts

| Term | What it means |
|------|--------------|
| **Repository (repo)** | A folder tracked by Git |
| **Commit** | A saved snapshot of your code at a point in time |
| **Branch** | A parallel version of your code (for new features) |
| **Remote** | The copy of your repo on GitHub |
| **Push** | Send commits from local → GitHub |
| **Pull** | Get commits from GitHub → local |
| **Clone** | Download a full repo from GitHub to your computer |
| **Staging** | Telling Git "I want to include these files in my next commit" |

---

## 5.11 The Git Workflow

```
Working Directory → Staging Area → Repository (commit history)
    [your files]     [git add]       [git commit]
```

```bash
# Check the status of your repo:
git status

# Stage all files:
git add .

# Stage specific files:
git add README.md

# Commit with a message:
git commit -m "feat: add monthly revenue chart"

# Push to GitHub:
git push origin main
```

---

## 5.12 Conventional Commits

A professional standard for writing commit messages:

```
<type>: <short description>
```

Types:
- `feat:` → new feature
- `fix:` → bug fix
- `docs:` → documentation only
- `chore:` → maintenance (no feature/fix)
- `refactor:` → restructuring code
- `style:` → formatting only

Examples:
```
feat: add SKU rationalization waterfall chart
fix: resolve date parsing error for DD-Mon-YYYY format
docs: update README with project structure
chore: add .gitignore to exclude generated files
```

Bad examples (don't do this):
```
update
fix stuff
asdfgh
final version 2 (real)
```

---

## 5.13 .gitignore

A file that tells Git to **ignore** certain files — don't track them.

```
# In .gitignore:
*.csv                # ignore all CSV files
*.html               # ignore all HTML files
__pycache__/         # ignore Python cache directories
.venv/               # ignore the virtual environment
*.pyc                # ignore compiled Python files
```

In our project — why ignore raw_sales_data.csv and the HTML report?
- They're **generated files** — anyone can recreate them by running the pipeline
- They're large (1.4 MB+) and would bloat the repo
- What to version control: **source code** (the scripts that create things), not the things created

---

## 5.14 Branches

```bash
# See all branches:
git branch

# Create a new branch:
git checkout -b feature/add-forecasting

# Switch back to main:
git checkout main

# Merge your feature branch into main:
git merge feature/add-forecasting

# Delete a branch after merging:
git branch -d feature/add-forecasting
```

Professional workflow (Git Flow):
1. `main` — always working, production-ready code
2. `develop` — integration branch
3. `feature/xyz` — work on new features here
4. When feature is done → merge into develop → test → merge into main

---

## 5.15 Viewing History

```bash
git log                    # full history
git log --oneline          # compact one-line history
git log --oneline -5       # last 5 commits
git show abc123            # show details of a specific commit
git diff                   # what changed since last commit
```

---

# SECTION C: POWER BI

---

## 5.16 What is Power BI?

Power BI is Microsoft's business intelligence (BI) tool. It lets you:
- Connect to data sources (CSV, Excel, SQL, APIs)
- Build interactive dashboards
- Share reports with others

Where Python gives you code-based analysis, Power BI gives you **drag-and-drop interactive dashboards** for non-technical users.

---

## 5.17 Power BI Desktop vs Power BI Service

| | Power BI Desktop | Power BI Service |
|--|--|--|
| What | Free Windows app | Cloud website (powerbi.com) |
| Purpose | Build and design reports | Share and distribute reports |
| Who uses it | Analysts (builders) | Business users (viewers) |

Download: https://powerbi.microsoft.com/en-us/desktop/

---

## 5.18 The Data Model

Before building charts in Power BI, you define the **data model** — how tables relate to each other.

Our project's data model:

```
clean_sales_data (fact table — the big transaction table)
    |
    ├── [many-to-one] ──→  product_summary  (one row per SKU)
    ├── [many-to-one] ──→  customer_summary (one row per customer)
    └── [many-to-one] ──→  monthly_summary  (one row per month)
```

A **fact table** contains the detailed transactions. **Dimension tables** contain descriptive info (product details, customer details). This is the **star schema** — the most common data model in BI.

---

## 5.19 DAX — Data Analysis Expressions

DAX is Power BI's formula language. It looks like Excel formulas but is more powerful.

### Basic Measures (what we documented)

**Total Revenue:**
```dax
Total Revenue = SUM(clean_sales_data[revenue])
```

**Total Profit:**
```dax
Total Profit = SUM(clean_sales_data[profit])
```

**Overall Margin %:**
```dax
Overall Margin % = DIVIDE([Total Profit], [Total Revenue], 0) * 100
```
`DIVIDE` is safer than `/` because it returns 0 (not an error) when dividing by zero.

**Total Orders:**
```dax
Total Orders = DISTINCTCOUNT(clean_sales_data[order_id])
```

**Average Order Value:**
```dax
Avg Order Value = DIVIDE([Total Revenue], [Total Orders])
```

---

## 5.20 DAX Context

The most important DAX concept: **filter context**.

A measure like `Total Revenue = SUM(revenue)` returns different values depending on what filters are active on the report:
- Filter by region "North" → returns only North revenue
- Filter by month "January" → returns only January revenue
- No filter → returns all revenue

This is what makes Power BI interactive — the same measure adapts to whatever the user has filtered.

---

## 5.21 Power BI Visual Types

| Visual | When to use |
|--------|------------|
| Bar/Column Chart | Comparison between categories |
| Line Chart | Trends over time |
| Pie/Donut Chart | Part-to-whole (max 5-6 slices) |
| Table/Matrix | Detailed data, multiple metrics |
| Card | Single KPI number (big number display) |
| Map | Geographic data |
| Slicer | Filter control for the user |
| Scatter Plot | Correlation between two numeric variables |
| Heatmap (Matrix) | Two-dimensional comparison |

---

## 5.22 Power BI Dashboard Layout (Our Project)

**Page 1 — Executive Summary**
- KPI Cards: Total Revenue, Total Profit, Overall Margin %, Total Orders
- Line chart: Monthly revenue trend
- Bar chart: Revenue by category

**Page 2 — Product Analysis**
- Table: Top 10 products by revenue with margin %
- Bar chart: Revenue vs profit by SKU
- Slicer: Filter by category

**Page 3 — Customer Analysis**
- Table: Top customers by revenue
- Chart: Customer order frequency
- Slicer: Filter by region

**Page 4 — SKU Rationalization**
- What-if parameter slider: Which SKUs to remove?
- Card: Current margin vs adjusted margin
- Table: SKU performance ranking

---

## 5.23 The Relationship Between Python and Power BI

They solve different problems:

```
Python Pipeline:
  raw CSV → clean CSV → chart PNGs → HTML report
  (automated, scheduled, reproducible, code-based)

Power BI:
  clean CSV → interactive dashboard
  (interactive, user-controlled, no code needed to view)
```

Best practice:
1. Use Python to **clean and engineer** the data
2. Export clean CSVs
3. Import those CSVs into Power BI
4. Build interactive dashboards in Power BI

This way, when new data arrives:
1. Re-run the Python pipeline → updated clean CSVs
2. Hit "Refresh" in Power BI → dashboard updates automatically

---

# SECTION D: VIRTUAL ENVIRONMENTS & JUPYTER

---

## 5.24 Virtual Environments

**The problem:** Different projects need different versions of libraries. If you install everything globally, projects conflict.

**The solution:** A virtual environment — an isolated Python installation per project.

```bash
# Create a virtual environment:
python -m venv .venv

# Activate it (Windows):
.venv\Scripts\activate

# Activate it (Mac/Linux):
source .venv/bin/activate

# Your terminal shows (.venv) when active

# Install packages into the venv:
pip install pandas matplotlib seaborn

# Save what's installed (so others can replicate):
pip freeze > requirements.txt

# Someone else installs from requirements.txt:
pip install -r requirements.txt

# Deactivate:
deactivate
```

**Why `.venv` in our project?**
The `.gitignore` file excludes it — 150+ MB of library files don't get pushed to GitHub. Instead, `requirements.txt` is committed — it's just a text file listing what to install. Anyone who clones the repo runs `pip install -r requirements.txt` and gets the exact same setup.

---

## 5.25 Jupyter Notebooks

A Jupyter Notebook (`.ipynb`) lets you mix:
- Python code (in cells you can run)
- Output (charts, tables, text — shown immediately below each cell)
- Markdown text (headers, explanations)

This makes it perfect for:
- Exploring data interactively
- Explaining your analysis step by step
- Portfolio demonstrations

```bash
# Open the notebook:
jupyter notebook notebooks/sales_analysis.ipynb
# or in VS Code: just click the .ipynb file
```

**Cell types:**
- **Code cell** → runs Python, shows output
- **Markdown cell** → formatted text (headers, bullet points, bold, italics)
- **Raw cell** → plain text, not rendered

**Kernel** = the Python instance running behind the notebook. If things get weird, "Restart Kernel" fixes it.

**Why notebooks for our project?**
The `sales_analysis.ipynb` is the **walkthrough version** of the pipeline — same code but with explanations between each step. Great for:
- Learning (run one cell, see what it does)
- Presentations (show your code AND your output side by side)
- Job interviews (walk through it live)

---

## 5.26 pip — Python's Package Manager

```bash
pip install pandas               # install a package
pip install pandas==2.2.0        # install specific version
pip install pandas>=2.0,<3.0     # install any version in range

pip uninstall pandas             # remove a package
pip list                         # see all installed packages
pip show pandas                  # details about a specific package
pip freeze                       # all packages with exact versions
pip freeze > requirements.txt    # save to file
pip install -r requirements.txt  # install from file
pip install --upgrade pandas     # update to latest version
```

---

# SECTION E: THE DATA SCIENCE CAREER PATH

---

## 5.27 Job Titles in Data (What's the Difference?)

| Role | Main Tool | What They Do |
|------|-----------|-------------|
| **Data Analyst** | Excel, SQL, Power BI | Describe what happened (reports, dashboards) |
| **Data Scientist** | Python, ML libraries | Predict what will happen (models) |
| **Data Engineer** | Python, Spark, SQL | Build pipelines that move and store data |
| **Business Intelligence (BI) Analyst** | Power BI, Tableau | Build dashboards for business decisions |
| **ML Engineer** | Python, TensorFlow | Deploy ML models to production |

**This project covers:** Data Analyst + BI Analyst skills. A strong foundation.

---

## 5.28 What To Learn Next (Ordered by Priority)

| Priority | Topic | Why |
|----------|-------|-----|
| 1 | **SQL** | 90% of data jobs require SQL. It's how you get data from databases. |
| 2 | **Statistics deeper** | Hypothesis testing, regression, A/B testing |
| 3 | **Excel + Power BI** | Still used everywhere in business |
| 4 | **scikit-learn** | Machine learning — classification, regression, clustering |
| 5 | **Tableau** | Alternative to Power BI, used in many companies |
| 6 | **Cloud basics** | AWS / Azure / GCP — data lives there now |
| 7 | **APIs + Web Scraping** | Getting data from the internet |
| 8 | **Apache Spark** | Big data (millions of rows, not thousands) |

**Recommended free resources:**
- SQL: https://sqlzoo.net / https://mode.com/sql-tutorial/
- Python: https://www.kaggle.com/learn
- Statistics: https://www.khanacademy.org/math/statistics-probability
- Power BI: Microsoft Learn free courses
- Machine Learning: Andrew Ng's course on Coursera (free to audit)

---

## 5.29 Your Study Plan (4 Weeks to Job-Ready Basics)

### Week 1: Python Solid
- Read Chapter 1 and 2 of this guide
- Practice: rewrite `generate_raw_data.py` from scratch without looking
- Goal: understand every line of `clean_and_engineer.py`

### Week 2: Data Skills
- Read Chapter 3 of this guide
- Practice: take a new dataset from Kaggle, clean it yourself
- Goal: do a full clean → feature engineer → export on a new dataset

### Week 3: Visualization + Stats
- Read Chapters 4 and 5 of this guide
- Practice: recreate all 8 charts from memory using the clean data
- Goal: build a mini EDA report on a Kaggle dataset

### Week 4: SQL + Power BI
- Learn SQL basics (SELECT, WHERE, GROUP BY, JOIN)
- Build the Power BI dashboard using the POWERBI_SETUP.md guide
- Goal: full project presentation ready

### After Week 4: Portfolio
- Upload this project to GitHub ✅ (done)
- Start a second project on a Kaggle dataset
- Add SQL queries to demonstrate database skills
- Apply for Data Analyst / BI Analyst internships

---

## 5.30 What Interviewers Actually Test

| They ask | They're testing |
|----------|----------------|
| "Walk me through your project" | Communication, clarity |
| "What was the hardest part?" | Problem-solving, honesty |
| "How did you handle nulls?" | Technical depth |
| "What's a profit margin?" | Domain knowledge |
| "Write a SQL query to..." | SQL skills |
| "What's the difference between mean and median?" | Statistics fundamentals |
| "How would you scale this?" | Systems thinking |
| "What would you do differently?" | Self-reflection, growth mindset |

---

## 5.31 Summary — What This Project Demonstrates

By completing this project you have demonstrated:

✅ **Python proficiency** — functions, loops, conditionals, error handling, imports  
✅ **Pandas data manipulation** — reading CSVs, cleaning, groupby, feature engineering  
✅ **Data cleaning** — handling nulls, duplicates, inconsistent formats  
✅ **Feature engineering** — deriving profit margin, revenue bands, time features  
✅ **Statistical thinking** — median imputation, percentiles, distribution awareness  
✅ **Data visualization** — 8 publication-ready charts with consistent design  
✅ **Business intelligence** — actionable SKU rationalization recommendation  
✅ **Report generation** — self-contained HTML executive report  
✅ **Git & GitHub** — proper version control, clean commit history  
✅ **Documentation** — README, CONTRIBUTING, demo guide, Power BI setup  
✅ **Pipeline design** — modular, reproducible, end-to-end pipeline  

That's a Data Analyst job application-ready portfolio project. You built it. You understand it. Go get the job.
