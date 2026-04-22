# STUDY GUIDE — Chapter 1: Python Fundamentals
# From Zero to Understanding Every Line of This Project

---

## 1.1 What is Python?

Python is a programming language. A programming language lets you give instructions to a computer.
When you write Python code, you are writing a list of instructions in a file. Python reads that file
top to bottom and does what you said.

A Python file ends in `.py`. Example: `run_pipeline.py`, `clean_and_engineer.py`.

---

## 1.2 Variables

A variable is a named box that stores a value.

```python
name = "Haseeb"       # stores text (called a string)
age = 21              # stores a whole number (called an integer)
margin = 47.5         # stores a decimal number (called a float)
is_ready = True       # stores True or False (called a boolean)
```

In our project:
```python
N_ROWS = 10_500       # variable storing how many rows to generate
BAD_SKUS = ["SKU-098", "SKU-099"]   # variable storing a list
```

The `_` in `10_500` is just for readability — Python ignores it. Same as writing 10500.

---

## 1.3 Data Types

| Type | Example | What it is |
|------|---------|-----------|
| `str` | `"hello"` | Text — always in quotes |
| `int` | `42` | Whole number |
| `float` | `3.14` | Decimal number |
| `bool` | `True` / `False` | Yes or No |
| `list` | `[1, 2, 3]` | An ordered collection |
| `dict` | `{"key": "value"}` | Key-value pairs |
| `None` | `None` | Represents "nothing" / "missing" |

Check the type of anything with `type()`:
```python
type("hello")   # <class 'str'>
type(42)        # <class 'int'>
type(3.14)      # <class 'float'>
```

---

## 1.4 Strings

Text data. Anything inside quotes.

```python
category = "Electronics"

# Common string methods:
category.upper()        # "ELECTRONICS"
category.lower()        # "electronics"
category.title()        # "Electronics"  (first letter of each word capitalized)
category.strip()        # removes spaces from start and end
category.replace("e", "E")  # replaces characters

# Check if something is in a string:
"Elect" in category     # True

# f-strings — the modern way to build strings:
sku = "SKU-001"
msg = f"Processing {sku} now"   # "Processing SKU-001 now"
```

In our project:
```python
# clean_and_engineer.py line 40
df["category"] = df["category"].str.strip().str.title()
# .str. means "apply this string method to every row in this column"
```

---

## 1.5 Lists

An ordered collection of items. Uses square brackets `[]`.

```python
regions = ["North", "South", "East", "West", "Central"]

regions[0]      # "North"   (indexing starts at 0, not 1)
regions[-1]     # "Central" (negative index = from the end)
regions[1:3]    # ["South", "East"]  (slicing)

len(regions)    # 5  (how many items)

regions.append("Northeast")   # add to end
regions.remove("South")       # remove a specific item
"North" in regions            # True  (check membership)
```

In our project:
```python
ALL_SKUS = REGULAR_SKUS + BAD_SKUS   # joining two lists
random.choice(ALL_SKUS)               # picks a random item from the list
```

---

## 1.6 Dictionaries

Key-value pairs. Uses curly braces `{}`. Like a lookup table.

```python
person = {
    "name": "Haseeb",
    "age": 21,
    "city": "Lahore"
}

person["name"]          # "Haseeb"
person["age"]           # 21
person.keys()           # dict_keys(["name", "age", "city"])
person.values()         # dict_values(["Haseeb", 21, "Lahore"])
person.items()          # dict_items([("name","Haseeb"), ("age",21), ...])

# Add a new key:
person["job"] = "Data Analyst"

# Check if a key exists:
"name" in person        # True
```

In our project:
```python
# generate_raw_data.py
CATEGORIES = {
    "Electronics": {"base_price_range": (50, 1200), "cost_pct_range": (0.45, 0.65)},
    "Furniture":   {"base_price_range": (80, 900),  "cost_pct_range": (0.40, 0.60)},
}
# Accessing nested dict:
cfg = CATEGORIES["Electronics"]
cfg["base_price_range"]   # (50, 1200)
```

---

## 1.7 If / Elif / Else (Conditions)

Make decisions in code.

```python
score = 85

if score >= 90:
    print("A grade")
elif score >= 80:
    print("B grade")
elif score >= 70:
    print("C grade")
else:
    print("Below C")
```

In our project:
```python
# generate_raw_data.py
if sku in BAD_SKUS:
    cost_pct = random.uniform(0.94, 0.99)   # bad SKUs get terrible margins
    unit_price = round(unit_price * 0.55, 2)
    quantity = random.randint(40, 100)
```

One-line if (called a ternary):
```python
label = "Bad" if sku in BAD_SKUS else "Good"
```

---

## 1.8 For Loops

Repeat code for every item in a collection.

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)
# apple
# banana
# cherry
```

Loop with index using `enumerate`:
```python
for i, fruit in enumerate(fruits):
    print(i, fruit)
# 0 apple
# 1 banana
# 2 cherry
```

Loop over a range of numbers:
```python
for i in range(5):
    print(i)    # 0, 1, 2, 3, 4

for i in range(1, 6):
    print(i)    # 1, 2, 3, 4, 5
```

In our project:
```python
# run_pipeline.py
for i, (label, script) in enumerate(STEPS, 1):
    print(f"Step {i}/{len(STEPS)} : {label}")
    ok = run(script)
```

---

## 1.9 While Loops

Repeat code as long as a condition is True.

```python
count = 0
while count < 5:
    print(count)
    count += 1   # count = count + 1
```

---

## 1.10 Functions

A reusable block of code. Define once, use many times.

```python
# Define:
def add(a, b):
    return a + b

# Call:
result = add(3, 4)   # result = 7
```

Functions with default values:
```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Haseeb")           # "Hello, Haseeb!"
greet("Haseeb", "Hi")     # "Hi, Haseeb!"
```

In our project:
```python
# generate_raw_data.py
def random_date() -> pd.Timestamp:
    delta = (DATE_END - DATE_START).days
    return DATE_START + pd.Timedelta(days=random.randint(0, delta))

# The -> pd.Timestamp is a "type hint" — it tells you what the function returns
# It's optional but good practice
```

```python
# clean_and_engineer.py
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
```

The text inside triple quotes `"""..."""` is called a **docstring** — it explains what the function does.

---

## 1.11 Try / Except (Error Handling)

Catch errors so your program doesn't crash.

```python
try:
    result = 10 / 0        # this causes a ZeroDivisionError
except ZeroDivisionError:
    result = 0             # handle it gracefully
    print("Cannot divide by zero")
```

Multiple error types:
```python
try:
    value = int("abc")     # ValueError
except (ValueError, TypeError):
    value = 0
```

In our project — the date parser:
```python
for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%d-%b-%Y", "%d/%m/%Y"):
    try:
        return pd.to_datetime(val, format=fmt)   # try this format
    except (ValueError, TypeError):
        pass    # "pass" means "do nothing, try the next one"
```

---

## 1.12 Imports

Python code is organized into **modules** (files) and **packages** (folders of files).
`import` loads external code so you can use it.

```python
import random              # import the whole module
import numpy as np         # import and give it a shorter nickname "np"
from faker import Faker    # import just one thing from a module
import pandas as pd
```

After importing:
```python
random.randint(1, 50)      # use random module's randint function
np.array([1, 2, 3])        # use numpy's array function
fake = Faker()             # create a Faker object
pd.read_csv("file.csv")    # use pandas' read_csv function
```

---

## 1.13 F-Strings (String Formatting)

The modern way to embed variables inside strings.

```python
name = "Haseeb"
rows = 10464
margin = 47.5

print(f"Hello {name}")               # Hello Haseeb
print(f"Rows: {rows:,}")            # Rows: 10,464  (comma formatting)
print(f"Margin: {margin:.2f}%")     # Margin: 47.50%
print(f"Revenue: ${rows:,.0f}")     # Revenue: $10,464
```

Format codes after `:`:
- `,` → add thousand separators
- `.2f` → 2 decimal places (float)
- `.0f` → 0 decimal places
- `d` → integer

---

## 1.14 List Comprehensions

A compact way to build a list.

```python
# Normal way:
squares = []
for i in range(5):
    squares.append(i * i)
# [0, 1, 4, 9, 16]

# List comprehension — same thing, one line:
squares = [i * i for i in range(5)]
```

With a condition:
```python
evens = [i for i in range(10) if i % 2 == 0]
# [0, 2, 4, 6, 8]
```

In our project:
```python
# generate_raw_data.py
REGULAR_SKUS = [f"SKU-{str(i).zfill(3)}" for i in range(1, 39)]
# zfill(3) pads with zeros: "1" -> "001", "12" -> "012"
# Result: ["SKU-001", "SKU-002", ..., "SKU-038"]
```

---

## 1.15 None vs NaN vs NaT

Three different ways to represent "missing" in Python + Pandas:

| Value | Meaning | Where |
|-------|---------|-------|
| `None` | Python's "nothing" | Regular Python |
| `NaN` | "Not a Number" | NumPy / Pandas for numbers |
| `NaT` | "Not a Time" | Pandas for dates |

```python
import pandas as pd
import numpy as np

pd.isna(None)    # True
pd.isna(np.nan)  # True
pd.isna(pd.NaT)  # True
pd.isna(0)       # False  (0 is a valid number, not missing)
pd.isna("")      # False  (empty string is not missing)
```

---

## 1.16 The `round()` Function

```python
round(3.14159, 2)    # 3.14
round(1234.5, 0)     # 1234.0
round(47.123)        # 47  (no decimal argument = round to integer)
```

In our project:
```python
unit_price = round(random.uniform(50, 1200), 2)   # e.g., 847.23
revenue    = round(unit_price * quantity, 2)
```

---

## 1.17 The `random` Module

```python
import random

random.random()           # random float between 0.0 and 1.0
random.uniform(10, 50)    # random float between 10 and 50
random.randint(1, 50)     # random integer between 1 and 50 (inclusive)
random.choice(["A","B","C"])  # picks one item randomly from a list
random.seed(42)           # fix the random seed — same "random" numbers every time
```

Why `seed(42)`? So that every time you run the script, you get the **same** dataset.
Without a seed, the dataset would be different every run — not reproducible.

---

## 1.18 What You Now Know

You now understand every Python syntax concept used in this project:
- Variables, data types, strings, lists, dicts
- If/elif/else, for loops
- Functions, docstrings, type hints
- Try/except error handling
- Imports
- f-strings, list comprehensions
- None/NaN/NaT, round(), random module

**Next:** Chapter 2 — NumPy and Pandas (the real data science tools).
