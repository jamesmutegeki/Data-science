import pandas as pd
from datetime import datetime

# Known vald commodities (normalized)
VALID_COMMODITIES = {"Maize", "Beans", "Rice", "Wheat", "Coffee", "Tea"}

def rule_positive_price(df):
    # Handle both numeric and string prices
    df_temp = df.copy()
    # Convert to numeric, non-numeric become NaN
    df_temp["price_numeric"] = pd.to_numeric(df_temp["price"], errors="coerce")
    # Find negative prices
    neg_prices = df_temp[df_temp["price_numeric"] < 0].copy()
    neg_prices["Reason"] = "Negative Price"
    return neg_prices[["record_id", "price", "Reason"]]

def rule_duplicate_ids(df):
    # Fnd record_ids that apear more than once
    dup_mask = df.duplicated(subset=["record_id"], keep=False)
    dup_ids = df[dup_mask].copy()
    dup_ids["Reason"] = "Duplicate record_id"
    # Add count of how many times this id appears
    id_counts = df["record_id"].value_counts()
    dup_ids["id_count"] = dup_ids["record_id"].map(id_counts)
    return dup_ids[["record_id", "Reason", "id_count"]]

def rule_duplicate_rows(df):
    # Find fully duplicate rows 
    dup_mask = df.duplicated(keep=False)
    dup_rows = df[dup_mask].copy()
    dup_rows["Reason"] = "Duplicate Row"
    return dup_rows

def rule_valid_date(df):
    def is_valid_date(date_str):
        if pd.isna(date_str) or date_str == "":
            return False
        try:
            datetime.strptime(str(date_str), "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    invalid_dates = df[~df["date"].apply(is_valid_date)].copy()
    invalid_dates["Reason"] = "Invalid Date"
    return invalid_dates[["record_id", "date", "Reason"]]

def rule_missing_market(df):
    missing_market = df[
        df["market"].isna() | 
        (df["market"].astype(str).str.strip() == "")
    ].copy()
    missing_market["Reason"] = "Missing Market Value"
    return missing_market[["record_id", "market", "Reason"]]

def rule_known_commodity(df):
    def normalize_commodity(commodity):
        if pd.isna(commodity) or commodity == "":
            return None
        return str(commodity).strip().title()
    
    df_temp = df.copy()
    df_temp["normalized_commodity"] = df_temp["commodity"].apply(normalize_commodity)
    
    # Find commodities where original doesn't match canonical frm
    inconsistent_mask = df_temp["commodity"].astype(str).str.strip() != df_temp["normalized_commodity"]
    inconsistent_commodities = df_temp[inconsistent_mask].copy()
    inconsistent_commodities["Reason"] = "Inconsistent Casing"
    inconsistent_commodities["original_commodity"] = inconsistent_commodities["commodity"]
    
    return inconsistent_commodities[["record_id", "commodity", "normalized_commodity", "Reason"]]
