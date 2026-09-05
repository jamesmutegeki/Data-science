# Lab 02 Notes

## Summary of Changes

We cleaned the `prices.csv` dataset by applying six validation rules. For duplicate rows and duplicate IDs, we **rejected** the redundant entries (keeping only the first occurrence) because duplicates provide no new information and distort analysis. Invalid dates and negative prices were **rejected** because they represent genuine data entry errors that cannot be meaningfully imputed. Missing market values were **rejected** since market identification is essential for downstream analysis and cannot be reasonably guessed. Inconsistent commodity casing (e.g., "MAIZE", "maize") was **normalized** to title-case ("Maize") since these all represent the same commodity—normalization preserves data while standardizing format.

## Outliers vs. Errors

We distinguished outliers from errors based on whether a value could plausibly occur in reality. Negative prices are clearly **errors** (prices cannot be negative in any real market context). Extremely high or low prices that still fall within a plausible range were treated as potential **outliers** but were not automatically removed—instead, they were flagged for manual review if they exceeded domain knowledge thresholds (e.g., a price 10x above the median).

## Leakage Considerations

If this cleaned dataset were used for prediction, **leakage** would occur if:
1. The `record_id` (which encodes sequential generation order) were used as a feature, as it indirectly reveals the data generation process
2. Duplicate rows were left in the training set, causing the model to memorize and overfit to repeated observations
3. Future information (e.g., knowing which prices were "errors") were used to selectively clean only the test set, giving artificially inflated performance metrics
