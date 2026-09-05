# Data Cleaning Log

## Original row count: 1019
## Raw file hash: 87bd8925b3c62702a5786e77403c817d

## Duplicate Rows: 38 found
- Action: REJECT (remove all duplicate rows)
- Reason: Exact duplicates provide no new information

- Result: Removed 19 rows

## Invalid Dates: 45 found
- Action: REJECT (remove rows with invalid dates)
- Reason: Cannot be reasonably imputed; invalid dates are data errors

- Result: Removed 45 rows

## Negative Prices: 25 found
- Action: REJECT (remove rows with negative prices)
- Reason: Prices cannot be negative in real-world context

- Result: Removed 44 rows

## Missing Market Values: 18 found
- Action: REJECT (remove rows with missing market)
- Reason: Market is essential for analysis; cannot impute reliably

- Result: Removed 18 rows

## Inconsistent Commodity Casing: 63 found
- Action: NORMALIZE (convert to title-case)
- Reason: 'Maize', 'MAIZE', 'maize' all mean the same thing

- Mapping applied: 63 rows normalized


## Summary
- Original rows: 1019
- Final rows: 893
- Rows removed: 126
- Raw file hash after: 87bd8925b3c62702a5786e77403c817d