import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


# ============================================================
# PROFILING FUNCTION
# ============================================================

def profile_dataset(file_path):
    """
    Load a CSV file and generate a basic source-data profile.
    """

    df = pd.read_csv(file_path)

    print("=" * 70)
    print(f"DATASET: {file_path.name}")
    print("=" * 70)

    # --------------------------------------------------------
    # Basic information
    # --------------------------------------------------------

    print(f"\nRows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    # --------------------------------------------------------
    # Data types
    # --------------------------------------------------------

    print("\nData Types:")
    print(df.dtypes)

    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    print("\nMissing Values:")
    
    missing = df.isnull().sum()

    for column, count in missing.items():
        print(
            f"  {column}: {count:,}"
        )

    # --------------------------------------------------------
    # Empty strings
    # --------------------------------------------------------

    print("\nEmpty Strings:")

    for column in df.columns:

        empty_count = (
            df[column]
            .astype(str)
            .str.strip()
            .eq("")
            .sum()
        )

        if empty_count > 0:
            print(
                f"  {column}: {empty_count:,}"
            )

    # --------------------------------------------------------
    # Duplicate rows
    # --------------------------------------------------------

    duplicate_rows = df.duplicated().sum()

    print(
        f"\nDuplicate complete rows: "
        f"{duplicate_rows:,}"
    )

    # --------------------------------------------------------
    # Unique values
    # --------------------------------------------------------

    print("\nUnique Values:")

    for column in df.columns:

        unique_count = df[column].nunique(
            dropna=False
        )

        print(
            f"  {column}: {unique_count:,}"
        )

    # --------------------------------------------------------
    # Numeric statistics
    # --------------------------------------------------------

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    if len(numeric_columns) > 0:

        print("\nNumeric Statistics:")

        print(
            df[numeric_columns].describe()
        )

    # --------------------------------------------------------
    # Sample records
    # --------------------------------------------------------

    print("\nSample Records:")

    print(
        df.head(5).to_string(index=False)
    )

    print()


# ============================================================
# MAIN
# ============================================================

def main():

    datasets = [
        "customers.csv",
        "merchants.csv",
        "transactions.csv"
    ]

    for dataset in datasets:

        file_path = RAW_DATA_DIR / dataset

        if not file_path.exists():

            print(
                f"File not found: {file_path}"
            )

            continue

        profile_dataset(file_path)


if __name__ == "__main__":
    main()