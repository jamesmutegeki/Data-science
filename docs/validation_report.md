# Data Validation Report

## Overview

This report documents the validation rules applied to `data/raw/prices.csv` and the cleaning actions taken to address data quality issues.

## Validation Rules Tested

| Rule | Description | Rows Failed | Action Taken |
|------|-------------|-------------|--------------|
| `rule_positive_price` | Checks for negative or zero prices | 26 | REJECT - removed rows |
| `rule_duplicate_ids` | Checks for duplicate `record_id` values | 38 | REJECT - kept first occurrence |
| `rule_duplicate_rows` | Checks for exact duplicate rows | 38 | REJECT - removed duplicates |
| `rule_valid_date` | Checks for invalid date formats (YYYY-MM-DD) | 47 | REJECT - removed invalid rows |
| `rule_missing_market` | Checks for missing/empty market values | 21 | REJECT - removed rows |
| `rule_known_commodity` | Checks for inconsistent commodity casing | 69 | NORMALIZE - converted to title-case |

## Dataset Summary

- **Original row count:** 1019
- **Total rows removed:** 132 (negative prices + invalid dates + missing markets + duplicates)
- **Rows normalized:** 69 (commodity casing)
- **Final row count after cleaning:** ~887

## Actions Defined

| Action | Description | Rules Used |
|--------|-------------|------------|
| **REJECT** | Rows failing this rule were removed from the dataset | positive_price, valid_date, missing_market |
| **REMOVE** | Exact duplicates and duplicate IDs were deleted | duplicate_ids, duplicate_rows |
| **NORMALIZE** | Values were standardized to title-case | known_commodity |
| **IMPUTE** | Not used - all issues were data errors, not missing values | N/A |

## Data Quality Issues Found

### 1. Negative Prices (26 rows)
```
record_id: 13, 26, 30, 70, 92, ...
Examples: -46.53, -31.44, -38.78, -23.07, -41.67
Action: REJECT - Prices must be > 0 for valid market data
```

### 2. Duplicate record_ids (38 rows, 19 pairs)
```
19 record_ids appear twice each
Examples: 54, 62, 99, 124, 297, ...
Action: REJECT duplicates, keep first occurrence
```

### 3. Exact Duplicate Rows (38 rows)
```
Rows that are 100% identical across all columns
Action: REJECT duplicates, keep first occurrence
```

### 4. Invalid Dates (47 rows)
```
- 19 rows with NaN (empty date field)
- 28 rows with impossible dates like "2020-14-50"
Action: REJECT - Dates must be valid YYYY-MM-DD format
```

### 5. Missing Market Values (21 rows)
```
Empty/null market field
Action: REJECT - Market name is required
```

### 6. Inconsistent Commodity Casing (69 rows)
```
Examples: "wheat" → "Wheat", "RICE" → "Rice", "COFFEE" → "Coffee"
Action: NORMALIZE - Convert to title-case ("Maize", "Beans", etc.)
```

## Cleaning Log

Detailed cleaning decisions are logged in `data/processed/cleaning_log.md` with:
- record_id
- Field changed
- Old value
- New value
- Reason/Rule

## Files Generated

| File | Description |
|------|-------------|
| `data/processed/prices_clean.parquet` | Cleaned dataset after all transformations |
| `data/processed/cleaning_log.md` | Complete audit trail of all decisions |
| `docs/price_histogram.png` | Price distribution visualization |

## Raw File Preservation

The raw file `data/raw/prices.csv` was **NOT modified** by the cleaning process. Hash verification confirms integrity before and after cleaning.
