import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


from etl.config import DB_CONFIG

def to_python_value(value):
    """
    Convert pandas missing values into Python None so that
    psycopg2 can safely send them to PostgreSQL as SQL NULL.

    pandas.NA / NaN / NaT -> None
    Everything else -> unchanged
    """
    if pd.isna(value):
        return None

    return value

def get_connection():
    """
    Create and return a PostgreSQL database connection.
    """

    print("\nConnecting to PostgreSQL...")

    connection = psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
    )

    print("PostgreSQL connection established.")

    return connection


def load_dim_country(cursor, df: pd.DataFrame) -> None:
    """
    Load the country dimension.
    """

    rows = [
        (
            row.country_name,
        )
        for row in df.itertuples(index=False)
    ]

    query = """
        INSERT INTO dim_country (
            country_name
        )
        VALUES %s
    """

    execute_values(
        cursor,
        query,
        rows,
    )

    print(
        f"Loaded dim_country: {len(rows):,} rows"
    )


def load_dim_date(cursor, df: pd.DataFrame) -> None:
    """
    Load the date dimension.
    """

    rows = [
        (
            int(row.date_key),
            row.calendar_date,
            int(row.year),
            int(row.quarter),
            int(row.month),
            row.month_name,
            int(row.week),
            int(row.day),
            row.day_name,
        )
        for row in df.itertuples(index=False)
    ]

    query = """
        INSERT INTO dim_date (
            date_key,
            calendar_date,
            year,
            quarter,
            month,
            month_name,
            week,
            day,
            day_name
        )
        VALUES %s
    """

    execute_values(
        cursor,
        query,
        rows,
    )

    print(
        f"Loaded dim_date: {len(rows):,} rows"
    )


def load_customers(cursor, df: pd.DataFrame) -> None:
    """
    Load the customers dimension.

    Converts pandas missing values into PostgreSQL-compatible NULLs
    before inserting the customer records.
    """

    rows = [
        (
            None
            if pd.isna(row.customer_id)
            else int(row.customer_id),

            to_python_value(row.country),
            to_python_value(row.first_order_date),
            to_python_value(row.last_order_date),

            None
            if pd.isna(row.order_count)
            else int(row.order_count),

            None
            if pd.isna(row.total_revenue)
            else float(row.total_revenue),
        )
        for row in df.itertuples(index=False)
    ]

    query = """
        INSERT INTO customers (
            customer_id,
            country,
            first_order_date,
            last_order_date,
            order_count,
            total_revenue
        )
        VALUES %s
    """

    execute_values(
        cursor,
        query,
        rows,
    )

    print(
        f"Loaded customers: {len(rows):,} rows"
    )
    """
    Load the customers dimension.
    """

    rows = [
        (
            int(row.customer_id),
            row.country,
            row.first_order_date,
            row.last_order_date,
            int(row.order_count),
            float(row.total_revenue),
        )
        for row in df.itertuples(index=False)
    ]

    query = """
        INSERT INTO customers (
            customer_id,
            country,
            first_order_date,
            last_order_date,
            order_count,
            total_revenue
        )
        VALUES %s
    """

    execute_values(
        cursor,
        query,
        rows,
    )

    print(
        f"Loaded customers: {len(rows):,} rows"
    )


def load_products(cursor, df: pd.DataFrame) -> None:
    """
    Load the products dimension.
    """

    rows = [
    (
        to_python_value(row.product_id),
        to_python_value(row.description),
        to_python_value(row.first_seen_at),
        to_python_value(row.last_seen_at),
        to_python_value(row.average_unit_price),
    )
    for row in df.itertuples(index=False)
]

    query = """
        INSERT INTO products (
            product_id,
            description,
            first_seen_at,
            last_seen_at,
            average_unit_price
        )
        VALUES %s
    """

    execute_values(
        cursor,
        query,
        rows,
    )

    print(
        f"Loaded products: {len(rows):,} rows"
    )


def load_orders(cursor, df: pd.DataFrame) -> None:
    """
    Load the orders table.
    """

    rows = [
        (
            to_python_value(row.order_id),

            None
            if pd.isna(row.customer_id)
            else int(row.customer_id),

            to_python_value(row.order_date),
            to_python_value(row.country),

            None
            if pd.isna(row.is_cancelled)
            else bool(row.is_cancelled),
        )
        for row in df.itertuples(index=False)
    ]

    query = """
        INSERT INTO orders (
            order_id,
            customer_id,
            order_date,
            country,
            is_cancelled
        )
        VALUES %s
    """

    execute_values(
        cursor,
        query,
        rows,
        page_size=5000,
    )

    print(
        f"Loaded orders: {len(rows):,} rows"
    )


def load_order_items(cursor, df: pd.DataFrame) -> None:
    """
    Load the order items table.

    order_item_id is generated automatically by PostgreSQL.
    """

    rows = [
    (
        to_python_value(row.order_id),
        to_python_value(row.product_id),

        None
        if pd.isna(row.quantity)
        else int(row.quantity),

        None
        if pd.isna(row.unit_price)
        else float(row.unit_price),

        None
        if pd.isna(row.line_revenue)
        else float(row.line_revenue),
    )
    for row in df.itertuples(index=False)
]

    query = """
        INSERT INTO order_items (
            order_id,
            product_id,
            quantity,
            unit_price,
            line_revenue
        )
        VALUES %s
    """

    execute_values(
        cursor,
        query,
        rows,
        page_size=5000,
    )

    print(
        f"Loaded order_items: {len(rows):,} rows"
    )


def load_fact_sales(cursor, df: pd.DataFrame) -> None:
    """
    Load the sales fact table.

    sales_id is generated automatically by PostgreSQL.
    """

    rows = [
    (
        to_python_value(row.order_id),
        to_python_value(row.product_id),

        None
        if pd.isna(row.customer_id)
        else int(row.customer_id),

        None
        if pd.isna(row.date_key)
        else int(row.date_key),

        None
        if pd.isna(row.country_key)
        else int(row.country_key),

        None
        if pd.isna(row.quantity)
        else int(row.quantity),

        None
        if pd.isna(row.unit_price)
        else float(row.unit_price),

        None
        if pd.isna(row.revenue)
        else float(row.revenue),

        None
        if pd.isna(row.is_cancelled)
        else bool(row.is_cancelled),
    )
    for row in df.itertuples(index=False)
]
    query = """
        INSERT INTO fact_sales (
            order_id,
            product_id,
            customer_id,
            date_key,
            country_key,
            quantity,
            unit_price,
            revenue,
            is_cancelled
        )
        VALUES %s
    """

    execute_values(
        cursor,
        query,
        rows,
        page_size=5000,
    )

    print(
        f"Loaded fact_sales: {len(rows):,} rows"
    )


def load_all(
    customers: pd.DataFrame,
    products: pd.DataFrame,
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    dim_date: pd.DataFrame,
    dim_country: pd.DataFrame,
    fact_sales: pd.DataFrame,
) -> None:
    """
    Load all validated analytical tables into PostgreSQL.

    The entire operation runs inside one database transaction.
    If any table fails to load, all changes are rolled back.
    """

    connection = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        print("\n========================================")
        print("POSTGRESQL DATA LOAD")
        print("========================================")

        # ----------------------------------------------------
        # Load parent/dimension tables first
        # ----------------------------------------------------

        load_dim_country(
            cursor,
            dim_country,
        )

        load_dim_date(
            cursor,
            dim_date,
        )

        load_customers(
            cursor,
            customers,
        )

        load_products(
            cursor,
            products,
        )

        # ----------------------------------------------------
        # Load dependent tables
        # ----------------------------------------------------

        load_orders(
            cursor,
            orders,
        )

        load_order_items(
            cursor,
            order_items,
        )

        load_fact_sales(
            cursor,
            fact_sales,
        )

        # ----------------------------------------------------
        # Commit transaction
        # ----------------------------------------------------

        connection.commit()

        print("\n========================================")
        print("POSTGRESQL LOAD SUCCESSFUL")
        print("========================================")

    except Exception as error:

        if connection is not None:
            connection.rollback()

        print("\n========================================")
        print("POSTGRESQL LOAD FAILED")
        print("========================================")

        print(f"Error: {error}")

        raise

    finally:

        if connection is not None:
            connection.close()

            print(
                "PostgreSQL connection closed."
            )