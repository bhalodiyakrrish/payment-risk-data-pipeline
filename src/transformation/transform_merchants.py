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
    / "merchants.csv"
)

VALIDATION_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "validation"
    / "merchant_validation_results.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "silver"
)

OUTPUT_FILE = OUTPUT_DIR / "merchants.csv"


# ---------------------------------------------------------
# Load source data
# ---------------------------------------------------------

merchants = pd.read_csv(RAW_FILE)

validation_results = pd.read_csv(
    VALIDATION_FILE
)


# ---------------------------------------------------------
# Identify valid merchant records
# ---------------------------------------------------------

valid_merchant_ids = set(
    validation_results.loc[
        validation_results["validation_status"] == "VALID",
        "record_key"
    ]
)


# ---------------------------------------------------------
# Keep only validated records
# ---------------------------------------------------------

silver_merchants = merchants[
    merchants["merchant_id"].isin(valid_merchant_ids)
].copy()


# ---------------------------------------------------------
# Standardize data types
# ---------------------------------------------------------

silver_merchants["onboarding_date"] = pd.to_datetime(
    silver_merchants["onboarding_date"]
).dt.date


# ---------------------------------------------------------
# Select final Silver columns
# ---------------------------------------------------------

silver_merchants = silver_merchants[
    [
        "merchant_id",
        "merchant_name",
        "merchant_category",
        "country",
        "onboarding_date",
        "merchant_status"
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

silver_merchants.to_csv(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

print("----------------------------------------")
print("Merchant Silver Transformation")
print("----------------------------------------")

print(f"Raw records:       {len(merchants):,}")
print(f"Valid records:     {len(silver_merchants):,}")
print(f"Rejected records:  {len(merchants) - len(silver_merchants):,}")

print("\nOutput:")
print(OUTPUT_FILE)

print("\nTransformation completed successfully.")