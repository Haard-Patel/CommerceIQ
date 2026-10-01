from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

SOURCE_EXCEL = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "online_retail.xlsx"
)

OUTPUT_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "raw"
)


def create_source_formats() -> None:
    """
    Create CSV and JSON versions of the validated source dataset.

    The generated files are used to test CommerceIQ's
    multi-format extraction layer.
    """

    if not SOURCE_EXCEL.exists():
        raise FileNotFoundError(
            f"Source Excel file not found: {SOURCE_EXCEL}"
        )

    print(f"Reading source Excel file: {SOURCE_EXCEL}")

    df = pd.read_excel(
        SOURCE_EXCEL,
        sheet_name=0,
    )

    print(f"Rows loaded: {len(df):,}")
    print(f"Columns loaded: {len(df.columns)}")

    csv_path = OUTPUT_DIRECTORY / "online_retail.csv"
    json_path = OUTPUT_DIRECTORY / "online_retail.json"

    print("\nCreating CSV...")
    df.to_csv(
        csv_path,
        index=False,
    )

    print(f"CSV created: {csv_path}")

    print("\nCreating JSON...")
    df.to_json(
        json_path,
        orient="records",
        date_format="iso",
    )

    print(f"JSON created: {json_path}")

    print("\nSource format generation complete.")


if __name__ == "__main__":
    create_source_formats()