from pathlib import Path

import pandas as pd


# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "data" / "raw" / "online_retail.xlsx"


# ============================================================
# Load dataset
# ============================================================

print("=" * 70)
print("CommerceIQ — Raw Dataset Inspection")
print("=" * 70)

print(f"\nDataset: {DATASET_PATH}")

if not DATASET_PATH.exists():
    raise FileNotFoundError(
        f"\nDataset not found:\n{DATASET_PATH}\n"
        "Make sure online_retail.xlsx is inside data/raw/."
    )

print("\nLoading dataset...")

df = pd.read_excel(DATASET_PATH)


# ============================================================
# Basic dimensions
# ============================================================

print("\n" + "=" * 70)
print("1. DATASET SIZE")
print("=" * 70)

print(f"Rows:    {len(df):,}")
print(f"Columns: {len(df.columns):,}")


# ============================================================
# Column information
# ============================================================

print("\n" + "=" * 70)
print("2. COLUMNS")
print("=" * 70)

for column in df.columns:
    print(f"- {column}")


# ============================================================
# Data types
# ============================================================

print("\n" + "=" * 70)
print("3. DATA TYPES")
print("=" * 70)

print(df.dtypes)


# ============================================================
# Missing values
# ============================================================

print("\n" + "=" * 70)
print("4. MISSING VALUES")
print("=" * 70)

missing = df.isna().sum()

missing = missing[missing > 0].sort_values(ascending=False)

if missing.empty:
    print("No missing values found.")
else:
    for column, count in missing.items():
        percentage = (count / len(df)) * 100
        print(f"{column}: {count:,} ({percentage:.2f}%)")


# ============================================================
# Duplicate rows
# ============================================================

print("\n" + "=" * 70)
print("5. DUPLICATES")
print("=" * 70)

duplicate_count = df.duplicated().sum()

print(f"Duplicate rows: {duplicate_count:,}")


# ============================================================
# Unique values
# ============================================================

print("\n" + "=" * 70)
print("6. UNIQUE VALUES")
print("=" * 70)

if "CustomerID" in df.columns:
    print(f"Unique customers: {df['CustomerID'].nunique(dropna=True):,}")

if "StockCode" in df.columns:
    print(f"Unique products:  {df['StockCode'].nunique(dropna=True):,}")

if "InvoiceNo" in df.columns:
    print(f"Unique invoices:  {df['InvoiceNo'].nunique(dropna=True):,}")

if "Country" in df.columns:
    print(f"Unique countries: {df['Country'].nunique(dropna=True):,}")


# ============================================================
# Date range
# ============================================================

print("\n" + "=" * 70)
print("7. DATE RANGE")
print("=" * 70)

if "InvoiceDate" in df.columns:

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce",
    )

    print(f"Earliest transaction: {df['InvoiceDate'].min()}")
    print(f"Latest transaction:   {df['InvoiceDate'].max()}")


# ============================================================
# Cancelled invoices
# ============================================================

print("\n" + "=" * 70)
print("8. CANCELLED INVOICES")
print("=" * 70)

if "InvoiceNo" in df.columns:

    invoice_numbers = df["InvoiceNo"].astype(str)

    cancelled = invoice_numbers.str.startswith("C")

    print(f"Cancelled transaction rows: {cancelled.sum():,}")
    print(
        f"Cancellation percentage: "
        f"{cancelled.mean() * 100:.2f}%"
    )


# ============================================================
# Quantity statistics
# ============================================================

print("\n" + "=" * 70)
print("9. QUANTITY")
print("=" * 70)

if "Quantity" in df.columns:

    print(f"Minimum: {df['Quantity'].min():,.0f}")
    print(f"Maximum: {df['Quantity'].max():,.0f}")
    print(f"Average: {df['Quantity'].mean():,.2f}")


# ============================================================
# Unit price statistics
# ============================================================

print("\n" + "=" * 70)
print("10. UNIT PRICE")
print("=" * 70)

if "UnitPrice" in df.columns:

    print(f"Minimum: {df['UnitPrice'].min():,.2f}")
    print(f"Maximum: {df['UnitPrice'].max():,.2f}")
    print(f"Average: {df['UnitPrice'].mean():,.2f}")


# ============================================================
# Countries
# ============================================================

print("\n" + "=" * 70)
print("11. TOP COUNTRIES")
print("=" * 70)

if "Country" in df.columns:

    country_counts = (
        df["Country"]
        .value_counts()
        .head(10)
    )

    for country, count in country_counts.items():
        print(f"{country}: {count:,}")


# ============================================================
# Sample records
# ============================================================

print("\n" + "=" * 70)
print("12. SAMPLE RECORDS")
print("=" * 70)

print(
    df.head(10).to_string(index=False)
)


# ============================================================
# Finished
# ============================================================

print("\n" + "=" * 70)
print("Inspection complete.")
print("=" * 70)