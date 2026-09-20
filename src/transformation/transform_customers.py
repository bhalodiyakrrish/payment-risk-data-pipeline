import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "customers.csv"

VALIDATION_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "validation"
    / "customer_validation_results.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "silver"
)

OUTPUT_FILE = OUTPUT_DIR / "customers.csv"


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

customers = pd.read_csv(RAW_FILE)

validation_results = pd.read_csv(
    VALIDATION_FILE
)


# ---------------------------------------------------------
# Select valid records
# ---------------------------------------------------------

valid_customer_ids = set(
    validation_results.loc[
        validation_results["validation_status"] == "VALID",
        "record_key"
    ]
)


silver_customers = customers[
    customers["customer_id"].isin(valid_customer_ids)
].copy()


# ---------------------------------------------------------
# Standardize data types
# ---------------------------------------------------------

silver_customers["registration_date"] = pd.to_datetime(
    silver_customers["registration_date"]
).dt.date


# ---------------------------------------------------------
# Select final Silver columns
# ---------------------------------------------------------

silver_customers = silver_customers[
    [
        "customer_id",
        "customer_name",
        "customer_email",
        "country",
        "registration_date",
        "customer_status"
    ]
]


# ---------------------------------------------------------
# Create output directory
# ---------------------------------------------------------

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# Write Silver dataset
# ---------------------------------------------------------

silver_customers.to_csv(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

print("----------------------------------------")
print("Customer Silver Transformation")
print("----------------------------------------")

print(f"Raw records:       {len(customers):,}")
print(f"Valid records:     {len(silver_customers):,}")
print(f"Rejected records:  {len(customers) - len(silver_customers):,}")

print("\nOutput:")
print(OUTPUT_FILE)

print("\nTransformation completed successfully.")