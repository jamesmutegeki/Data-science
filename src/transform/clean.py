import pandas as pd
import hashlib
import os
from src.validate import rules

raw_path = "data/raw/prices.csv"
processed_path = "data/processed/prices_clean.parquet"
log_path = "data/processed/cleaning_log.md"

# Known valid commodities
VALID_COMMODITIES = {"Maize", "Beans", "Rice", "Wheat", "Coffee", "Tea"}

def get_file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def clean_data(raw_path, processed_path):
    # VERIFY RAW FILE HASH BEFORE ANYTHING
    hash_before = get_file_hash(raw_path)
    print(f"[VERIFY] Raw file hash before cleaning: {hash_before}")
    
    df = pd.read_csv(raw_path)
    original_count = len(df)
    
    # Create a log of all decisions
    log = []
    log.append("# Data Cleaning Log\n")
    log.append(f"## Original row count: {original_count}")
    log.append(f"## Raw file hash: {hash_before}\n")
    
    # 1: Duplicate Rows — REJECT (remove entirely)
    # -----------------------------------------------------------
    dup_rows = rules.rule_duplicate_rows(df)
    if len(dup_rows) > 0:
        log.append(f"## Duplicate Rows: {len(dup_rows)} found")
        log.append(f"- Action: REJECT (remove all duplicate rows)")
        log.append(f"- Reason: Exact duplicates provide no new information\n")
        before = len(df)
        df = df.drop_duplicates(keep="first")
        log.append(f"- Result: Removed {before - len(df)} rows\n")
    
    # 2: Duplcate IDs — REJECT but keep first occurrence
    # -----------------------------------------------------------
    dup_ids = rules.rule_duplicate_ids(df)
    if len(dup_ids) > 0:
        log.append(f"## Duplicate record_ids: {len(dup_ids)} found")
        log.append(f"- Action: REJECT (keep first occurrence only)")
        log.append(f"- Reason: Duplicate IDs indicate data integrity issues\n")
        before = len(df)
        df = df.drop_duplicates(subset=["record_id"], keep="first")
        log.append(f"- Result: Removed {before - len(df)} rows\n")
    
    # 3: Invalid Dates — REJECT
    # -----------------------------------------------------------
    invalid_dates = rules.rule_valid_date(df)
    if len(invalid_dates) > 0:
        log.append(f"## Invalid Dates: {len(invalid_dates)} found")
        log.append(f"- Action: REJECT (remove rows with invalid dates)")
        log.append(f"- Reason: Cannot be reasonably imputed; invalid dates are data errors\n")
        before = len(df)
        df = df[df["date"].apply(is_valid_date)]
        log.append(f"- Result: Removed {before - len(df)} rows\n")
    
    # 4: Negtive Prices — REJECT
    # -----------------------------------------------------------
    neg_prices = rules.rule_positive_price(df)
    if len(neg_prices) > 0:
        log.append(f"## Negative Prices: {len(neg_prices)} found")
        log.append(f"- Action: REJECT (remove rows with negative prices)")
        log.append(f"- Reason: Prices cannot be negative in real-world context\n")
        before = len(df)
        df["price_numeric"] = pd.to_numeric(df["price"], errors="coerce")
        df = df[df["price_numeric"] >= 0]
        log.append(f"- Result: Removed {before - len(df)} rows\n")
    
    # 5: Missing Market Values — REJECT
    # -----------------------------------------------------------
    missing_market = rules.rule_missing_market(df)
    if len(missing_market) > 0:
        log.append(f"## Missing Market Values: {len(missing_market)} found")
        log.append(f"- Action: REJECT (remove rows with missing market)")
        log.append(f"- Reason: Market is essential for analysis; cannot impute reliably\n")
        before = len(df)
        df = df[df["market"].notna() & (df["market"].astype(str).str.strip() != "")]
        log.append(f"- Result: Removed {before - len(df)} rows\n")
      
    # 6: Inconsistent Commodity Casing — NORMALIZE
    # -----------------------------------------------------------
    unknown_comm = rules.rule_known_commodity(df)
    if len(unknown_comm) > 0:
        log.append(f"## Inconsistent Commodity Casing: {len(unknown_comm)} found")
        log.append(f"- Action: NORMALIZE (convert to title-case)")
        log.append(f"- Reason: 'Maize', 'MAIZE', 'maize' all mean the same thing\n")
        log.append(f"- Mapping applied: {len(unknown_comm)} rows normalized\n")
        df["commodity"] = df["commodity"].str.strip().str.title()
    
    # ----------------------------------------------------------------


    df = df.drop(columns=["price_numeric"], errors="ignore")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    
    # Save cleaned data
    df.to_parquet(processed_path, index=False)
    
    # VERIFY RAW FILE HASH AFTER
    hash_after = get_file_hash(raw_path)
    print(f"[VERIFY] Raw file hash after cleaning: {hash_after}")
    
    if hash_before == hash_after:
        print("[VERIFY] Raw file UNCHANGED — verification passed!")
    else:
        print("[WARNING] Raw file was modified!")
    
    # Save log
    log.append(f"\n## Summary")
    log.append(f"- Original rows: {original_count}")
    log.append(f"- Final rows: {len(df)}")
    log.append(f"- Rows removed: {original_count - len(df)}")
    log.append(f"- Raw file hash after: {hash_after}")
    
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "w") as f:
        f.write("\n".join(log))
    print(f"[LOG] Saved cleaning log to: {log_path}")
    print(f"[SUCCESS] Cleaned data saved to: {processed_path}")
    
    return df, log


def is_valid_date(date_str):
    """Check if date string is valid YYYY-MM-DD."""
    from datetime import datetime
    if pd.isna(date_str) or date_str == "":
        return False
    try:
        datetime.strptime(str(date_str), "%Y-%m-%d")
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    clean_data(raw_path, processed_path)
