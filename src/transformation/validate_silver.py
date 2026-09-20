import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SILVER_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "silver"
)

CUSTOMERS_FILE = SILVER_DIR / "customers.csv"
MERCHANTS_FILE = SILVER_DIR / "merchants.csv"
TRANSACTIONS_FILE = SILVER_DIR / "transactions.csv"


# ---------------------------------------------------------
# Expected values
# ---------------------------------------------------------

EXPECTED_CUSTOMERS = 9_920
EXPECTED_MERCHANTS = 970
EXPECTED_TRANSACTIONS = 95_188

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
    "00",
    "05",
    "09",
    "14",
    "51",
    "91"
}

VALID_DEVICE_TYPES = {
    "MOBILE",
    "DESKTOP",
    "TABLET"
}

VALID_CUSTOMER_STATUSES = {
    "ACTIVE",
    "INACTIVE",
    "SUSPENDED"
}

VALID_MERCHANT_CATEGORIES = {
    "RETAIL",
    "FOOD",
    "TRAVEL",
    "ENTERTAINMENT",
    "HEALTHCARE",
    "EDUCATION",
    "SERVICES"
}

VALID_MERCHANT_STATUSES = {
    "ACTIVE",
    "INACTIVE",
    "SUSPENDED"
}


# ---------------------------------------------------------
# Check helper
# ---------------------------------------------------------

check_results = []


def check(name, condition, details):
    """
    Record the result of a quality check.
    """

    status = "PASS" if condition else "FAIL"

    check_results.append({
        "check": name,
        "status": status,
        "details": details
    })

    symbol = "PASS" if condition else "FAIL"

    print(f"[{symbol}] {name}")
    print(f"       {details}")


# =========================================================
# Load Silver datasets
# =========================================================

print("----------------------------------------")
print("Loading Silver datasets")
print("----------------------------------------")

customers = pd.read_csv(CUSTOMERS_FILE)
merchants = pd.read_csv(MERCHANTS_FILE)
transactions = pd.read_csv(
    TRANSACTIONS_FILE,
    dtype={"response_code": str}
)

print(f"Customers:    {len(customers):,}")
print(f"Merchants:    {len(merchants):,}")
print(f"Transactions: {len(transactions):,}")


# =========================================================
# CUSTOMER CHECKS
# =========================================================

print("\n========================================")
print("CUSTOMER QUALITY CHECKS")
print("========================================")


# ---------------------------------------------------------
# Customer record count
# ---------------------------------------------------------

check(
    "Customer record count",
    len(customers) == EXPECTED_CUSTOMERS,
    f"Expected {EXPECTED_CUSTOMERS:,}, found {len(customers):,}"
)


# ---------------------------------------------------------
# Customer ID completeness
# ---------------------------------------------------------

missing_customer_ids = customers["customer_id"].isna().sum()

check(
    "Customer ID completeness",
    missing_customer_ids == 0,
    f"Missing customer IDs: {missing_customer_ids}"
)


# ---------------------------------------------------------
# Customer ID uniqueness
# ---------------------------------------------------------

duplicate_customer_ids = customers["customer_id"].duplicated().sum()

check(
    "Customer ID uniqueness",
    duplicate_customer_ids == 0,
    f"Duplicate customer IDs: {duplicate_customer_ids}"
)


# ---------------------------------------------------------
# Customer email completeness
# ---------------------------------------------------------

missing_customer_emails = customers["customer_email"].isna().sum()

check(
    "Customer email completeness",
    missing_customer_emails == 0,
    f"Missing customer emails: {missing_customer_emails}"
)


# ---------------------------------------------------------
# Customer registration date
# ---------------------------------------------------------

customer_dates = pd.to_datetime(
    customers["registration_date"],
    errors="coerce"
)

invalid_customer_dates = customer_dates.isna().sum()

check(
    "Customer registration date validity",
    invalid_customer_dates == 0,
    f"Invalid registration dates: {invalid_customer_dates}"
)


# ---------------------------------------------------------
# Customer status
# ---------------------------------------------------------

invalid_customer_statuses = (
    ~customers["customer_status"].isin(
        VALID_CUSTOMER_STATUSES
    )
).sum()

check(
    "Customer status validity",
    invalid_customer_statuses == 0,
    f"Invalid customer statuses: {invalid_customer_statuses}"
)


# =========================================================
# MERCHANT CHECKS
# =========================================================

print("\n========================================")
print("MERCHANT QUALITY CHECKS")
print("========================================")


# ---------------------------------------------------------
# Merchant record count
# ---------------------------------------------------------

check(
    "Merchant record count",
    len(merchants) == EXPECTED_MERCHANTS,
    f"Expected {EXPECTED_MERCHANTS:,}, found {len(merchants):,}"
)


# ---------------------------------------------------------
# Merchant ID completeness
# ---------------------------------------------------------

missing_merchant_ids = merchants["merchant_id"].isna().sum()

check(
    "Merchant ID completeness",
    missing_merchant_ids == 0,
    f"Missing merchant IDs: {missing_merchant_ids}"
)


# ---------------------------------------------------------
# Merchant ID uniqueness
# ---------------------------------------------------------

duplicate_merchant_ids = merchants["merchant_id"].duplicated().sum()

check(
    "Merchant ID uniqueness",
    duplicate_merchant_ids == 0,
    f"Duplicate merchant IDs: {duplicate_merchant_ids}"
)


# ---------------------------------------------------------
# Merchant category completeness
# ---------------------------------------------------------

missing_merchant_categories = merchants["merchant_category"].isna().sum()

check(
    "Merchant category completeness",
    missing_merchant_categories == 0,
    f"Missing merchant categories: {missing_merchant_categories}"
)


# ---------------------------------------------------------
# Merchant category validity
# ---------------------------------------------------------

invalid_merchant_categories = (
    ~merchants["merchant_category"].isin(
        VALID_MERCHANT_CATEGORIES
    )
).sum()

check(
    "Merchant category validity",
    invalid_merchant_categories == 0,
    f"Invalid merchant categories: {invalid_merchant_categories}"
)


# ---------------------------------------------------------
# Merchant onboarding date
# ---------------------------------------------------------

merchant_dates = pd.to_datetime(
    merchants["onboarding_date"],
    errors="coerce"
)

invalid_merchant_dates = merchant_dates.isna().sum()

check(
    "Merchant onboarding date validity",
    invalid_merchant_dates == 0,
    f"Invalid onboarding dates: {invalid_merchant_dates}"
)


# ---------------------------------------------------------
# Merchant status
# ---------------------------------------------------------

invalid_merchant_statuses = (
    ~merchants["merchant_status"].isin(
        VALID_MERCHANT_STATUSES
    )
).sum()

check(
    "Merchant status validity",
    invalid_merchant_statuses == 0,
    f"Invalid merchant statuses: {invalid_merchant_statuses}"
)


# =========================================================
# TRANSACTION CHECKS
# =========================================================

print("\n========================================")
print("TRANSACTION QUALITY CHECKS")
print("========================================")


# ---------------------------------------------------------
# Transaction record count
# ---------------------------------------------------------

check(
    "Transaction record count",
    len(transactions) == EXPECTED_TRANSACTIONS,
    f"Expected {EXPECTED_TRANSACTIONS:,}, found {len(transactions):,}"
)


# ---------------------------------------------------------
# Transaction ID completeness
# ---------------------------------------------------------

missing_transaction_ids = transactions["transaction_id"].isna().sum()

check(
    "Transaction ID completeness",
    missing_transaction_ids == 0,
    f"Missing transaction IDs: {missing_transaction_ids}"
)


# ---------------------------------------------------------
# Transaction ID uniqueness
# ---------------------------------------------------------

duplicate_transaction_ids = transactions[
    "transaction_id"
].duplicated().sum()

check(
    "Transaction ID uniqueness",
    duplicate_transaction_ids == 0,
    f"Duplicate transaction IDs: {duplicate_transaction_ids}"
)


# ---------------------------------------------------------
# Customer ID completeness
# ---------------------------------------------------------

missing_transaction_customer_ids = (
    transactions["customer_id"].isna().sum()
)

check(
    "Transaction customer ID completeness",
    missing_transaction_customer_ids == 0,
    f"Missing customer IDs: {missing_transaction_customer_ids}"
)


# ---------------------------------------------------------
# Merchant ID completeness
# ---------------------------------------------------------

missing_transaction_merchant_ids = (
    transactions["merchant_id"].isna().sum()
)

check(
    "Transaction merchant ID completeness",
    missing_transaction_merchant_ids == 0,
    f"Missing merchant IDs: {missing_transaction_merchant_ids}"
)


# =========================================================
# Referential integrity
# =========================================================

customer_ids = set(
    customers["customer_id"]
)

merchant_ids = set(
    merchants["merchant_id"]
)


# ---------------------------------------------------------
# Customer references
# ---------------------------------------------------------

unknown_customer_ids = transactions[
    ~transactions["customer_id"].isin(customer_ids)
]

check(
    "Transaction customer referential integrity",
    len(unknown_customer_ids) == 0,
    f"Transactions with unknown customers: {len(unknown_customer_ids)}"
)


# ---------------------------------------------------------
# Merchant references
# ---------------------------------------------------------

unknown_merchant_ids = transactions[
    ~transactions["merchant_id"].isin(merchant_ids)
]

check(
    "Transaction merchant referential integrity",
    len(unknown_merchant_ids) == 0,
    f"Transactions with unknown merchants: {len(unknown_merchant_ids)}"
)


# ---------------------------------------------------------
# Transaction timestamp
# ---------------------------------------------------------

transaction_dates = pd.to_datetime(
    transactions["transaction_timestamp"],
    errors="coerce"
)

invalid_transaction_dates = transaction_dates.isna().sum()

check(
    "Transaction timestamp validity",
    invalid_transaction_dates == 0,
    f"Invalid timestamps: {invalid_transaction_dates}"
)


# ---------------------------------------------------------
# Transaction amount
# ---------------------------------------------------------

invalid_amounts = (
    pd.to_numeric(
        transactions["amount"],
        errors="coerce"
    ) <= 0
).sum()

check(
    "Transaction amount validity",
    invalid_amounts == 0,
    f"Invalid amounts: {invalid_amounts}"
)


# ---------------------------------------------------------
# Currency
# ---------------------------------------------------------

invalid_currencies = (
    ~transactions["currency"].isin(
        VALID_CURRENCIES
    )
).sum()

check(
    "Currency validity",
    invalid_currencies == 0,
    f"Invalid currencies: {invalid_currencies}"
)


# ---------------------------------------------------------
# Payment method
# ---------------------------------------------------------

invalid_payment_methods = (
    ~transactions["payment_method"].isin(
        VALID_PAYMENT_METHODS
    )
).sum()

check(
    "Payment method validity",
    invalid_payment_methods == 0,
    f"Invalid payment methods: {invalid_payment_methods}"
)


# ---------------------------------------------------------
# Transaction status
# ---------------------------------------------------------

invalid_transaction_statuses = (
    ~transactions["transaction_status"].isin(
        VALID_TRANSACTION_STATUSES
    )
).sum()

check(
    "Transaction status validity",
    invalid_transaction_statuses == 0,
    f"Invalid transaction statuses: {invalid_transaction_statuses}"
)


# ---------------------------------------------------------
# Country
# ---------------------------------------------------------

invalid_countries = (
    ~transactions["country"].isin(
        VALID_COUNTRIES
    )
).sum()

check(
    "Country validity",
    invalid_countries == 0,
    f"Invalid countries: {invalid_countries}"
)


# ---------------------------------------------------------
# Gateway
# ---------------------------------------------------------

invalid_gateways = (
    ~transactions["gateway"].isin(
        VALID_GATEWAYS
    )
).sum()

check(
    "Gateway validity",
    invalid_gateways == 0,
    f"Invalid gateways: {invalid_gateways}"
)


# ---------------------------------------------------------
# Response code
# ---------------------------------------------------------

invalid_response_codes = (
    ~transactions["response_code"].isin(
        VALID_RESPONSE_CODES
    )
).sum()

check(
    "Response code validity",
    invalid_response_codes == 0,
    f"Invalid response codes: {invalid_response_codes}"
)


# ---------------------------------------------------------
# Device type
# ---------------------------------------------------------

invalid_device_types = (
    ~transactions["device_type"].isin(
        VALID_DEVICE_TYPES
    )
).sum()

check(
    "Device type validity",
    invalid_device_types == 0,
    f"Invalid device types: {invalid_device_types}"
)


# ---------------------------------------------------------
# Complete duplicate rows
# ---------------------------------------------------------

duplicate_complete_rows = transactions.duplicated().sum()

check(
    "Duplicate complete transaction rows",
    duplicate_complete_rows == 0,
    f"Duplicate complete rows: {duplicate_complete_rows}"
)


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n========================================")
print("SILVER QUALITY CHECK SUMMARY")
print("========================================")

total_checks = len(check_results)

passed_checks = sum(
    result["status"] == "PASS"
    for result in check_results
)

failed_checks = sum(
    result["status"] == "FAIL"
    for result in check_results
)

print(f"Total checks:  {total_checks}")
print(f"Passed:        {passed_checks}")
print(f"Failed:        {failed_checks}")

print("\n----------------------------------------")

if failed_checks == 0:

    print("SILVER QUALITY STATUS: PASS")
    print("Silver layer is ready for warehouse loading.")

else:

    print("SILVER QUALITY STATUS: FAIL")
    print("Silver layer requires investigation before warehouse loading.")


# =========================================================
# Save quality-check results
# =========================================================

RESULTS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "silver"
    / "silver_quality_results.csv"
)

results_df = pd.DataFrame(check_results)

results_df.to_csv(
    RESULTS_FILE,
    index=False
)

print("\nQuality-check results saved to:")
print(RESULTS_FILE)