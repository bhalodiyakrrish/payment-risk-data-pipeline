import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

TRANSACTIONS_FILE = PROJECT_ROOT / "data" / "raw" / "transactions.csv"
CUSTOMERS_FILE = PROJECT_ROOT / "data" / "raw" / "customers.csv"
MERCHANTS_FILE = PROJECT_ROOT / "data" / "raw" / "merchants.csv"
CUSTOMER_VALIDATION_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "validation"
    / "customer_validation_results.csv"
)

MERCHANT_VALIDATION_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "validation"
    / "merchant_validation_results.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "validation"

RESULTS_FILE = OUTPUT_DIR / "transaction_validation_results.csv"
ERRORS_FILE = OUTPUT_DIR / "transaction_validation_errors.csv"


# ---------------------------------------------------------
# Allowed values
# ---------------------------------------------------------

VALID_CURRENCIES = {
    "INR",
    "AED",
    "SAR",
    "USD",
    "EUR"
}

VALID_PAYMENT_METHODS = {
    "CARD",
    "UPI",
    "WALLET",
    "BANK_TRANSFER"
}

VALID_TRANSACTION_STATUSES = {
    "SUCCESS",
    "FAILED",
    "PENDING"
}

VALID_COUNTRIES = {
    "IN",
    "AE",
    "SA",
    "US",
    "GB"
}

VALID_GATEWAYS = {
    "GATEWAY_A",
    "GATEWAY_B",
    "GATEWAY_C"
}

VALID_RESPONSE_CODES = {
    0,
    5,
    9,
    14,
    51,
    91
}

VALID_DEVICE_TYPES = {
    "MOBILE",
    "DESKTOP",
    "TABLET"
}


# ---------------------------------------------------------
# Validation function
# ---------------------------------------------------------

def validate_transactions(transactions, customer_ids, merchant_ids):

    validation_results = []
    validation_errors = []

    # -----------------------------------------------------
    # Identify duplicate transaction IDs
    # -----------------------------------------------------

    duplicate_transaction_ids = set(
        transactions.loc[
            transactions["transaction_id"].duplicated(keep=False),
            "transaction_id"
        ]
    )

    # -----------------------------------------------------
    # Validate each transaction
    # -----------------------------------------------------

    for _, row in transactions.iterrows():

        errors = []

        # -------------------------------------------------
        # Helper function for recording errors
        # -------------------------------------------------

        def add_error(error_code, error_message):

            errors.append({
                "record_key": row["transaction_id"],
                "error_code": error_code,
                "severity": "ERROR",
                "error_message": error_message
            })

        # -------------------------------------------------
        # 1. Transaction ID
        # -------------------------------------------------

        transaction_id = row["transaction_id"]

        if pd.isna(transaction_id) or str(transaction_id).strip() == "":

            add_error(
                "TXN_MISSING_ID",
                "Transaction ID is missing."
            )

        elif transaction_id in duplicate_transaction_ids:

            add_error(
                "TXN_DUPLICATE_ID",
                "Transaction ID is not unique."
            )

        # -------------------------------------------------
        # 2. Customer ID
        # -------------------------------------------------

        customer_id = row["customer_id"]

        if pd.isna(customer_id) or str(customer_id).strip() == "":

            add_error(
                "TXN_MISSING_CUSTOMER",
                "Customer ID is missing."
            )

        elif customer_id not in customer_ids:

            add_error(
                "TXN_UNKNOWN_CUSTOMER",
                "Customer ID does not exist in the customer master."
            )

        # -------------------------------------------------
        # 3. Merchant ID
        # -------------------------------------------------

        merchant_id = row["merchant_id"]

        if pd.isna(merchant_id) or str(merchant_id).strip() == "":

            add_error(
                "TXN_MISSING_MERCHANT",
                "Merchant ID is missing."
            )

        elif merchant_id not in merchant_ids:

            add_error(
                "TXN_UNKNOWN_MERCHANT",
                "Merchant ID does not exist in the merchant master."
            )

        # -------------------------------------------------
        # 4. Transaction timestamp
        # -------------------------------------------------

        transaction_timestamp = pd.to_datetime(
            row["transaction_timestamp"],
            errors="coerce"
        )

        if pd.isna(transaction_timestamp):

            add_error(
                "TXN_INVALID_TIMESTAMP",
                "Transaction timestamp is invalid."
            )

        # -------------------------------------------------
        # 5. Transaction amount
        # -------------------------------------------------

        amount = row["amount"]

        if pd.isna(amount) or amount <= 0:

            add_error(
                "TXN_INVALID_AMOUNT",
                "Transaction amount must be greater than zero."
            )

        # -------------------------------------------------
        # 6. Currency
        # -------------------------------------------------

        currency = row["currency"]

        if pd.isna(currency) or currency not in VALID_CURRENCIES:

            add_error(
                "TXN_INVALID_CURRENCY",
                "Transaction currency is invalid."
            )

        # -------------------------------------------------
        # 7. Payment method
        # -------------------------------------------------

        payment_method = row["payment_method"]

        if (
            pd.isna(payment_method)
            or payment_method not in VALID_PAYMENT_METHODS
        ):

            add_error(
                "TXN_INVALID_PAYMENT_METHOD",
                "Payment method is invalid."
            )

        # -------------------------------------------------
        # 8. Transaction status
        # -------------------------------------------------

        transaction_status = row["transaction_status"]

        if (
            pd.isna(transaction_status)
            or transaction_status not in VALID_TRANSACTION_STATUSES
        ):

            add_error(
                "TXN_INVALID_STATUS",
                "Transaction status is invalid."
            )

        # -------------------------------------------------
        # 9. Country
        # -------------------------------------------------

        country = row["country"]

        if pd.isna(country) or country not in VALID_COUNTRIES:

            add_error(
                "TXN_INVALID_COUNTRY",
                "Transaction country is invalid."
            )

        # -------------------------------------------------
        # 10. Gateway
        # -------------------------------------------------

        gateway = row["gateway"]

        if pd.isna(gateway) or gateway not in VALID_GATEWAYS:

            add_error(
                "TXN_INVALID_GATEWAY",
                "Gateway is invalid."
            )

        # -------------------------------------------------
        # 11. Response code
        # -------------------------------------------------

        response_code = row["response_code"]

        if (
            pd.isna(response_code)
            or response_code not in VALID_RESPONSE_CODES
        ):

            add_error(
                "TXN_INVALID_RESPONSE_CODE",
                "Response code is invalid."
            )

        # -------------------------------------------------
        # 12. Device type
        # -------------------------------------------------

        device_type = row["device_type"]

        if pd.isna(device_type) or device_type not in VALID_DEVICE_TYPES:

            add_error(
                "TXN_INVALID_DEVICE",
                "Device type is invalid."
            )

        # -------------------------------------------------
        # Validation result for the current record
        # -------------------------------------------------

        if len(errors) == 0:

            validation_results.append({
                "record_key": transaction_id,
                "validation_status": "VALID"
            })

        else:

            validation_results.append({
                "record_key": transaction_id,
                "validation_status": "REJECTED"
            })

            validation_errors.extend(errors)

    # -----------------------------------------------------
    # Convert results to DataFrames
    # -----------------------------------------------------

    results_df = pd.DataFrame(validation_results)

    errors_df = pd.DataFrame(validation_errors)

    return results_df, errors_df


# ---------------------------------------------------------
# Main execution
# ---------------------------------------------------------

if __name__ == "__main__":

    print("Loading source data...")

    transactions = pd.read_csv(TRANSACTIONS_FILE)
    customers = pd.read_csv(CUSTOMERS_FILE)
    merchants = pd.read_csv(MERCHANTS_FILE)
    customer_validation = pd.read_csv(
    CUSTOMER_VALIDATION_FILE
)

    merchant_validation = pd.read_csv(
    MERCHANT_VALIDATION_FILE
)

    print(f"Transactions loaded: {len(transactions):,}")
    print(f"Customers loaded: {len(customers):,}")
    print(f"Merchants loaded: {len(merchants):,}")

    # -----------------------------------------------------
    # Build reference sets
    # -----------------------------------------------------

    customer_ids = set(
    customer_validation.loc[
        customer_validation["validation_status"] == "VALID",
        "record_key"
    ]
)

    merchant_ids = set(
    merchant_validation.loc[
        merchant_validation["validation_status"] == "VALID",
        "record_key"
    ]
)

    # -----------------------------------------------------
    # Run validation
    # -----------------------------------------------------

    print("\nValidating transactions...")

    results_df, errors_df = validate_transactions(
        transactions,
        customer_ids,
        merchant_ids
    )

    # -----------------------------------------------------
    # Create output directory
    # -----------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # -----------------------------------------------------
    # Save validation results
    # -----------------------------------------------------

    results_df.to_csv(
        RESULTS_FILE,
        index=False
    )

    errors_df.to_csv(
        ERRORS_FILE,
        index=False
    )

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    total_records = len(results_df)

    valid_records = (
        results_df["validation_status"] == "VALID"
    ).sum()

    rejected_records = (
        results_df["validation_status"] == "REJECTED"
    ).sum()

    total_errors = len(errors_df)

    print("\n----------------------------------------")
    print("Transaction Validation Summary")
    print("----------------------------------------")

    print(f"Total records:      {total_records:,}")
    print(f"Valid records:      {valid_records:,}")
    print(f"Rejected records:   {rejected_records:,}")
    print(f"Validation errors:  {total_errors:,}")

    print("\nError breakdown:")

    if not errors_df.empty:

        print(
            errors_df["error_code"]
            .value_counts()
            .to_string()
        )

    else:

        print("No validation errors found.")

    print("\nOutput files:")

    print(RESULTS_FILE)
    print(ERRORS_FILE)

    print("\nValidation completed successfully.")