# STUDY GUIDE — Chapter 4: Matplotlib & Seaborn
# Building Professional Data Visualizations

---

## 4.1 Why Visualize Data?

Numbers in a table are hard for humans to interpret quickly.
Charts make patterns **instantly obvious**.

Compare:
```
Monthly Revenue:
Jan: 234,123  Feb: 198,456  Mar: 312,789  Apr: 289,100  ...
```
vs. a line chart with a clear peak in March.

The chart communicates in 1 second what the table takes 30 seconds to parse.

---

## 4.2 Matplotlib vs Seaborn

| Library | Role | Think of it as |
|---------|------|---------------|
| **Matplotlib** | Low-level charting | The drawing toolkit — full control |
| **Seaborn** | High-level charting | Built on Matplotlib, less code, prettier defaults |

In practice: use Seaborn for statistical charts (heatmaps, distributions), use Matplotlib for everything else or for fine-tuning.

```python
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
```

---

## 4.3 The Figure and Axes Model

This is the most important concept in Matplotlib.

- **Figure** (`fig`) — the whole canvas/window
- **Axes** (`ax`) — one chart panel within the figure

```
┌─────────── Figure ───────────┐
│  ┌────── Axes ──────┐        │
│  │  ← chart lives  │        │
│  │    here          │        │
│  └──────────────────┘        │
└──────────────────────────────┘
```

```python
fig, ax = plt.subplots(figsize=(12, 5))
# fig = the window (12 inches wide, 5 inches tall)
# ax  = the chart area inside the window
```

Multiple charts side by side:
```python
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
ax1 = axes[0]   # left chart
ax2 = axes[1]   # right chart
```

---

## 4.4 Setting a Dark Style (Used in Our Project)

```python
plt.style.use("dark_background")
```

This sets the background to black and text to white — good for presentations and reports.
Our project uses this for all 8 charts.

Other available styles:
```python
plt.style.use("ggplot")       # R-inspired, gray background
plt.style.use("seaborn-v0_8") # clean white
plt.style.use("default")      # matplotlib default
```

---

## 4.5 Colors in Matplotlib

You can specify colors as:
- Named color: `"red"`, `"blue"`, `"white"`, `"gold"`, `"coral"`
- Hex code: `"#3498db"`, `"#e74c3c"`, `"#2ecc71"`
- RGB tuple: `(0.2, 0.5, 0.8)`
- Color from a colormap: `plt.cm.Greens(0.7)`

Color lists for multiple bars:
```python
colors = ["#2ecc71" if val > 0 else "#e74c3c" for val in values]
# Green for positive values, red for negative
```

---

## 4.6 Bar Charts (Chart 01 — Monthly Revenue)

```python
fig, ax = plt.subplots(figsize=(14, 5))

# Basic bar chart:
ax.bar(x_positions, values, width=0.6, color="#3498db", edgecolor="none")
```

In our project:
```python
# eda_and_charts.py — monthly revenue chart
bars = ax.bar(
    x,                    # x positions
    monthly["total_revenue"],   # bar heights
    width=0.6,
    color=ACCENT,         # teal color
    edgecolor="none",
    zorder=3,             # draw bars on top of gridlines
)
```

Adding a line on top of bars:
```python
ax.plot(x, monthly["total_revenue"], color="white", linewidth=2, marker="o", zorder=4)
```

Adding value labels on top of each bar:
```python
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,  # x position (center of bar)
        height,                               # y position (top of bar)
        f"${height/1000:.0f}K",              # label text
        ha="center",                          # horizontal alignment
        va="bottom",                          # vertical alignment
        fontsize=8,
        color="white",
    )
```

---

## 4.7 Horizontal Bar Charts (Chart 03 — Top Products)

```python
ax.barh(y_labels, values, color=colors, edgecolor="none", height=0.7)
```

`barh` = bar horizontal

In our project:
```python
# Top 10 products by revenue
bars = ax.barh(
    labels[::-1],           # reverse so #1 is at top
    values[::-1],
    color=colors[::-1],
    height=0.7,
)
```

`[::-1]` is Python's way to reverse a list.

---

## 4.8 Line Charts

```python
ax.plot(x, y, color="#3498db", linewidth=2)

# With markers (dots at each point):
ax.plot(x, y, color="#3498db", linewidth=2, marker="o", markersize=6)
```

Shading below the line (area chart):
```python
ax.fill_between(x, y, alpha=0.15, color="#3498db")
# alpha controls transparency: 0 = invisible, 1 = fully opaque
```

---

## 4.9 Pie Charts (Chart 06 — Category Revenue)

```python
wedges, texts, autotexts = ax.pie(
    values,
    labels=labels,
    autopct="%1.1f%%",      # show percentage on each slice
    startangle=90,          # rotate so first slice starts at top
    colors=colors,
    wedgeprops={"linewidth": 2, "edgecolor": "black"},
)
```

`autopct="%1.1f%%"` formats the percentage with 1 decimal place.

---

## 4.10 Waterfall Charts (Chart 07 — SKU Removal Impact)

Matplotlib doesn't have a built-in waterfall chart — you build it manually with bar charts.

A waterfall chart shows how values build up or break down:
- Start with baseline margin
- Show each SKU's contribution
- Show the final margin after removal

```python
# Waterfall uses bars that start from different y positions (bottoms)
ax.bar(x, heights, bottom=bottoms, color=colors, width=0.6)
```

`bottom` controls where the bar starts from — the visual "stack" effect.

---

## 4.11 Heatmaps with Seaborn (Chart 08 — Region × Category)

```python
sns.heatmap(
    pivot_data,              # 2D data (rows × columns)
    ax=ax,
    cmap="YlOrRd",           # colormap: Yellow → Orange → Red
    annot=True,              # show values in each cell
    fmt=".0f",               # format: no decimal places
    linewidths=0.5,          # grid lines between cells
    cbar_kws={"shrink": 0.8} # colorbar sizing
)
```

Common colormaps:
- `"Blues"` — white to dark blue
- `"Greens"` — white to dark green
- `"YlOrRd"` — yellow → orange → red (good for business data)
- `"RdYlGn"` — red → yellow → green (good for good/bad data)
- `"coolwarm"` — blue → white → red

---

## 4.12 Axis Labels, Titles, and Formatting

```python
# Labels:
ax.set_xlabel("Month", fontsize=12, labelpad=10)
ax.set_ylabel("Revenue ($)", fontsize=12, labelpad=10)
ax.set_title("Monthly Revenue Trend", fontsize=16, fontweight="bold", pad=20)

# X-axis tick labels:
ax.set_xticks(x_positions)
ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=9)

# Remove tick marks (just keep labels):
ax.tick_params(axis="x", length=0)

# Axis limits:
ax.set_xlim(-0.5, len(x) - 0.5)
ax.set_ylim(0, max_value * 1.15)    # add 15% headroom above bars

# Remove axis spines (the border lines):
for spine in ax.spines.values():
    spine.set_visible(False)
```

---

## 4.13 Formatting Numbers on Axis

```python
import matplotlib.ticker as mticker

# Format y-axis as $K (thousands):
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}K")
)

# Format y-axis as percentage:
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{x:.1f}%")
)
```

---

## 4.14 Gridlines

```python
# Add horizontal gridlines:
ax.yaxis.grid(True, linestyle="--", alpha=0.3, color="white")

# z-order (what's drawn on top of what):
ax.set_axisbelow(True)   # gridlines behind bars (not on top)
```

---

## 4.15 Adding Text Annotations

```python
# Simple text at a position:
ax.text(
    x=0.5,              # x position
    y=0.95,             # y position (in axes coordinates: 0=bottom, 1=top)
    s="Key Insight",    # the text
    transform=ax.transAxes,   # coordinates relative to axes (not data)
    fontsize=14,
    color="white",
    ha="center",        # horizontal alignment
    va="top",           # vertical alignment
)
```

Difference between data coordinates and axes coordinates:
- **Data coordinates**: `x=2023, y=500000` — position on the actual chart scale
- **Axes coordinates**: `x=0.5, y=0.95` — 0 to 1, relative to axes size (use `transform=ax.transAxes`)

In our project — adding a reference line:
```python
ax.axhline(y=median_margin, color="white", linestyle="--", alpha=0.4, linewidth=1.5)
ax.text(len(x) - 0.3, median_margin + 0.3, f"Median {median_margin:.1f}%", ...)
```

`axhline` = horizontal reference line across the whole chart.
`axvline` = vertical reference line.

---

## 4.16 Legends

```python
# Automatic legend from chart elements:
ax.plot(x, y1, label="Revenue", color="teal")
ax.plot(x, y2, label="Profit", color="gold")
ax.legend(loc="upper left", fontsize=10)

# legend() location options: "upper left", "upper right", "lower left",
# "lower right", "center", "best"
```

Custom legend (for when chart elements don't auto-label):
```python
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="teal", label="Revenue"),
    Patch(facecolor="gold", label="Profit"),
]
ax.legend(handles=legend_elements, loc="upper left")
```

---

## 4.17 Tight Layout and Saving

```python
# Prevent labels from being cut off:
fig.tight_layout(pad=2.0)

# Save the figure:
plt.savefig(
    "reports/figures/01_monthly_revenue_trend.png",
    dpi=150,           # resolution: 150 dots per inch (good for screen)
    bbox_inches="tight",  # no whitespace cut off
    facecolor=fig.get_facecolor()   # preserve background color
)

# Close the figure (free memory):
plt.close(fig)
```

Why `plt.close(fig)`? Matplotlib keeps figures in memory. For 8 charts, you'd accumulate 8 figures. Close each one after saving.

---

## 4.18 Subplots — Multiple Charts in One Figure

```python
# 1 row, 2 columns (side by side):
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# 2 rows, 2 columns (2x2 grid):
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
ax_top_left     = axes[0, 0]
ax_top_right    = axes[0, 1]
ax_bottom_left  = axes[1, 0]
ax_bottom_right = axes[1, 1]
```

Shared axis (useful for comparison charts):
```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
# sharey=True: both charts use the same y-axis scale
```

---

## 4.19 Full Chart Recipe (Used in Our Project)

Here's the pattern for every chart:

```python
def make_chart(df):
    # 1. Set up figure and axes
    fig, ax = plt.subplots(figsize=(14, 5))
    fig.patch.set_facecolor(BG)    # background color
    ax.set_facecolor(BG)           # axes background

    # 2. Draw the chart
    ax.bar(x, y, color=ACCENT)

    # 3. Style axes
    ax.set_title("Chart Title", fontsize=16, fontweight="bold", color="white", pad=20)
    ax.set_xlabel("X Label", color="white", fontsize=11)
    ax.set_ylabel("Y Label", color="white", fontsize=11)
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_visible(False)

    # 4. Add gridlines
    ax.yaxis.grid(True, linestyle="--", alpha=0.2, color="white")
    ax.set_axisbelow(True)

    # 5. Format numbers
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v/1000:.0f}K"))

    # 6. Save and close
    fig.tight_layout(pad=2)
    plt.savefig(OUTPUT_PATH, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
```

---

## 4.20 Color Strategy in Our Project

```python
# Constants defined at top of eda_and_charts.py
BG     = "#0d1117"    # dark background (GitHub dark theme)
CARD   = "#161b22"    # slightly lighter dark (card backgrounds)
ACCENT = "#00bfae"    # teal — main color
GOLD   = "#f0b429"    # gold — secondary highlight
RED    = "#e05252"    # red — negative/bad
GREEN  = "#52e0a0"    # green — positive/good
TEXT   = "#e6edf3"    # near-white text
```

Why a defined color palette?
- Consistency across all 8 charts
- Professional look (not random colors)
- Easy to change theme: update 6 variables, all charts update

---

## 4.21 What You Now Know

You now understand:
- Figure vs Axes model
- Dark theme styling
- Bar charts, horizontal bar charts, line charts, pie charts, waterfall charts, heatmaps
- Axis labels, titles, tick formatting
- Number formatters ($K, %)
- Gridlines, annotations, reference lines, legends
- Saving charts with proper DPI
- The full chart recipe used in this project

**Next:** Chapter 5 — Statistics for Data Science (the math behind the analysis).
