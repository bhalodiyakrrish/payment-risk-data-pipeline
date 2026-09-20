import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "transactions.csv"
)

VALIDATION_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "validation"
    / "transaction_validation_results.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "silver"
)

OUTPUT_FILE = OUTPUT_DIR / "transactions.csv"


# ---------------------------------------------------------
# Load source data
# ---------------------------------------------------------

transactions = pd.read_csv(RAW_FILE)

validation_results = pd.read_csv(
    VALIDATION_FILE
)


# ---------------------------------------------------------
# Identify valid transaction records
# ---------------------------------------------------------

valid_transaction_ids = set(
    validation_results.loc[
        validation_results["validation_status"] == "VALID",
        "record_key"
    ]
)


# ---------------------------------------------------------
# Keep only validated transactions
# ---------------------------------------------------------

silver_transactions = transactions[
    transactions["transaction_id"].isin(valid_transaction_ids)
].copy()


# ---------------------------------------------------------
# Standardize timestamp
# ---------------------------------------------------------

silver_transactions["transaction_timestamp"] = pd.to_datetime(
    silver_transactions["transaction_timestamp"],
    errors="coerce"
)


# ---------------------------------------------------------
# Standardize amount
# ---------------------------------------------------------

silver_transactions["amount"] = pd.to_numeric(
    silver_transactions["amount"],
    errors="coerce"
).round(2)


# ---------------------------------------------------------
# Standardize response code
# ---------------------------------------------------------

silver_transactions["response_code"] = (
    silver_transactions["response_code"]
    .astype(int)
    .astype(str)
    .str.zfill(2)
)


# ---------------------------------------------------------
# Select final Silver columns
# ---------------------------------------------------------

silver_transactions = silver_transactions[
    [
        "transaction_id",
        "customer_id",
        "merchant_id",
        "transaction_timestamp",
        "amount",
        "currency",
        "payment_method",
        "transaction_status",
        "country",
        "gateway",
        "response_code",
        "device_type"
    ]
]


# ---------------------------------------------------------
# Create Silver directory
# ---------------------------------------------------------

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# Write Silver dataset
# ---------------------------------------------------------

silver_transactions.to_csv(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

print("----------------------------------------")
print("Transaction Silver Transformation")
print("----------------------------------------")

print(f"Raw records:       {len(transactions):,}")
print(f"Valid records:     {len(silver_transactions):,}")
print(f"Rejected records:  {len(transactions) - len(silver_transactions):,}")

print("\nOutput:")
print(OUTPUT_FILE)

print("\nTransformation completed successfully.")