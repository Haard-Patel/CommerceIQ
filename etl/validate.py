import pandas as pd


class ValidationError(Exception):
    """Raised when ETL validation fails."""


def validate_transactions(df: pd.DataFrame) -> None:
    """
    Validate the transformed transaction-level dataset.
    """

    print("\n========================================")
    print("TRANSACTION VALIDATION")
    print("========================================")

    errors = []

    # --------------------------------------------------------
    # Required columns
    # --------------------------------------------------------

    required_columns = [
        "InvoiceNo",
        "StockCode",
        "InvoiceDate",
        "Quantity",
        "UnitPrice",
        "Country",
        "IsCancelled",
        "TransactionType",
        "LineRevenue",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        errors.append(
            f"Missing required columns: {missing_columns}"
        )

    # Stop here if the structure itself is invalid.
    if missing_columns:
        print("\nVALIDATION FAILED")

        for error in errors:
            print(f" - {error}")

        raise ValidationError(
            "Transaction validation failed."
        )

    # --------------------------------------------------------
    # Null checks
    # --------------------------------------------------------

    if df["InvoiceNo"].isna().any():
        errors.append("InvoiceNo contains null values.")

    if df["StockCode"].isna().any():
        errors.append("StockCode contains null values.")

    if df["InvoiceDate"].isna().any():
        errors.append("InvoiceDate contains null values.")

    if df["Quantity"].isna().any():
        errors.append("Quantity contains null values.")

    if df["UnitPrice"].isna().any():
        errors.append("UnitPrice contains null values.")

    # --------------------------------------------------------
    # Quantity validation
    # --------------------------------------------------------

    zero_quantity = (df["Quantity"] == 0).sum()

    print(f"Zero-quantity rows: {zero_quantity:,}")

    if zero_quantity > 0:
        errors.append(
            f"Found {zero_quantity:,} rows with zero quantity."
        )

    # --------------------------------------------------------
    # Price validation
    # --------------------------------------------------------

    negative_price = (df["UnitPrice"] < 0).sum()

    print(f"Negative-price rows: {negative_price:,}")

    if negative_price > 0:
        adjustment_rows = df[
            (df["UnitPrice"] < 0)
            & (df["TransactionType"] == "Adjustment")
        ]

        print(
            f"Negative-price adjustments: "
            f"{len(adjustment_rows):,}"
        )

        if len(adjustment_rows) != negative_price:
            errors.append(
                "Negative-price rows are not correctly classified "
                "as adjustments."
            )

    # --------------------------------------------------------
    # Revenue calculation validation
    # --------------------------------------------------------

    expected_revenue = (
        df["Quantity"] * df["UnitPrice"]
    )

    revenue_mismatch = (
        (df["LineRevenue"] - expected_revenue).abs() > 0.000001
    ).sum()

    print(f"Revenue mismatches: {revenue_mismatch:,}")

    if revenue_mismatch > 0:
        errors.append(
            f"Found {revenue_mismatch:,} revenue calculation mismatches."
        )

    # --------------------------------------------------------
    # Country validation
    # --------------------------------------------------------

    missing_country = df["Country"].isna().sum()

    print(f"Missing country: {missing_country:,}")

    if missing_country > 0:
        errors.append(
            f"Found {missing_country:,} rows with missing country."
        )

    # --------------------------------------------------------
    # Cancellation validation
    # --------------------------------------------------------

    cancellation_count = df["IsCancelled"].sum()

    print(
        f"Cancelled transaction rows: "
        f"{cancellation_count:,}"
    )

    # --------------------------------------------------------
    # Negative quantity reporting
    # --------------------------------------------------------

    negative_quantity = (df["Quantity"] < 0).sum()

    print(
        f"Negative-quantity rows: "
        f"{negative_quantity:,}"
    )

    # Negative quantities are intentionally reported,
    # not treated as automatic validation failures.
    # They may represent returns or corrections.

    # --------------------------------------------------------
    # Transaction type reporting
    # --------------------------------------------------------

    print("\n========================================")
    print("TRANSACTION TYPES")
    print("========================================")

    transaction_type_counts = (
        df["TransactionType"]
        .value_counts()
    )

    print(transaction_type_counts.to_string())

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    if errors:
        print("\nVALIDATION FAILED")

        for error in errors:
            print(f" - {error}")

        raise ValidationError(
            "Transaction validation failed."
        )

    print("\nVALIDATION PASSED")