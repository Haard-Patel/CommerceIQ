from etl.extract import extract_data

from etl.transform import (
    transform_transactions,
    build_customers,
    build_products,
    build_orders,
    build_order_items,
    build_dim_date,
    build_dim_country,
    build_fact_sales,
)

from etl.validate import validate_transactions

from etl.test_dimensions import validate_analytical_tables

from etl.load import load_all


def run_pipeline():
    """
    Run the complete CommerceIQ ETL pipeline.

    Pipeline stages:

        Extract
        → Transform
        → Validate
        → Build analytical tables
        → Validate analytical relationships
        → Load PostgreSQL
    """

    print("\n")
    print("============================================================")
    print("              COMMERCEIQ ETL PIPELINE")
    print("============================================================")

    # ========================================================
    # 1. EXTRACT
    # ========================================================

    print("\n[1/6] EXTRACT")

    raw_data = extract_data()

    # ========================================================
    # 2. TRANSFORM
    # ========================================================

    print("\n[2/6] TRANSFORM")

    transactions = transform_transactions(
        raw_data
    )

    # ========================================================
    # 3. TRANSACTION VALIDATION
    # ========================================================

    print("\n[3/6] TRANSACTION VALIDATION")

    validate_transactions(
        transactions
    )

    # ========================================================
    # 4. BUILD ANALYTICAL TABLES
    # ========================================================

    print("\n[4/6] BUILD ANALYTICAL TABLES")

    customers = build_customers(
        transactions
    )

    products = build_products(
        transactions
    )

    orders = build_orders(
        transactions
    )

    order_items = build_order_items(
        transactions
    )

    dim_date = build_dim_date(
        transactions
    )

    dim_country = build_dim_country(
        transactions
    )

    fact_sales = build_fact_sales(
        transactions,
        dim_date,
        dim_country,
    )

    # ========================================================
    # 5. ANALYTICAL VALIDATION
    # ========================================================

    print("\n[5/6] ANALYTICAL VALIDATION")

    validate_analytical_tables(
        transactions,
        customers,
        products,
        orders,
        order_items,
        dim_date,
        dim_country,
        fact_sales,
    )

    # ========================================================
    # 6. LOAD POSTGRESQL
    # ========================================================

    print("\n[6/6] LOAD POSTGRESQL")


    load_all(
        customers=customers,
        products=products,
        orders=orders,
        order_items=order_items,
        dim_date=dim_date,
        dim_country=dim_country,
        fact_sales=fact_sales,
    )

    # ========================================================
    # COMPLETE
    # ========================================================

    print("\n")
    print("============================================================")
    print("             COMMERCEIQ ETL PIPELINE COMPLETE")
    print("============================================================")

    print("\nData successfully loaded into PostgreSQL.")
    print("Database: commerceiq")


if __name__ == "__main__":
    run_pipeline()