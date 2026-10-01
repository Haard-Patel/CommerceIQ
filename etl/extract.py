from pathlib import Path

import pandas as pd

from etl.config import (
    RAW_DATA_PATH,
    REQUIRED_COLUMNS,
    SOURCE_SHEET,
)


# ============================================================
# Source readers
# ============================================================

def read_excel_source(source_path: Path) -> pd.DataFrame:
    """
    Read an Excel source file into a pandas DataFrame.
    """

    return pd.read_excel(
        source_path,
        sheet_name=SOURCE_SHEET,
    )


def read_csv_source(source_path: Path) -> pd.DataFrame:
    """
    Read a CSV source file into a pandas DataFrame.
    """

    return pd.read_csv(
        source_path,
    )


def read_json_source(source_path: Path) -> pd.DataFrame:
    """
    Read a JSON source file into a pandas DataFrame.
    """

    return pd.read_json(
        source_path,
    )


# ============================================================
# Source dispatch
# ============================================================

def read_source(source_path: Path) -> pd.DataFrame:
    """
    Read a supported source file based on its file extension.

    Supported formats:

        .xlsx
        .xls
        .csv
        .json

    Returns:
        pandas.DataFrame: Extracted source data.
    """

    extension = source_path.suffix.lower()

    if extension in {".xlsx", ".xls"}:
        return read_excel_source(source_path)

    if extension == ".csv":
        return read_csv_source(source_path)

    if extension == ".json":
        return read_json_source(source_path)

    raise ValueError(
        f"Unsupported source file format: {extension}"
    )


# ============================================================
# Schema validation
# ============================================================

def validate_source_schema(df: pd.DataFrame) -> None:
    """
    Validate that the extracted DataFrame contains
    all columns required by CommerceIQ.
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {missing_columns}"
        )


# ============================================================
# Source type normalization
# ============================================================

def normalize_source_types(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Normalize source column data types into the
    standardized CommerceIQ extraction schema.

    This ensures that Excel, CSV, and JSON sources
    produce compatible DataFrames for downstream
    transformation.
    """

    normalized = df.copy()

    # --------------------------------------------------------
    # Identifier columns
    # --------------------------------------------------------

    normalized["InvoiceNo"] = (
        normalized["InvoiceNo"]
        .astype("string")
    )

    normalized["StockCode"] = (
        normalized["StockCode"]
        .astype("string")
    )

    # --------------------------------------------------------
    # Text columns
    # --------------------------------------------------------

    normalized["Description"] = (
        normalized["Description"]
        .astype("string")
    )

    normalized["Country"] = (
        normalized["Country"]
        .astype("string")
    )

    # --------------------------------------------------------
    # Numeric columns
    # --------------------------------------------------------

    normalized["Quantity"] = pd.to_numeric(
        normalized["Quantity"],
        errors="raise",
    )

    normalized["UnitPrice"] = pd.to_numeric(
        normalized["UnitPrice"],
        errors="raise",
    )

    normalized["CustomerID"] = pd.to_numeric(
        normalized["CustomerID"],
        errors="coerce",
    )

    # --------------------------------------------------------
    # Date column
    # --------------------------------------------------------

    normalized["InvoiceDate"] = pd.to_datetime(
        normalized["InvoiceDate"],
        errors="raise",
    )

    return normalized


# ============================================================
# Main extraction function
# ============================================================

def extract_data(
    source_path: Path = RAW_DATA_PATH,
) -> pd.DataFrame:
    """
    Extract source data into a standardized pandas DataFrame.

    The extraction layer:

        1. Reads the source file.
        2. Validates the required schema.
        3. Normalizes column data types.

    Args:
        source_path:
            Path to the source data file.

    Returns:
        pandas.DataFrame:
            Extracted, schema-validated, and type-normalized
            source data.
    """

    source_path = Path(source_path)

    if not source_path.exists():
        raise FileNotFoundError(
            f"Source dataset not found: {source_path}"
        )

    print(f"Reading dataset: {source_path}")

    df = read_source(source_path)

    validate_source_schema(df)

    df = normalize_source_types(df)

    print(f"Rows extracted: {len(df):,}")
    print(f"Columns extracted: {len(df.columns)}")

    return df