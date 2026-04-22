"""
generate_raw_data.py
────────────────────
Generates a realistic, intentionally-messy 10 000+ row sales dataset.
Issues baked in:
  • Duplicate rows                (~3 %)
  • Inconsistent category casing  ("Electronics" / "ELECTRONICS" / "electronics")
  • Inconsistent date formats      (MM/DD/YYYY, YYYY-MM-DD, DD-Mon-YYYY …)
  • Missing revenue / cost values  (~5 %)
  • Null customer names            (~2 %)
  • Invalid negative quantities    (~1 %)
  • Two deliberately underperforming SKUs (SKU-098, SKU-099)
"""

import random
import numpy as np
import pandas as pd
from faker import Faker

random.seed(42)
np.random.seed(42)
fake = Faker()
Faker.seed(42)

# ── Constants ──────────────────────────────────────────────────────────────────
N_ROWS = 10_500          # we'll trim dupes later to land ~10 000 unique

CATEGORIES = {
    "Electronics":  {"base_price_range": (50,  1200), "cost_pct_range": (0.45, 0.65)},
    "Furniture":    {"base_price_range": (80,   900), "cost_pct_range": (0.40, 0.60)},
    "Clothing":     {"base_price_range": (15,   250), "cost_pct_range": (0.30, 0.50)},
    "Office Supplies": {"base_price_range": (5, 150), "cost_pct_range": (0.35, 0.55)},
    "Food & Beverage": {"base_price_range": (3,  80), "cost_pct_range": (0.50, 0.70)},
}

CATEGORY_NAMES = list(CATEGORIES.keys())

# 38 regular SKUs  +  2 bad ones (bad SKUs get heavy volume to drag margin)
REGULAR_SKUS = [f"SKU-{str(i).zfill(3)}" for i in range(1, 39)]
BAD_SKUS     = ["SKU-098", "SKU-099"]
ALL_SKUS     = REGULAR_SKUS + BAD_SKUS

SKU_CATEGORY = {}
for sku in REGULAR_SKUS:
    SKU_CATEGORY[sku] = random.choice(CATEGORY_NAMES)
SKU_CATEGORY["SKU-098"] = "Office Supplies"
SKU_CATEGORY["SKU-099"] = "Office Supplies"

# 200 customers
CUSTOMERS = [fake.company() for _ in range(200)]

REGIONS = ["North", "South", "East", "West", "Central"]

DATE_START = pd.Timestamp("2023-01-01")
DATE_END   = pd.Timestamp("2023-12-31")


def random_date() -> pd.Timestamp:
    delta = (DATE_END - DATE_START).days
    return DATE_START + pd.Timedelta(days=random.randint(0, delta))


def format_date_messy(ts: pd.Timestamp) -> str:
    """Return the same date in one of four formats at random."""
    style = random.randint(0, 3)
    if style == 0:
        return ts.strftime("%m/%d/%Y")       # 01/15/2023
    elif style == 1:
        return ts.strftime("%Y-%m-%d")        # 2023-01-15
    elif style == 2:
        return ts.strftime("%d-%b-%Y")        # 15-Jan-2023
    else:
        return ts.strftime("%d/%m/%Y")        # 15/01/2023


def messy_category(cat: str) -> str:
    """Randomly mis-case the category name."""
    style = random.random()
    if style < 0.70:
        return cat                    # correct
    elif style < 0.85:
        return cat.upper()            # "ELECTRONICS"
    elif style < 0.95:
        return cat.lower()            # "electronics"
    else:
        return cat.title()            # already title, fine for compound names


# ── Row builder ────────────────────────────────────────────────────────────────
rows = []
for _ in range(N_ROWS):
    sku      = random.choice(ALL_SKUS)
    cat      = SKU_CATEGORY[sku]
    cfg      = CATEGORIES[cat]
    customer = random.choice(CUSTOMERS)
    region   = random.choice(REGIONS)
    ts       = random_date()

    unit_price = round(random.uniform(*cfg["base_price_range"]), 2)
    cost_pct   = random.uniform(*cfg["cost_pct_range"])
    quantity   = random.randint(1, 50)

    # underperformers: near-break-even cost ratio, heavily discounted price, high volume
    if sku in BAD_SKUS:
        cost_pct   = random.uniform(0.94, 0.99)   # 1-6% margin only
        unit_price = round(unit_price * 0.55, 2)  # sold well below market
        quantity   = random.randint(40, 100)       # high volume = massive margin drag
    revenue  = round(unit_price * quantity, 2)
    cost     = round(unit_price * cost_pct * quantity, 2)

    rows.append({
        "order_id":     f"ORD-{fake.unique.random_number(digits=7, fix_len=True)}",
        "sale_date":    format_date_messy(ts),
        "sku":          sku,
        "product_name": f"{cat} Item {sku}",
        "category":     messy_category(cat),
        "customer_name":customer,
        "region":       region,
        "quantity":     quantity,
        "unit_price":   unit_price,
        "revenue":      revenue,
        "cost":         cost,
        "sales_rep":    fake.name(),
    })

df = pd.DataFrame(rows)

# ── Inject data-quality issues ─────────────────────────────────────────────────

# 1. Duplicate rows (~3 %)
dup_idx = df.sample(frac=0.03, random_state=1).index
df = pd.concat([df, df.loc[dup_idx]], ignore_index=True)

# 2. Missing revenue (~5 %)
mask_rev = df.sample(frac=0.05, random_state=2).index
df.loc[mask_rev, "revenue"] = np.nan

# 3. Missing cost (~4 %)
mask_cost = df.sample(frac=0.04, random_state=3).index
df.loc[mask_cost, "cost"] = np.nan

# 4. Null customer names (~2 %)
mask_cust = df.sample(frac=0.02, random_state=4).index
df.loc[mask_cust, "customer_name"] = np.nan

# 5. Negative quantities (~1 %)
mask_qty = df.sample(frac=0.01, random_state=5).index
df.loc[mask_qty, "quantity"] = df.loc[mask_qty, "quantity"] * -1

# 6. Shuffle row order
df = df.sample(frac=1, random_state=99).reset_index(drop=True)

# ── Save ───────────────────────────────────────────────────────────────────────
df.to_csv("raw_sales_data.csv", index=False)
print(f"✅  Generated raw_sales_data.csv  →  {len(df):,} rows  ×  {len(df.columns)} columns")
print(f"    Nulls in revenue : {df['revenue'].isna().sum()}")
print(f"    Nulls in cost    : {df['cost'].isna().sum()}")
print(f"    Null customers   : {df['customer_name'].isna().sum()}")
print(f"    Negative qty rows: {(df['quantity'] < 0).sum()}")
