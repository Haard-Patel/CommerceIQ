from decimal import Decimal

from etl.config import DB_CONFIG
from etl.load import get_connection


EXPECTED_COUNTS = {
    "customers": 4_372,
    "products": 4_070,
    "orders": 25_900,
    "order_items": 536_641,
    "dim_date": 305,
    "dim_country": 38,
    "fact_sales": 536_641,
}


def verify_row_counts(cursor) -> None:
    """
    Verify that each analytical table contains the expected
    number of records.

    This checks whether the database load produced the same
    record counts as the validated ETL output.
    """

    print("\n========================================")
    print("ROW COUNT VERIFICATION")
    print("========================================")

    all_passed = True

    for table_name, expected_count in EXPECTED_COUNTS.items():
        query = f"SELECT COUNT(*) FROM {table_name}"

        cursor.execute(query)
        actual_count = cursor.fetchone()[0]

        passed = actual_count == expected_count

        status = "PASS" if passed else "FAIL"

        print(
            f"{status}: {table_name:<15} "
            f"expected={expected_count:,} "
            f"actual={actual_count:,}"
        )

        if not passed:
            all_passed = False

    if not all_passed:
        raise AssertionError(
            "One or more table row counts do not match expectations."
        )


def verify_primary_keys(cursor) -> None:
    """
    Verify that identifiers used as primary-key-like fields
    contain no duplicates.
    """

    print("\n========================================")
    print("PRIMARY KEY VERIFICATION")
    print("========================================")

    checks = {
        "customers.customer_id": """
            SELECT COUNT(*) - COUNT(DISTINCT customer_id)
            FROM customers
        """,
        "products.product_id": """
            SELECT COUNT(*) - COUNT(DISTINCT product_id)
            FROM products
        """,
        "orders.order_id": """
            SELECT COUNT(*) - COUNT(DISTINCT order_id)
            FROM orders
        """,
        "dim_date.date_key": """
            SELECT COUNT(*) - COUNT(DISTINCT date_key)
            FROM dim_date
        """,
        "dim_country.country_key": """
            SELECT COUNT(*) - COUNT(DISTINCT country_key)
            FROM dim_country
        """,
    }

    for name, query in checks.items():
        cursor.execute(query)
        duplicate_count = cursor.fetchone()[0]

        if duplicate_count != 0:
            raise AssertionError(
                f"{name} contains {duplicate_count} duplicate records."
            )

        print(f"PASS: {name} has no duplicate keys")


def verify_foreign_keys(cursor) -> None:
    """
    Verify that analytical relationships do not contain
    orphaned records.
    """

    print("\n========================================")
    print("FOREIGN KEY VERIFICATION")
    print("========================================")

    checks = {
        "order_items → orders": """
            SELECT COUNT(*)
            FROM order_items oi
            LEFT JOIN orders o
                ON oi.order_id = o.order_id
            WHERE o.order_id IS NULL
        """,

        "order_items → products": """
            SELECT COUNT(*)
            FROM order_items oi
            LEFT JOIN products p
                ON oi.product_id = p.product_id
            WHERE p.product_id IS NULL
        """,

        "fact_sales → orders": """
            SELECT COUNT(*)
            FROM fact_sales fs
            LEFT JOIN orders o
                ON fs.order_id = o.order_id
            WHERE o.order_id IS NULL
        """,

        "fact_sales → products": """
            SELECT COUNT(*)
            FROM fact_sales fs
            LEFT JOIN products p
                ON fs.product_id = p.product_id
            WHERE p.product_id IS NULL
        """,

        "fact_sales → dates": """
            SELECT COUNT(*)
            FROM fact_sales fs
            LEFT JOIN dim_date d
                ON fs.date_key = d.date_key
            WHERE d.date_key IS NULL
        """,

        "fact_sales → countries": """
            SELECT COUNT(*)
            FROM fact_sales fs
            LEFT JOIN dim_country c
                ON fs.country_key = c.country_key
            WHERE c.country_key IS NULL
        """,
    }

    for relationship, query in checks.items():
        cursor.execute(query)
        orphan_count = cursor.fetchone()[0]

        if orphan_count != 0:
            raise AssertionError(
                f"{relationship} contains {orphan_count} orphaned records."
            )

        print(f"PASS: {relationship}")


def verify_revenue_calculations(cursor) -> None:
    """
    Verify that revenue values stored in analytical tables
    are mathematically consistent with quantity and unit price.
    """

    print("\n========================================")
    print("REVENUE VERIFICATION")
    print("========================================")

    cursor.execute("""
        SELECT COUNT(*)
        FROM order_items
        WHERE line_revenue != quantity * unit_price
    """)

    order_item_mismatches = cursor.fetchone()[0]

    if order_item_mismatches != 0:
        raise AssertionError(
            f"Found {order_item_mismatches:,} invalid order item revenue calculations."
        )

    print("PASS: order_items.line_revenue = quantity × unit_price")

    cursor.execute("""
        SELECT COUNT(*)
        FROM fact_sales
        WHERE revenue != quantity * unit_price
    """)

    fact_sales_mismatches = cursor.fetchone()[0]

    if fact_sales_mismatches != 0:
        raise AssertionError(
            f"Found {fact_sales_mismatches:,} invalid fact sales revenue calculations."
        )

    print("PASS: fact_sales.revenue = quantity × unit_price")


def verify_fact_sales_consistency(cursor) -> None:
    """
    Verify that fact_sales and order_items represent the same
    number of analytical transaction rows.
    """

    print("\n========================================")
    print("FACT TABLE CONSISTENCY")
    print("========================================")

    cursor.execute("""
        SELECT
            (SELECT COUNT(*) FROM order_items),
            (SELECT COUNT(*) FROM fact_sales)
    """)

    order_item_count, fact_sales_count = cursor.fetchone()
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM fact_sales
        WHERE is_valid_sale = TRUE
        """
    )

    valid_sale_count = cursor.fetchone()[0]

    assert valid_sale_count == 524_878, (
        f"Expected 524,878 valid sales, "
        f"got {valid_sale_count:,}"
    )

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM fact_sales
        WHERE is_valid_sale = TRUE
          AND (
              quantity <= 0
              OR unit_price <= 0
              OR is_cancelled = TRUE
          )
        """
    )

    invalid_marked_as_valid = cursor.fetchone()[0]

    assert invalid_marked_as_valid == 0, (
        "Found fact_sales rows incorrectly marked as valid sales"
    )

    print("Valid-sale count: 524,878")
    print("Valid-sale business rules: passed")

    print(f"Order items: {order_item_count:,}")
    print(f"Fact sales:  {fact_sales_count:,}")

    if order_item_count != fact_sales_count:
        raise AssertionError(
            "order_items and fact_sales row counts do not match."
        )

    print("PASS: order_items and fact_sales row counts match")


def verify_database() -> None:
    """
    Run all CommerceIQ PostgreSQL database verification checks.
    """

    print("\n")
    print("============================================================")
    print("          COMMERCEIQ DATABASE VERIFICATION")
    print("============================================================")

    connection = None

    try:
        print("\nConnecting to PostgreSQL...")

        connection = get_connection()

        print("PostgreSQL connection established.")

        with connection.cursor() as cursor:
            verify_row_counts(cursor)
            verify_primary_keys(cursor)
            verify_foreign_keys(cursor)
            verify_revenue_calculations(cursor)
            verify_fact_sales_consistency(cursor)

        print("\n")
        print("============================================================")
        print("       COMMERCEIQ DATABASE VERIFICATION PASSED")
        print("============================================================")

    except Exception as error:
        print("\n")
        print("============================================================")
        print("       COMMERCEIQ DATABASE VERIFICATION FAILED")
        print("============================================================")

        print(f"\nError: {error}")

        raise

    finally:
        if connection is not None:
            connection.close()
            print("\nPostgreSQL connection closed.")


if __name__ == "__main__":
    verify_database()