import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "merchants.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "validation"
)


# ============================================================
# REFERENCE VALUES
# ============================================================

SUPPORTED_COUNTRIES = {
    "IN",
    "AE",
    "SA",
    "US",
    "GB"
}

SUPPORTED_CATEGORIES = {
    "RETAIL",
    "FOOD",
    "TRAVEL",
    "ENTERTAINMENT",
    "HEALTHCARE",
    "EDUCATION",
    "SERVICES"
}

SUPPORTED_STATUSES = {
    "ACTIVE",
    "INACTIVE",
    "SUSPENDED"
}


# ============================================================
# MERCHANT VALIDATION
# ============================================================

def validate_merchants(df):

    validation_results = []
    validation_errors = []

    for index, row in df.iterrows():

        merchant_id = row["merchant_id"]

        errors = []

        # ----------------------------------------------------
        # MER-DQ-001
        # Merchant ID must not be missing
        # ----------------------------------------------------

        if (
            pd.isna(merchant_id)
            or str(merchant_id).strip() == ""
        ):

            errors.append({
                "record_key": merchant_id,
                "error_code": "MER_MISSING_ID",
                "severity": "Critical",
                "error_message": "Merchant ID is missing"
            })

        # ----------------------------------------------------
        # MER-DQ-003
        # Merchant name must not be missing
        # ----------------------------------------------------

        if (
            pd.isna(row["merchant_name"])
            or str(row["merchant_name"]).strip() == ""
        ):

            errors.append({
                "record_key": merchant_id,
                "error_code": "MER_MISSING_NAME",
                "severity": "High",
                "error_message": "Merchant name is missing"
            })

        # ----------------------------------------------------
        # MER-DQ-004
        # Merchant category must not be missing
        # ----------------------------------------------------

        if (
            pd.isna(row["merchant_category"])
            or str(row["merchant_category"]).strip() == ""
        ):

            errors.append({
                "record_key": merchant_id,
                "error_code": "MER_MISSING_CATEGORY",
                "severity": "High",
                "error_message": "Merchant category is missing"
            })

        # ----------------------------------------------------
        # MER-DQ-005
        # Merchant category must be valid
        # ----------------------------------------------------

        elif row["merchant_category"] not in SUPPORTED_CATEGORIES:

            errors.append({
                "record_key": merchant_id,
                "error_code": "MER_INVALID_CATEGORY",
                "severity": "High",
                "error_message": "Merchant category is unsupported"
            })

        # ----------------------------------------------------
        # MER-DQ-006
        # Country must be valid
        # ----------------------------------------------------

        if row["country"] not in SUPPORTED_COUNTRIES:

            errors.append({
                "record_key": merchant_id,
                "error_code": "MER_INVALID_COUNTRY",
                "severity": "High",
                "error_message": "Merchant country is unsupported"
            })

        # ----------------------------------------------------
        # MER-DQ-007
        # Onboarding date must be valid
        # ----------------------------------------------------

        onboarding_date = pd.to_datetime(
            row["onboarding_date"],
            errors="coerce"
        )

        if pd.isna(onboarding_date):

            errors.append({
                "record_key": merchant_id,
                "error_code": "MER_INVALID_DATE",
                "severity": "High",
                "error_message": "Merchant onboarding date is invalid"
            })

        # ----------------------------------------------------
        # MER-DQ-008
        # Merchant status must be valid
        # ----------------------------------------------------

        if row["merchant_status"] not in SUPPORTED_STATUSES:

            errors.append({
                "record_key": merchant_id,
                "error_code": "MER_INVALID_STATUS",
                "severity": "High",
                "error_message": "Merchant status is unsupported"
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
            "record_key": merchant_id,
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

    print("Loading merchant source data...")

    df = pd.read_csv(
        INPUT_FILE
    )

    print(
        f"Records loaded: {len(df):,}"
    )

    print("Running merchant validation...")

    results, errors = validate_merchants(df)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    results.to_csv(
        OUTPUT_DIR / "merchant_validation_results.csv",
        index=False
    )

    errors.to_csv(
        OUTPUT_DIR / "merchant_validation_errors.csv",
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