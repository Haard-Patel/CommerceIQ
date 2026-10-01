import os
from pathlib import Path


# ============================================================
# Project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
)

DEFAULT_SOURCE_FILE = "online_retail.xlsx"

RAW_DATA_PATH = (
    RAW_DATA_DIR
    / DEFAULT_SOURCE_FILE
)


# ============================================================
# Database configuration
# ============================================================

DB_CONFIG = {
    "host": os.getenv(
        "COMMERCEIQ_DB_HOST",
        "localhost",
    ),
    "port": int(
        os.getenv(
            "COMMERCEIQ_DB_PORT",
            "5432",
        )
    ),
    "database": os.getenv(
        "COMMERCEIQ_DB_NAME",
        "commerceiq",
    ),
    "user": os.getenv(
        "COMMERCEIQ_DB_USER",
        "postgres",
    ),
    "password": os.getenv(
        "COMMERCEIQ_DB_PASSWORD"
    ),
}


# ============================================================
# Source configuration
# ============================================================

SOURCE_SHEET = 0


# ============================================================
# Expected source schema
# ============================================================

REQUIRED_COLUMNS = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
]