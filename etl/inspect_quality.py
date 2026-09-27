from etl.extract import extract_data
from etl.transform import transform_transactions


df = extract_data()

transactions = transform_transactions(df)


print("\n========================================")
print("NEGATIVE PRICE RECORDS")
print("========================================")

negative_prices = transactions[
    transactions["UnitPrice"] < 0
]

print(
    negative_prices[
        [
            "InvoiceNo",
            "StockCode",
            "Description",
            "Quantity",
            "InvoiceDate",
            "UnitPrice",
            "CustomerID",
            "Country",
            "IsCancelled",
            "LineRevenue",
        ]
    ].to_string(index=False)
)


print("\n========================================")
print("NEGATIVE QUANTITY + CANCELLATION")
print("========================================")

negative_quantity_cancelled = transactions[
    (transactions["Quantity"] < 0)
    & (transactions["IsCancelled"])
]

print(
    f"Rows: {len(negative_quantity_cancelled):,}"
)


print("\n========================================")
print("NEGATIVE QUANTITY WITHOUT CANCELLATION")
print("========================================")

negative_quantity_not_cancelled = transactions[
    (transactions["Quantity"] < 0)
    & (~transactions["IsCancelled"])
]

print(
    f"Rows: {len(negative_quantity_not_cancelled):,}"
)
