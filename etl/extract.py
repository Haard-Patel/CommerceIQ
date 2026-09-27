import pandas as pd

from etl.config import RAW_DATA_PATH, REQUIRED_COLUMNS, SOURCE_SHEET


def extract_data() -> pd.DataFrame:
    """
    Extract raw e-commerce data from the source Excel file.

    Returns:
        pandas.DataFrame: Raw dataset loaded into memory.
    """

    # --------------------------------------------------------
    # 1. Verify that the source file exists
    # --------------------------------------------------------

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Source dataset not found: {RAW_DATA_PATH}"
        )

    print(f"Reading dataset: {RAW_DATA_PATH}")

    # --------------------------------------------------------
    # 2. Read the Excel file
    # --------------------------------------------------------

    df = pd.read_excel(
        RAW_DATA_PATH,
        sheet_name=SOURCE_SHEET,
    )

    # --------------------------------------------------------
    # 3. Verify required columns
    # --------------------------------------------------------

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {missing_columns}"
        )

    # --------------------------------------------------------
    # 4. Report extraction result
    # --------------------------------------------------------

    print(f"Rows extracted: {len(df):,}")
    print(f"Columns extracted: {len(df.columns)}")

    return df