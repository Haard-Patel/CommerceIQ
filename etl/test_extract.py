from etl.config import (
    RAW_DATA_DIR,
    REQUIRED_COLUMNS,
)

from etl.extract import extract_data


EXPECTED_ROW_COUNT = 541_909
EXPECTED_COLUMN_COUNT = 8


SOURCE_FILES = [
    "online_retail.xlsx",
    "online_retail.csv",
    "online_retail.json",
]


def test_source_file(
    filename: str,
) -> None:
    """
    Test extraction for a single source file.
    """

    source_path = RAW_DATA_DIR / filename

    print("\n" + "=" * 60)
    print(f"TESTING: {filename}")
    print("=" * 60)

    df = extract_data(source_path)

    assert len(df) == EXPECTED_ROW_COUNT, (
        f"Expected {EXPECTED_ROW_COUNT:,} rows, "
        f"got {len(df):,}"
    )

    assert len(df.columns) == EXPECTED_COLUMN_COUNT, (
        f"Expected {EXPECTED_COLUMN_COUNT} columns, "
        f"got {len(df.columns)}"
    )

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    assert not missing_columns, (
        f"Missing required columns: {missing_columns}"
    )

    print("PASS: Row count")
    print("PASS: Column count")
    print("PASS: Required schema")


def test_all_source_formats() -> None:
    """
    Test extraction across all supported source formats.
    """

    for filename in SOURCE_FILES:
        test_source_file(filename)

    print("\n" + "=" * 60)
    print("ALL EXTRACTION TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    test_all_source_formats()