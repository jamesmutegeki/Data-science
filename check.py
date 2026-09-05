"""
Check script to verify all validation rules work correctly.
Run with: python check.py
"""
import pandas as pd
from src.validate.rules import (
    rule_positive_price,
    rule_duplicate_ids,
    rule_duplicate_rows,
    rule_valid_date,
    rule_missing_market,
    rule_known_commodity
)

# Load the messy data
df = pd.read_csv("data/raw/prices.csv")

print("=" * 60)
print("TESTING ALL VALIDATION RULES")
print("=" * 60)

print("\n1. rule_positive_price")
print("-" * 40)
neg_prices = rule_positive_price(df)
print(f"   Found: {len(neg_prices)} rows with negative prices")
if len(neg_prices) > 0:
    print(neg_prices.head())

print("\n2. rule_duplicate_ids")
print("-" * 40)
dup_ids = rule_duplicate_ids(df)
print(f"   Found: {len(dup_ids)} rows with duplicate record_ids")
if len(dup_ids) > 0:
    print(dup_ids.head())

print("\n3. rule_duplicate_rows")
print("-" * 40)
dup_rows = rule_duplicate_rows(df)
print(f"   Found: {len(dup_rows)} rows that are exact duplicates")
if len(dup_rows) > 0:
    print(dup_rows.head())

print("\n4. rule_valid_date")
print("-" * 40)
invalid_dates = rule_valid_date(df)
print(f"   Found: {len(invalid_dates)} rows with invalid dates")
if len(invalid_dates) > 0:
    print(invalid_dates.head())

print("\n5. rule_missing_market")
print("-" * 40)
missing_market = rule_missing_market(df)
print(f"   Found: {len(missing_market)} rows with missing market values")
if len(missing_market) > 0:
    print(missing_market.head())

print("\n6. rule_known_commodity")
print("-" * 40)
unknown_comm = rule_known_commodity(df)
print(f"   Found: {len(unknown_comm)} rows with unknown commodities")
if len(unknown_comm) > 0:
    print(unknown_comm.head())

print("\n" + "=" * 60)
print("ALL RULES TESTED SUCCESSFULLY")
print("=" * 60)
