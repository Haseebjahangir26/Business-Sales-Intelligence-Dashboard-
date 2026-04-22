# Contributing

Thank you for considering contributing to this project!

## How to Contribute

### 1. Fork & Clone
```bash
git clone https://github.com/YOUR_USERNAME/business-sales-intelligence-dashboard.git
cd business-sales-intelligence-dashboard
```

### 2. Set Up Environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the Pipeline First
Make sure everything works before making changes:
```bash
python run_pipeline.py
```

### 4. Make Your Changes
- Keep code in `src/` for pipeline scripts
- Use `notebooks/` for exploratory analysis
- Follow existing code style (no magic numbers, clear variable names)

### 5. Commit Convention
Use [Conventional Commits](https://www.conventionalcommits.org/):
```
feat: add new chart for seasonal trends
fix: handle empty customer_name edge case
docs: update Power BI setup guide
refactor: extract date parser into utils.py
```

### 6. Open a Pull Request
- Describe what changed and why
- Include before/after screenshots for any chart changes

## Coding Standards
- Python: PEP 8 compliant
- Max line length: 100 characters
- All functions must have a docstring
- No hardcoded file paths — use `pathlib.Path` or relative paths from project root

## Reporting Issues
Open a GitHub Issue with:
1. What you expected to happen
2. What actually happened
3. Your Python version (`python --version`)
4. The full error traceback
