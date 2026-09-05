# DSC3103 - Data Science Lab 02

## Data Profiler and Cleaner

Build a Data Profiler and Cleaner for the synthetic dataset.

## Project Structure

```
Lab1/
├── .gitignore                    # Git ignore patterns
├── README.md                     # This file
├── Lab_02.ipynb                  # Lab instructions
├── generate_messy_prices.py      # Step 1: Generates 1019 messy rows
├── check.py                      # Step 3: Tests all validation rules
├── src/
│   ├── __init__.py               # Package marker
│   ├── validate/
│   │   ├── __init__.py          # Validate package marker
│   │   ├── rules.py             # Step 3: 6 validation rules
│   │   └── profile.py           # Step 4: Data profiler
│   └── transform/
│       └── clean.py              # Step 5: Data cleaner
├── data/
│   ├── raw/
│   │   └── prices.csv          # Raw messy data (1019 rows)
│   └── processed/
│       ├── prices_clean.parquet  # Cleaned output
│       └── cleaning_log.md      # Decision log
├── docs/
│   ├── validation_report.md      # Step 7: Validation results
│   ├── lab_02_notes.md          # Step 7: Reflection notes
│   ├── price_histogram.png      # Step 4: Price distribution chart
│   └── Lab02_Code_Explanation.pdf # Code explanation
└── .venv/                       # Virtual environment (not committed)
```

## How to Run

### Step 1: Generate messy data
```bash
python generate_messy_prices.py
```

### Step 2: Test validation rules
```bash
python check.py
```

### Step 3: Profile the data
```bash
python -m src.validate.profile
```

### Step 4: Clean the data
```bash
python -m src.transform.clean
```

## Data Quality Issues Introduced

The generator creates 1019 rows with exactly 1000 unique rows and 19 duplicate rows:

- **Negative prices** - ~3% of rows have negative price values
- **Duplicate record_ids** - 19 rows share record_ids with other rows
- **Exact duplicate rows** - 19 rows are exact duplicates
- **Invalid dates** - ~3% have impossible dates like "2020-14-50"
- **Missing market values** - ~3% have empty market field
- **Inconsistent commodity casing** - ~10% have "MAIZE", "maize", "Maize ", etc.

## Validation Rules (Step 3)

Each rule is implemented in `src/validate/rules.py`:

| Rule | Function | Action |
|------|----------|--------|
| 1 | `rule_positive_price(df)` | REJECT rows with price <= 0 |
| 2 | `rule_duplicate_ids(df)` | REJECT duplicate record_ids (keep first) |
| 3 | `rule_duplicate_rows(df)` | REJECT exact duplicate rows |
| 4 | `rule_valid_date(df)` | REJECT invalid date formats |
| 5 | `rule_missing_market(df)` | REJECT rows with empty market |
| 6 | `rule_known_commodity(df)` | NORMALIZE to title-case |

## Profiler Output (Step 4)

The profiler in `src/validate/profile.py` reports:
- Inferred schema (column names and types)
- Row count: 1019 total
- Missing-value counts per column
- Duplicate counts (exact-row and by record_id)
- Invalid values per rule
- Summary statistics (mean, median, min, max, std)
- Price histogram saved to `docs/price_histogram.png`

## Cleaner Output (Step 5)

The cleaner in `src/transform/clean.py` produces:
- `data/processed/prices_clean.parquet` - Cleaned dataset
- `data/processed/cleaning_log.md` - Every decision logged with record_id, field, old value, new value, reason

## Step 6: Raw File Preservation

The raw file `data/raw/prices.csv` is NEVER modified by cleaning scripts. Hash verification confirms integrity before and after.

## Step 7: Deliverables

| File | Purpose |
|------|---------|
| `docs/validation_report.md` | What was checked, failures per rule, actions taken |
| `docs/lab_02_notes.md` | 3-4 sentence reflection on cleaning decisions |

## Step 8: Git Commits (5+ Required)

All code and data committed with meaningful messages:
1. Generator + raw data
2. Validation rules + checker
3. Profiler + chart
4. Cleaner + processed output
5. Validation report + notes
6. README + documentation
