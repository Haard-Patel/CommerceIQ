import pandas as pd

from etl.extract import extract_data
from etl.transform import transform_transactions


def test_transaction_type_classification() -> None:
    """
    Verify that transaction types are mutually exclusive
    and that cancellations take priority over returns.
    """

    test_data = pd.DataFrame(
        {
            "InvoiceNo": [
                "10001",
                "10002",
                "C10003",
                "10004",
            ],
            "StockCode": [
                "A",
                "B",
                "C",
                "D",
            ],
            "Description": [
                "Sale",
                "Return",
                "Cancellation",
                "Adjustment",
            ],
            "Quantity": [
                2,
                -2,
                -3,
                1,
            ],
            "InvoiceDate": pd.to_datetime(
                [
                    "2011-01-01",
                    "2011-01-02",
                    "2011-01-03",
                    "2011-01-04",
                ]
            ),
            "UnitPrice": [
                10.0,
                10.0,
                10.0,
                -5.0,
            ],
            "CustomerID": [
                1,
                2,
                3,
                4,
            ],
            "Country": [
                "UK",
                "UK",
                "UK",
                "UK",
            ],
        }
    )

    transformed = transform_transactions(
        test_data
    )

    expected_types = [
        "Sale",
        "Return",
        "Cancellation",
        "Adjustment",
    ]

    actual_types = (
        transformed["TransactionType"]
        .tolist()
    )

    assert actual_types == expected_types, (
        f"Expected {expected_types}, "
        f"got {actual_types}"
    )

    expected_valid_sales = [
        True,
        False,
        False,
        False,
    ]

    actual_valid_sales = (
        transformed["IsValidSale"]
        .tolist()
    )

    assert actual_valid_sales == expected_valid_sales, (
        f"Expected {expected_valid_sales}, "
        f"got {actual_valid_sales}"
    )

    print(
        "PASS: IsValidSale classification"
    )

    print(
        "PASS: Transaction type classification"
    )


def test_real_dataset_transformation() -> None:
    """
    Verify the transformation of the real CommerceIQ
    source dataset.
    """

    df = extract_data()

    transformed_df = transform_transactions(
        df
    )

    print("\n========================================")
    print("REAL DATASET TRANSFORMATION")
    print("========================================")

    print("\nTRANSACTION TYPES")

    print(
        transformed_df["TransactionType"]
        .value_counts()
        .to_string()
    )

    print("\nTransformed columns:")

    print(
        transformed_df.columns.tolist()
    )

    print("\nFirst 5 transformed rows:")

    print(
        transformed_df[
            [
                "InvoiceNo",
                "StockCode",
                "Quantity",
                "UnitPrice",
                "LineRevenue",
                "IsCancelled",
                "IsValidSale",
                "CustomerID",
                "Country",
            ]
        ].head()
    )

    print("\nFinal shape:")

    print(
        transformed_df.shape
    )

    print("\nCancellation breakdown:")

    print(
        transformed_df[
            "IsCancelled"
        ].value_counts()
    )

    expected_counts = {
        "Sale": 526_052,
        "Cancellation": 9_251,
        "Return": 1_336,
        "Adjustment": 2,
    }

    actual_counts = (
        transformed_df[
            "TransactionType"
        ]
        .value_counts()
        .to_dict()
    )

    assert actual_counts == expected_counts, (
        f"Unexpected transaction counts: "
        f"{actual_counts}"
    )

    assert (
        transformed_df["IsCancelled"].sum()
        == 9_251
    ), (
        "Unexpected cancellation count"
    )

    assert len(transformed_df) == 536_641, (
        "Unexpected transformed row count"
    )
    valid_sale_count = (
        transformed_df["IsValidSale"]
        .sum()
    )

    assert valid_sale_count == 524_878, (
        f"Expected 524,878 valid sales, "
        f"got {valid_sale_count}"
    )

    print(
        "PASS: Valid sale count"
    )

    invalid_sale_rows = transformed_df[
        transformed_df["IsValidSale"]
        & (
            (transformed_df["Quantity"] <= 0)
            | (transformed_df["UnitPrice"] <= 0)
            | transformed_df["IsCancelled"]
        )
    ]

    assert invalid_sale_rows.empty, (
        "IsValidSale contains rows that violate "
        "the valid-sale business rules"
    )

    print(
        "PASS: Valid sale business rules"
    )

    print("\nPASS: Real dataset transaction counts")
    print("PASS: Cancellation count")
    print("PASS: Transformed row count")

def test_transformation_data_quality() -> None:
    """
    Verify the core data-quality guarantees produced by
    the transaction transformation layer.
    """

    df = extract_data()

    transformed = transform_transactions(
        df
    )

    print("\n========================================")
    print("TRANSFORMATION DATA-QUALITY TEST")
    print("========================================")

    # --------------------------------------------------------
    # Quantity validation
    # --------------------------------------------------------

    zero_quantity_count = (
        transformed["Quantity"]
        .eq(0)
        .sum()
    )

    assert zero_quantity_count == 0, (
        f"Found {zero_quantity_count} zero-quantity rows"
    )

    print(
        "PASS: No zero-quantity transactions"
    )

    # --------------------------------------------------------
    # Revenue validation
    # --------------------------------------------------------

    expected_revenue = (
        transformed["Quantity"]
        * transformed["UnitPrice"]
    )

    revenue_matches = (
        transformed["LineRevenue"]
        == expected_revenue
    )

    assert revenue_matches.all(), (
        "LineRevenue does not match "
        "Quantity × UnitPrice"
    )

    print(
        "PASS: LineRevenue calculation"
    )

    # --------------------------------------------------------
    # Cancellation consistency
    # --------------------------------------------------------

    invalid_cancellations = transformed[
        transformed["IsCancelled"]
        & (
            transformed["TransactionType"]
            != "Cancellation"
        )
    ]

    assert invalid_cancellations.empty, (
        "Cancelled transactions must have "
        "TransactionType = Cancellation"
    )

    print(
        "PASS: Cancellation classification consistency"
    )

    # --------------------------------------------------------
    # Return consistency
    # --------------------------------------------------------

    invalid_returns = transformed[
        (~transformed["IsCancelled"])
        & (transformed["Quantity"] < 0)
        & (
            transformed["TransactionType"]
            != "Return"
        )
    ]

    assert invalid_returns.empty, (
        "Non-cancelled negative-quantity transactions "
        "must have TransactionType = Return"
    )

    print(
        "PASS: Return classification consistency"
    )

    # --------------------------------------------------------
    # Adjustment consistency
    # --------------------------------------------------------

    invalid_adjustments = transformed[
        (transformed["UnitPrice"] < 0)
        & (
            transformed["TransactionType"]
            != "Adjustment"
        )
    ]

    assert invalid_adjustments.empty, (
        "Negative-price transactions must have "
        "TransactionType = Adjustment"
    )

    print(
        "PASS: Adjustment classification consistency"
    )
def run_all_tests() -> None:
    """
    Run all transformation tests.
    """

    print("\n")
    print("============================================================")
    print("             COMMERCEIQ TRANSFORM TESTS")
    print("============================================================")

    print("\n[1/3] CLASSIFICATION TEST")

    test_transaction_type_classification()

    print("\n[2/3] REAL DATASET TEST")

    test_real_dataset_transformation()

    print("\n[3/3] DATA-QUALITY TEST")

    test_transformation_data_quality()

    print("\n")
    print("============================================================")
    print("          ALL TRANSFORMATION TESTS PASSED")
    print("============================================================")

if __name__ == "__main__":
    run_all_tests()