"""
Generate messy prices.csv with deliberate data quality issues:
- Negative prices
- Duplicate record_ids
- Duplicate rows
- Invalid dates
- Missing market values
- Inconsistent commodity spellings
"""
import csv
import random
from datetime import datetime, timedelta
import os

random.seed(42)
base_date = datetime(2020, 1, 1)

COMMODITIES = ["Maize", "Beans", "Rice", "Wheat", "Coffee", "Tea"]
MARKETS = ["Central Market", "East Side Market", "West End Market", "North Market"]

def random_date():
    return (base_date + timedelta(days=random.randint(0, 1000))).strftime("%Y-%m-%d")

def generate_row(record_id):
    commodity = random.choice(COMMODITIES)
    if random.random() < 0.1:
        case_style = random.choice(["upper", "lower", "trailing_space"])
        if case_style == "upper":
            commodity = commodity.upper()
        elif case_style == "lower":
            commodity = commodity.lower()
        elif case_style == "trailing_space":
            commodity = commodity + " "

    market = random.choice(MARKETS)

    price_choice = random.random()
    if price_choice < 0.03:
        price = -abs(random.uniform(1, 50))
    elif price_choice < 0.06:
        price = ""
    else:
        price = round(random.uniform(5, 100), 2)

    quantity = random.randint(1, 100) if random.random() > 0.02 else ""

    if random.random() < 0.03:
        date = "2020-14-50"
    elif random.random() < 0.02:
        date = ""
    else:
        date = random_date()

    market = market if random.random() > 0.03 else ""

    return {
        "record_id": record_id,
        "date": date,
        "commodity": commodity,
        "market": market,
        "price": price,
        "quantity": quantity
    }

def generate_dataset(num_unique=1000, num_duplicate_ids=19):
    """
    Generate dataset with:
    - num_unique: unique rows with unique record_ids
    - num_duplicate_ids: extra rows that copy existing record_ids
    """
    rows = []

    # Create 1000 unique rows with unique record_ids [0-999]
    for i in range(num_unique):
        row = generate_row(i)
        rows.append(row)

    # Create 19 duplicate rows by copying existing rows
    # These will have record_ids that already exist
    for _ in range(num_duplicate_ids):
        template = random.choice(rows[:num_unique])
        dup_row = dict(template)
        # Keep the SAME record_id as the template (creates duplicate ID)
        dup_row["record_id"] = template["record_id"]
        rows.append(dup_row)

    return rows

def main():
    os.makedirs("data/raw", exist_ok=True)

    # 1000 unique rows + 19 duplicate rows = 1019 total
    rows = generate_dataset(1000, 19)

    fieldnames = ["record_id", "date", "commodity", "market", "price", "quantity"]
    output_path = "data/raw/prices.csv"

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    unique_ids = len(set(r["record_id"] for r in rows))
    print(f"Generated {len(rows)} rows in {output_path}")
    print(f"Unique record_ids: {unique_ids}")
    print(f"Duplicate record_ids: {len(rows) - unique_ids}")
    print(f"Issues introduced:")
    print("  - Negative prices")
    print("  - Duplicate record_ids (19 extra copies of existing IDs)")
    print("  - Invalid dates (2020-14-50)")
    print("  - Missing market values")
    print("  - Inconsistent commodity casing")

if __name__ == "__main__":
    main()
