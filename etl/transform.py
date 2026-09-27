import pandas as pd


def transform_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and transform the raw transaction dataset.

    Returns:
        pandas.DataFrame: Cleaned transaction-level dataset.
    """

    data = df.copy()

    print("\nStarting transaction transformation...")
    print(f"Input rows: {len(data):,}")

    # --------------------------------------------------------
    # Standardize column names
    # --------------------------------------------------------

    data.columns = data.columns.str.strip()

    # --------------------------------------------------------
    # Remove exact duplicates
    # --------------------------------------------------------

    duplicate_count = data.duplicated().sum()

    data = data.drop_duplicates().copy()

    print(f"Duplicate rows removed: {duplicate_count:,}")

    # --------------------------------------------------------
    # Standardize text fields
    # --------------------------------------------------------

    data["InvoiceNo"] = data["InvoiceNo"].astype(str).str.strip()
    data["StockCode"] = data["StockCode"].astype(str).str.strip()
    data["Country"] = data["Country"].astype(str).str.strip()

    data["Description"] = (
        data["Description"]
        .astype("string")
        .str.strip()
    )

    # --------------------------------------------------------
    # Convert data types
    # --------------------------------------------------------

    data["InvoiceDate"] = pd.to_datetime(
        data["InvoiceDate"],
        errors="coerce",
    )

    data["Quantity"] = pd.to_numeric(
        data["Quantity"],
        errors="coerce",
    )

    data["UnitPrice"] = pd.to_numeric(
        data["UnitPrice"],
        errors="coerce",
    )

    data["CustomerID"] = pd.to_numeric(
        data["CustomerID"],
        errors="coerce",
    )

    # --------------------------------------------------------
    # Identify cancelled transactions
    # --------------------------------------------------------

    data["IsCancelled"] = (
        data["InvoiceNo"]
        .str.upper()
        .str.startswith("C")
    )

    # --------------------------------------------------------
    # Classify transaction type
    # --------------------------------------------------------

    data["TransactionType"] = "Sale"

    data.loc[
        data["IsCancelled"],
        "TransactionType"
    ] = "Cancellation"

    data.loc[
        data["Quantity"] < 0,
        "TransactionType"
    ] = "Return"

    data.loc[
        data["UnitPrice"] < 0,
        "TransactionType"
    ] = "Adjustment"

    # --------------------------------------------------------
    # Calculate line revenue
    # --------------------------------------------------------

    data["LineRevenue"] = (
        data["Quantity"] * data["UnitPrice"]
    )

    # --------------------------------------------------------
    # Remove rows missing essential transaction fields
    # --------------------------------------------------------

    before_validation = len(data)

    data = data.dropna(
        subset=[
            "InvoiceNo",
            "StockCode",
            "InvoiceDate",
            "Quantity",
            "UnitPrice",
        ]
    ).copy()

    removed_invalid = before_validation - len(data)

    print(
        f"Rows removed during basic validation: "
        f"{removed_invalid:,}"
    )

    print(f"Output rows: {len(data):,}")

    return data


# ============================================================
# CUSTOMERS
# ============================================================

def build_customers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build the customers dimension from transaction data.

    Customer-level metrics only use rows with a known CustomerID.
    """

    customer_data = df.dropna(subset=["CustomerID"]).copy()

    customer_data["CustomerID"] = (
        customer_data["CustomerID"]
        .astype(int)
    )

    customers = (
        customer_data
        .groupby("CustomerID")
        .agg(
            country=("Country", "last"),
            first_order_date=("InvoiceDate", "min"),
            last_order_date=("InvoiceDate", "max"),
            order_count=("InvoiceNo", "nunique"),
            total_revenue=("LineRevenue", "sum"),
        )
        .reset_index()
    )

    customers = customers.rename(
        columns={
            "CustomerID": "customer_id",
        }
    )

    return customers


# ============================================================
# PRODUCTS
# ============================================================

def build_products(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build the products dimension from transaction data.
    """

    products = (
        df.groupby("StockCode")
        .agg(
            description=("Description", "first"),
            first_seen_at=("InvoiceDate", "min"),
            last_seen_at=("InvoiceDate", "max"),
            average_unit_price=("UnitPrice", "mean"),
        )
        .reset_index()
    )

    products = products.rename(
        columns={
            "StockCode": "product_id",
        }
    )

    return products


# ============================================================
# ORDERS
# ============================================================

def build_orders(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build the orders table from transaction data.
    """

    orders = (
        df.groupby("InvoiceNo")
        .agg(
            customer_id=("CustomerID", "first"),
            order_date=("InvoiceDate", "min"),
            country=("Country", "first"),
            is_cancelled=("IsCancelled", "first"),
        )
        .reset_index()
    )

    orders = orders.rename(
        columns={
            "InvoiceNo": "order_id",
        }
    )

    orders["customer_id"] = (
        orders["customer_id"].astype("Int64")
    )

    return orders


# ============================================================
# ORDER ITEMS
# ============================================================

def build_order_items(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build the order items table.
    """

    order_items = df[
        [
            "InvoiceNo",
            "StockCode",
            "Quantity",
            "UnitPrice",
            "LineRevenue",
        ]
    ].copy()

    order_items = order_items.rename(
        columns={
            "InvoiceNo": "order_id",
            "StockCode": "product_id",
            "Quantity": "quantity",
            "UnitPrice": "unit_price",
            "LineRevenue": "line_revenue",
        }
    )

    return order_items


# ============================================================
# DATE DIMENSION
# ============================================================

def build_dim_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build the date dimension.
    """

    dates = (
        df["InvoiceDate"]
        .dt.normalize()
        .drop_duplicates()
        .sort_values()
    )

    dim_date = pd.DataFrame(
        {
            "calendar_date": dates,
        }
    )

    dim_date["date_key"] = (
        dim_date["calendar_date"]
        .dt.strftime("%Y%m%d")
        .astype(int)
    )

    dim_date["year"] = dim_date["calendar_date"].dt.year
    dim_date["quarter"] = dim_date["calendar_date"].dt.quarter
    dim_date["month"] = dim_date["calendar_date"].dt.month
    dim_date["month_name"] = dim_date["calendar_date"].dt.month_name()
    dim_date["week"] = (
        dim_date["calendar_date"]
        .dt.isocalendar()
        .week
        .astype(int)
    )
    dim_date["day"] = dim_date["calendar_date"].dt.day
    dim_date["day_name"] = dim_date["calendar_date"].dt.day_name()

    return dim_date[
        [
            "date_key",
            "calendar_date",
            "year",
            "quarter",
            "month",
            "month_name",
            "week",
            "day",
            "day_name",
        ]
    ].reset_index(drop=True)


# ============================================================
# COUNTRY DIMENSION
# ============================================================

def build_dim_country(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build the country dimension.
    """

    countries = (
        df["Country"]
        .dropna()
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
    )

    dim_country = pd.DataFrame(
        {
            "country_name": countries,
        }
    )

    dim_country.insert(
        0,
        "country_key",
        range(1, len(dim_country) + 1),
    )

    return dim_country


# ============================================================
# FACT SALES
# ============================================================

def build_fact_sales(
    df: pd.DataFrame,
    dim_date: pd.DataFrame,
    dim_country: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the fact sales table.
    """

    fact_sales = df[
        [
            "InvoiceNo",
            "StockCode",
            "CustomerID",
            "InvoiceDate",
            "Country",
            "Quantity",
            "UnitPrice",
            "LineRevenue",
            "IsCancelled",
        ]
    ].copy()

    # --------------------------------------------------------
    # Date key
    # --------------------------------------------------------

    fact_sales["calendar_date"] = (
        fact_sales["InvoiceDate"].dt.normalize()
    )

    fact_sales = fact_sales.merge(
        dim_date[
            [
                "date_key",
                "calendar_date",
            ]
        ],
        on="calendar_date",
        how="left",
    )

    # --------------------------------------------------------
    # Country key
    # --------------------------------------------------------

    fact_sales = fact_sales.merge(
        dim_country[
            [
                "country_key",
                "country_name",
            ]
        ],
        left_on="Country",
        right_on="country_name",
        how="left",
    )

    # --------------------------------------------------------
    # Rename columns
    # --------------------------------------------------------

    fact_sales = fact_sales.rename(
        columns={
            "InvoiceNo": "order_id",
            "StockCode": "product_id",
            "CustomerID": "customer_id",
            "Quantity": "quantity",
            "UnitPrice": "unit_price",
            "LineRevenue": "revenue",
            "IsCancelled": "is_cancelled",
        }
    )

    fact_sales["customer_id"] = (
        fact_sales["customer_id"].astype("Int64")
    )

    # --------------------------------------------------------
    # Select final columns
    # --------------------------------------------------------

    fact_sales = fact_sales[
        [
            "order_id",
            "product_id",
            "customer_id",
            "date_key",
            "country_key",
            "quantity",
            "unit_price",
            "revenue",
            "is_cancelled",
        ]
    ]

    return fact_sales.reset_index(drop=True)