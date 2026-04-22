"""
run_pipeline.py
───────────────
Master runner — executes the full pipeline in order:

  Step 1  →  Generate raw messy data   (data/raw/)
  Step 2  →  Clean + feature engineer  (data/processed/)
  Step 3  →  EDA charts                (reports/figures/)
  Step 4  →  HTML executive report     (reports/)

Usage:
  python run_pipeline.py
"""

import subprocess, sys, time, os

STEPS = [
    ("Generating raw data",            "data/raw/generate_raw_data.py"),
    ("Cleaning & engineering features", "src/clean_and_engineer.py"),
    ("Building EDA charts",            "src/eda_and_charts.py"),
    ("Writing HTML report",            "src/generate_report.py"),
]

def run(script: str) -> bool:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    result = subprocess.run(
        [sys.executable, script],
        capture_output=True, text=True, encoding="utf-8", env=env,
    )
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
    return result.returncode == 0

if __name__ == "__main__":
    total_start = time.time()
    for i, (label, script) in enumerate(STEPS, 1):
        print(f"\n{'-'*55}")
        print(f"  Step {i}/{len(STEPS)}  :  {label}")
        print(f"{'-'*55}")
        ok = run(script)
        if not ok:
            print(f"\n[ERROR] Pipeline failed at step {i}. Aborting.")
            sys.exit(1)

    elapsed = time.time() - total_start
    print(f"\n{'='*55}")
    print(f"  Pipeline complete in {elapsed:.1f}s")
    print(f"  Report  ->  reports/sales_intelligence_report.html")
    print(f"  Charts  ->  reports/figures/")
    print(f"  Data    ->  data/processed/")
    print(f"{'='*55}\n")
