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


def validate_analytical_tables(
    transactions,
    customers,
    products,
    orders,
    order_items,
    dim_date,
    dim_country,
    fact_sales,
):
    print("\n========================================")
    print("ANALYTICAL TABLE VALIDATION")
    print("========================================")

    errors = []

    # --------------------------------------------------------
    # Row counts
    # --------------------------------------------------------

    print(f"Transactions: {len(transactions):,}")
    print(f"Customers:    {len(customers):,}")
    print(f"Products:     {len(products):,}")
    print(f"Orders:       {len(orders):,}")
    print(f"Order Items:  {len(order_items):,}")
    print(f"Dates:        {len(dim_date):,}")
    print(f"Countries:    {len(dim_country):,}")
    print(f"Fact Sales:   {len(fact_sales):,}")

    # --------------------------------------------------------
    # Primary key uniqueness
    # --------------------------------------------------------

    if customers["customer_id"].duplicated().any():
        errors.append(
            "Duplicate customer_id values found."
        )

    if products["product_id"].duplicated().any():
        errors.append(
            "Duplicate product_id values found."
        )

    if orders["order_id"].duplicated().any():
        errors.append(
            "Duplicate order_id values found."
        )

    if dim_date["date_key"].duplicated().any():
        errors.append(
            "Duplicate date_key values found."
        )

    if dim_country["country_key"].duplicated().any():
        errors.append(
            "Duplicate country_key values found."
        )

    # --------------------------------------------------------
    # Order item → Order integrity
    # --------------------------------------------------------

    valid_orders = set(orders["order_id"])

    invalid_order_items = (
        ~order_items["order_id"].isin(valid_orders)
    ).sum()

    print(
        f"Order items with invalid order_id: "
        f"{invalid_order_items:,}"
    )

    if invalid_order_items > 0:
        errors.append(
            f"Found {invalid_order_items:,} order items "
            "without a matching order."
        )

    # --------------------------------------------------------
    # Order item → Product integrity
    # --------------------------------------------------------

    valid_products = set(products["product_id"])

    invalid_product_items = (
        ~order_items["product_id"].isin(valid_products)
    ).sum()

    print(
        f"Order items with invalid product_id: "
        f"{invalid_product_items:,}"
    )

    if invalid_product_items > 0:
        errors.append(
            f"Found {invalid_product_items:,} order items "
            "without a matching product."
        )

    # --------------------------------------------------------
    # Fact sales → Date integrity
    # --------------------------------------------------------

    valid_dates = set(dim_date["date_key"])

    invalid_fact_dates = (
        ~fact_sales["date_key"].isin(valid_dates)
    ).sum()

    print(
        f"Fact sales with invalid date_key: "
        f"{invalid_fact_dates:,}"
    )

    if invalid_fact_dates > 0:
        errors.append(
            f"Found {invalid_fact_dates:,} fact sales rows "
            "without a matching date."
        )



    # --------------------------------------------------------
    # Fact sales → Country integrity
    # --------------------------------------------------------

    valid_countries = set(
        dim_country["country_key"]
    )

    invalid_fact_countries = (
        ~fact_sales["country_key"].isin(valid_countries)
    ).sum()

    print(
        f"Fact sales with invalid country_key: "
        f"{invalid_fact_countries:,}"
    )

    if invalid_fact_countries > 0:
        errors.append(
            f"Found {invalid_fact_countries:,} fact sales rows "
            "without a matching country."
        )

    # --------------------------------------------------------
    # Fact sales → Product integrity
    # --------------------------------------------------------

    invalid_fact_products = (
        ~fact_sales["product_id"].isin(valid_products)
    ).sum()

    print(
        f"Fact sales with invalid product_id: "
        f"{invalid_fact_products:,}"
    )

    if invalid_fact_products > 0:
        errors.append(
            f"Found {invalid_fact_products:,} fact sales rows "
            "without a matching product."
        )

    # --------------------------------------------------------
    # Fact sales → Order integrity
    # --------------------------------------------------------

    invalid_fact_orders = (
        ~fact_sales["order_id"].isin(valid_orders)
    ).sum()

    print(
        f"Fact sales with invalid order_id: "
        f"{invalid_fact_orders:,}"
    )

    if invalid_fact_orders > 0:
        errors.append(
            f"Found {invalid_fact_orders:,} fact sales rows "
            "without a matching order."
        )

        print(
        "Fact sales is_valid_sale count:",
        int(fact_sales["is_valid_sale"].sum()),
    )

    expected_valid_sale_count = 524_878

    assert (
        int(fact_sales["is_valid_sale"].sum())
        == expected_valid_sale_count
    ), (
        f"Expected {expected_valid_sale_count:,} valid sales, "
        f"got {int(fact_sales['is_valid_sale'].sum()):,}"
    )

    invalid_marked_as_valid = fact_sales[
        fact_sales["is_valid_sale"]
        & (
            (fact_sales["quantity"] <= 0)
            | (fact_sales["unit_price"] <= 0)
            | fact_sales["is_cancelled"]
        )
    ]

    assert len(invalid_marked_as_valid) == 0, (
        "Found fact_sales rows incorrectly marked as valid sales"
    )

    print("Fact sales valid-sale count matches expected: True")
    print("Fact sales valid-sale business rules: True")

    # --------------------------------------------------------
    # Customer integrity
    # --------------------------------------------------------

    valid_customers = set(
        customers["customer_id"]
    )

    known_fact_customers = (
        fact_sales["customer_id"]
        .dropna()
        .astype(int)
    )

    invalid_fact_customers = (
        ~known_fact_customers.isin(valid_customers)
    ).sum()

    print(
        f"Fact sales with invalid customer_id: "
        f"{invalid_fact_customers:,}"
    )

    if invalid_fact_customers > 0:
        errors.append(
            f"Found {invalid_fact_customers:,} fact sales rows "
            "with an invalid customer_id."
        )

    # --------------------------------------------------------
    # Fact sales row-count consistency
    # --------------------------------------------------------

    if len(fact_sales) != len(transactions):
        errors.append(
            "Fact sales row count does not match "
            "transformed transaction row count."
        )

    print(
        f"Fact sales row count matches transactions: "
        f"{len(fact_sales) == len(transactions)}"
    )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    if errors:
        print("\nVALIDATION FAILED")

        for error in errors:
            print(f" - {error}")

        raise ValueError(
            "Analytical table validation failed."
        )

    print("\nANALYTICAL TABLE VALIDATION PASSED")


# ============================================================
# BUILD DATA
# ============================================================
if __name__ == "__main__":
    df = extract_data()

    transactions = transform_transactions(df)

    customers = build_customers(transactions)
    products = build_products(transactions)
    orders = build_orders(transactions)
    order_items = build_order_items(transactions)
    dim_date = build_dim_date(transactions)
    dim_country = build_dim_country(transactions)

    fact_sales = build_fact_sales(
        transactions,
        dim_date,
        dim_country,
    )

    # ============================================================
    # VALIDATE
    # ============================================================

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