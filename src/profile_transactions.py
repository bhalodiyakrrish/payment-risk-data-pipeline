import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRANSACTION_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "transactions.csv"
)


def main():

    df = pd.read_csv(
        TRANSACTION_FILE
    )

    print("=" * 70)
    print("TRANSACTION BUSINESS PROFILE")
    print("=" * 70)

    # --------------------------------------------------------
    # Transaction status
    # --------------------------------------------------------

    print("\nTransaction Status:")
    print(
        df["transaction_status"]
        .value_counts(dropna=False)
    )

    # --------------------------------------------------------
    # Payment method
    # --------------------------------------------------------

    print("\nPayment Method:")
    print(
        df["payment_method"]
        .value_counts(dropna=False)
    )

    # --------------------------------------------------------
    # Currency
    # --------------------------------------------------------

    print("\nCurrency:")
    print(
        df["currency"]
        .value_counts(dropna=False)
    )

    # --------------------------------------------------------
    # Gateway
    # --------------------------------------------------------

    print("\nGateway:")
    print(
        df["gateway"]
        .value_counts(dropna=False)
    )

    # --------------------------------------------------------
    # Device
    # --------------------------------------------------------

    print("\nDevice Type:")
    print(
        df["device_type"]
        .value_counts(dropna=False)
    )

    # --------------------------------------------------------
    # Country
    # --------------------------------------------------------

    print("\nCountry:")
    print(
        df["country"]
        .value_counts(dropna=False)
    )

    # --------------------------------------------------------
    # Amount
    # --------------------------------------------------------

    print("\nTransaction Amount:")
    print(
        df["amount"].describe()
    )


if __name__ == "__main__":
    main()