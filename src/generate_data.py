import csv
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

NUM_CUSTOMERS = 10_000
NUM_MERCHANTS = 1_000
NUM_TRANSACTIONS = 100_000

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

RANDOM_SEED = 42


# ============================================================
# REFERENCE DATA
# ============================================================

COUNTRIES = ["IN", "AE", "SA", "US", "GB"]

CURRENCIES = {
    "IN": "INR",
    "AE": "AED",
    "SA": "SAR",
    "US": "USD",
    "GB": "EUR"
}

PAYMENT_METHODS = [
    "CARD",
    "UPI",
    "WALLET",
    "BANK_TRANSFER"
]

TRANSACTION_STATUSES = [
    "SUCCESS",
    "FAILED",
    "PENDING"
]

DEVICE_TYPES = [
    "MOBILE",
    "DESKTOP",
    "TABLET"
]

GATEWAYS = [
    "GATEWAY_A",
    "GATEWAY_B",
    "GATEWAY_C"
]

MERCHANT_CATEGORIES = [
    "RETAIL",
    "FOOD",
    "TRAVEL",
    "ENTERTAINMENT",
    "HEALTHCARE",
    "EDUCATION",
    "SERVICES"
]

CUSTOMER_STATUSES = [
    "ACTIVE",
    "INACTIVE",
    "SUSPENDED"
]

MERCHANT_STATUSES = [
    "ACTIVE",
    "INACTIVE",
    "SUSPENDED"
]

FIRST_NAMES = [
    "Aarav",
    "Arjun",
    "Rohan",
    "Rahul",
    "Karan",
    "Aditya",
    "Vikram",
    "Neha",
    "Priya",
    "Ananya",
    "Sneha",
    "Isha",
    "Meera",
    "Kavya",
    "Riya"
]

LAST_NAMES = [
    "Sharma",
    "Patel",
    "Shah",
    "Mehta",
    "Bhat",
    "Joshi",
    "Verma",
    "Gupta",
    "Reddy",
    "Nair",
    "Iyer",
    "Desai"
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def random_date(start_date, end_date):
    """Generate a random date between two dates."""
    days = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, days))


def random_timestamp(start_date, end_date):
    """Generate a random timestamp between two dates."""
    seconds = int((end_date - start_date).total_seconds())
    return start_date + timedelta(seconds=random.randint(0, seconds))


def generate_name():
    """Generate a simple synthetic person name."""
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


# ============================================================
# CUSTOMER GENERATION
# ============================================================

def generate_customers():
    customers = []

    start_date = datetime(2022, 1, 1)
    end_date = datetime(2026, 9, 1)

    for i in range(1, NUM_CUSTOMERS + 1):

        customer_id = f"CUST{i:06d}"
        name = generate_name()

        first_name = name.split()[0].lower()
        customer_email = f"{first_name}.{i}@example.com"

        country = random.choice(COUNTRIES)

        registration_date = random_date(
            start_date,
            end_date
        ).date()

        status = random.choices(
            CUSTOMER_STATUSES,
            weights=[90, 7, 3]
        )[0]

        customers.append({
            "customer_id": customer_id,
            "customer_name": name,
            "customer_email": customer_email,
            "country": country,
            "registration_date": registration_date,
            "customer_status": status
        })

    return customers


# ============================================================
# MERCHANT GENERATION
# ============================================================

def generate_merchants():
    merchants = []

    start_date = datetime(2022, 1, 1)
    end_date = datetime(2026, 6, 1)

    for i in range(1, NUM_MERCHANTS + 1):

        merchant_id = f"MER{i:05d}"

        merchant_name = (
            f"Merchant {i}"
        )

        category = random.choice(
            MERCHANT_CATEGORIES
        )

        country = random.choice(
            COUNTRIES
        )

        onboarding_date = random_date(
            start_date,
            end_date
        ).date()

        status = random.choices(
            MERCHANT_STATUSES,
            weights=[90, 7, 3]
        )[0]

        merchants.append({
            "merchant_id": merchant_id,
            "merchant_name": merchant_name,
            "merchant_category": category,
            "country": country,
            "onboarding_date": onboarding_date,
            "merchant_status": status
        })

    return merchants


# ============================================================
# TRANSACTION GENERATION
# ============================================================

def generate_transactions(customers, merchants):

    transactions = []

    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 9, 15)

    for i in range(1, NUM_TRANSACTIONS + 1):

        transaction_id = f"TXN{i:08d}"

        customer = random.choice(customers)
        merchant = random.choice(merchants)

        country = random.choice(COUNTRIES)

        currency = CURRENCIES[country]

        payment_method = random.choice(
            PAYMENT_METHODS
        )

        status = random.choices(
            TRANSACTION_STATUSES,
            weights=[85, 12, 3]
        )[0]

        timestamp = random_timestamp(
            start_date,
            end_date
        )

        amount = round(
            random.uniform(50, 50_000),
            2
        )

        gateway = random.choice(
            GATEWAYS
        )

        if status == "SUCCESS":
            response_code = "00"
        elif status == "FAILED":
            response_code = random.choice(
                ["05", "14", "51", "91"]
            )
        else:
            response_code = "09"

        device_type = random.choice(
            DEVICE_TYPES
        )

        transactions.append({
            "transaction_id": transaction_id,
            "customer_id": customer["customer_id"],
            "merchant_id": merchant["merchant_id"],
            "transaction_timestamp": timestamp,
            "amount": amount,
            "currency": currency,
            "payment_method": payment_method,
            "transaction_status": status,
            "country": country,
            "gateway": gateway,
            "response_code": response_code,
            "device_type": device_type
        })

    return transactions


# ============================================================
# INTRODUCE DATA QUALITY ISSUES
# ============================================================

def introduce_data_quality_issues(
    customers,
    merchants,
    transactions
):

    # --------------------------------------------------------
    # Customer issues
    # --------------------------------------------------------

    # Missing email
    for customer in random.sample(customers, 50):
        customer["customer_email"] = ""

    # Invalid email
    for customer in random.sample(customers, 30):
        customer["customer_email"] = "invalid-email"


    # --------------------------------------------------------
    # Merchant issues
    # --------------------------------------------------------

    # Missing category
    for merchant in random.sample(merchants, 30):
        merchant["merchant_category"] = ""


    # --------------------------------------------------------
    # Transaction issues
    # --------------------------------------------------------

    # Duplicate transaction IDs
    duplicate_transactions = random.sample(
        transactions,
        100
    )

    for transaction in duplicate_transactions:
        transaction["transaction_id"] = "TXN00000001"


    # Negative amounts
    for transaction in random.sample(transactions, 100):
        transaction["amount"] = -abs(
            transaction["amount"]
        )


    # Zero amounts
    for transaction in random.sample(transactions, 100):
        transaction["amount"] = 0


    # Missing customer IDs
    for transaction in random.sample(transactions, 100):
        transaction["customer_id"] = ""


    # Missing merchant IDs
    for transaction in random.sample(transactions, 100):
        transaction["merchant_id"] = ""


    # Invalid currencies
    for transaction in random.sample(transactions, 100):
        transaction["currency"] = "XYZ"


    # Invalid transaction status
    for transaction in random.sample(transactions, 100):
        transaction["transaction_status"] = "UNKNOWN"


    # Invalid payment method
    for transaction in random.sample(transactions, 100):
        transaction["payment_method"] = "CRYPTO"


    # Unknown customer IDs
    for transaction in random.sample(transactions, 100):
        transaction["customer_id"] = "CUST999999"


    # Unknown merchant IDs
    for transaction in random.sample(transactions, 100):
        transaction["merchant_id"] = "MER99999"


# ============================================================
# CSV WRITER
# ============================================================

def write_csv(file_path, records):

    if not records:
        return

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        file_path,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=records[0].keys()
        )

        writer.writeheader()
        writer.writerows(records)


# ============================================================
# MAIN
# ============================================================

def main():

    random.seed(RANDOM_SEED)

    print("Generating customers...")
    customers = generate_customers()

    print("Generating merchants...")
    merchants = generate_merchants()

    print("Generating transactions...")
    transactions = generate_transactions(
        customers,
        merchants
    )

    print("Introducing controlled data quality issues...")

    introduce_data_quality_issues(
        customers,
        merchants,
        transactions
    )

    print("Writing CSV files...")

    write_csv(
        OUTPUT_DIR / "customers.csv",
        customers
    )

    write_csv(
        OUTPUT_DIR / "merchants.csv",
        merchants
    )

    write_csv(
        OUTPUT_DIR / "transactions.csv",
        transactions
    )

    print()
    print("Data generation completed.")
    print(f"Customers: {len(customers):,}")
    print(f"Merchants: {len(merchants):,}")
    print(f"Transactions: {len(transactions):,}")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()