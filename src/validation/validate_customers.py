import pandas as pd
from pathlib import Path
import re


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "customers.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "validation"
)


SUPPORTED_COUNTRIES = {
    "IN",
    "AE",
    "SA",
    "US",
    "GB"
}

SUPPORTED_STATUSES = {
    "ACTIVE",
    "INACTIVE",
    "SUSPENDED"
}


# ============================================================
# EMAIL VALIDATION
# ============================================================

def is_valid_email(email):
    """
    Basic email format validation.

    This is intended for data-quality validation,
    not full RFC email validation.
    """

    if pd.isna(email):
        return False

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return bool(
        re.match(pattern, str(email))
    )


# ============================================================
# CUSTOMER VALIDATION
# ============================================================

def validate_customers(df):

    validation_results = []
    validation_errors = []

    for index, row in df.iterrows():

        customer_id = row["customer_id"]

        errors = []

        # ----------------------------------------------------
        # CUST-DQ-001
        # Customer ID must not be NULL/empty
        # ----------------------------------------------------

        if pd.isna(customer_id) or str(customer_id).strip() == "":

            errors.append({
                "record_key": customer_id,
                "error_code": "CUST_MISSING_ID",
                "severity": "Critical",
                "error_message": "Customer ID is missing"
            })

        # ----------------------------------------------------
        # CUST-DQ-003
        # Customer name must not be NULL/empty
        # ----------------------------------------------------

        if (
            pd.isna(row["customer_name"])
            or str(row["customer_name"]).strip() == ""
        ):

            errors.append({
                "record_key": customer_id,
                "error_code": "CUST_MISSING_NAME",
                "severity": "High",
                "error_message": "Customer name is missing"
            })

        # ----------------------------------------------------
        # CUST-DQ-004
        # Customer email must not be NULL/empty
        # ----------------------------------------------------

        if (
            pd.isna(row["customer_email"])
            or str(row["customer_email"]).strip() == ""
        ):

            errors.append({
                "record_key": customer_id,
                "error_code": "CUST_MISSING_EMAIL",
                "severity": "High",
                "error_message": "Customer email is missing"
            })

        # ----------------------------------------------------
        # CUST-DQ-005
        # Email format
        # ----------------------------------------------------

        elif not is_valid_email(
            row["customer_email"]
        ):

            errors.append({
                "record_key": customer_id,
                "error_code": "CUST_INVALID_EMAIL",
                "severity": "Medium",
                "error_message": "Customer email format is invalid"
            })

        # ----------------------------------------------------
        # CUST-DQ-006
        # Country
        # ----------------------------------------------------

        if row["country"] not in SUPPORTED_COUNTRIES:

            errors.append({
                "record_key": customer_id,
                "error_code": "CUST_INVALID_COUNTRY",
                "severity": "High",
                "error_message": "Customer country is unsupported"
            })

        # ----------------------------------------------------
        # CUST-DQ-007
        # Registration date
        # ----------------------------------------------------

        registration_date = pd.to_datetime(
            row["registration_date"],
            errors="coerce"
        )

        if pd.isna(registration_date):

            errors.append({
                "record_key": customer_id,
                "error_code": "CUST_INVALID_DATE",
                "severity": "High",
                "error_message": "Registration date is invalid"
            })

        # ----------------------------------------------------
        # CUST-DQ-008
        # Customer status
        # ----------------------------------------------------

        if row["customer_status"] not in SUPPORTED_STATUSES:

            errors.append({
                "record_key": customer_id,
                "error_code": "CUST_INVALID_STATUS",
                "severity": "High",
                "error_message": "Customer status is unsupported"
            })

        # ----------------------------------------------------
        # Validation result
        # ----------------------------------------------------

        validation_status = (
            "VALID"
            if len(errors) == 0
            else "REJECTED"
        )

        validation_results.append({
            "record_key": customer_id,
            "validation_status": validation_status
        })

        validation_errors.extend(errors)

    return (
        pd.DataFrame(validation_results),
        pd.DataFrame(validation_errors)
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("Loading customer source data...")

    df = pd.read_csv(
        INPUT_FILE
    )

    print(
        f"Records loaded: {len(df):,}"
    )

    print("Running customer validation...")

    results, errors = validate_customers(df)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    results.to_csv(
        OUTPUT_DIR / "customer_validation_results.csv",
        index=False
    )

    errors.to_csv(
        OUTPUT_DIR / "customer_validation_errors.csv",
        index=False
    )

    print()
    print("Validation completed.")
    print(
        f"Valid records: "
        f"{(results['validation_status'] == 'VALID').sum():,}"
    )

    print(
        f"Rejected records: "
        f"{(results['validation_status'] == 'REJECTED').sum():,}"
    )

    print(
        f"Validation errors: "
        f"{len(errors):,}"
    )


if __name__ == "__main__":
    main()