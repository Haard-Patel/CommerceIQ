import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "online_retail.xlsx"
)


DB_CONFIG = {
    "host": os.getenv("COMMERCEIQ_DB_HOST", "localhost"),
    "port": int(os.getenv("COMMERCEIQ_DB_PORT", "5432")),
    "database": os.getenv("COMMERCEIQ_DB_NAME", "commerceiq"),
    "user": os.getenv("COMMERCEIQ_DB_USER", "postgres"),
    "password": os.getenv("COMMERCEIQ_DB_PASSWORD"),
}


SOURCE_SHEET = 0


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