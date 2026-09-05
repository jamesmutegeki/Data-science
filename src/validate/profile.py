"""
Data profiler for the prices dataset.
Generates a comprehensive profile report including schema, stats, and visualizations.
"""
import pandas as pd
import matplotlib.pyplot as plt
from src.validate import rules

def profile_data(path):
    """Generate a complete profile of the dataset."""
    df = pd.read_csv(path)
    
    report = []
    report.append("=" * 60)
    report.append("DATA PROFILING REPORT")
    report.append("=" * 60)
    
    # --- Schema ---
    report.append("\n1. SCHEMA (Inferred Types)")
    report.append("-" * 40)
    schema = pd.DataFrame({
        "column": df.columns,
        "dtype": [str(df[col].dtype) for col in df.columns],
        "non_null_count": [df[col].notna().sum() for col in df.columns]
    })
    report.append(schema.to_string(index=False))
    
    # --- Row count ---
    report.append(f"\n2. ROW COUNT: {len(df)}")
    
    # --- Missing values ---
    report.append("\n3. MISSING VALUES PER COLUMN")
    report.append("-" * 40)
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        "column": missing.index,
        "missing_count": missing.values,
        "missing_pct": missing_pct.values
    })
    report.append(missing_df.to_string(index=False))
    
    # --- Duplicates ---
    report.append("\n4. DUPLICATE ANALYSIS")
    report.append("-" * 40)
    dup_ids = rules.rule_duplicate_ids(df)
    dup_rows = rules.rule_duplicate_rows(df)
    report.append(f"  Duplicate record_ids: {len(dup_ids)} rows")
    report.append(f"  Exact duplicate rows: {len(dup_rows)} rows")
    
    # --- Invalid values ---
    report.append("\n5. INVALID VALUES")
    report.append("-" * 40)
    neg_prices = rules.rule_positive_price(df)
    invalid_dates = rules.rule_valid_date(df)
    unknown_comm = rules.rule_known_commodity(df)
    missing_market = rules.rule_missing_market(df)
    
    report.append(f"  Negative prices: {len(neg_prices)} rows")
    report.append(f"  Invalid dates: {len(invalid_dates)} rows")
    report.append(f"  Unknown/inconsistent commodities: {len(unknown_comm)} rows")
    report.append(f"  Missing market values: {len(missing_market)} rows")
    
    # --- Summary statistics ---
    report.append("\n6. SUMMARY STATISTICS (Numeric Columns)")
    report.append("-" * 40)
    
    # Convert price to numeric for stats
    df["price_numeric"] = pd.to_numeric(df["price"], errors="coerce")
    df["quantity_numeric"] = pd.to_numeric(df["quantity"], errors="coerce")
    
    numeric_cols = ["price_numeric", "quantity_numeric"]
    stats = df[numeric_cols].describe().T
    stats["median"] = df[numeric_cols].median()
    report.append(stats[["count", "mean", "median", "min", "max", "std"]].to_string())
    
    # --- Commodity distribution ---
    report.append("\n7. COMMODITY VALUE COUNTS")
    report.append("-" * 40)
    report.append(df["commodity"].value_counts().to_string())
    
    # --- Market distribution ---
    report.append("\n8. MARKET VALUE COUNTS")
    report.append("-" * 40)
    report.append(df["market"].value_counts().to_string())
    
    report.append("\n" + "=" * 60)
    
    # Print report
    for line in report:
        print(line)
    
    # --- Visualization: Price histogram ---
    fig, ax = plt.subplots(figsize=(10, 6))
    df["price_numeric"].dropna().hist(bins=50, ax=ax, edgecolor='black')
    ax.set_xlabel("Price")
    ax.set_ylabel("Frequency")
    ax.set_title("Price Distribution (for outlier threshold decision)")
    plt.tight_layout()
    plt.savefig("docs/price_histogram.png", dpi=150)
    plt.close()
    print("\n[Saved: docs/price_histogram.png]")
    
    return "\n".join(report)


if __name__ == "__main__":
    profile_data("data/raw/prices.csv")
