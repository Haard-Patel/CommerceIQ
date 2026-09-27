from etl.extract import extract_data
from etl.transform import transform_transactions


df = extract_data()

transformed_df = transform_transactions(df)

print("\n========================================")
print("TRANSACTION TYPES")
print("========================================")

print(
    transformed_df["TransactionType"]
    .value_counts()
    .to_string()
)

print("\nTransformed columns:")
print(transformed_df.columns.tolist())

print("\nFirst 5 transformed rows:")
print(
    transformed_df[
        [
            "InvoiceNo",
            "StockCode",
            "Quantity",
            "UnitPrice",
            "LineRevenue",
            "IsCancelled",
            "CustomerID",
            "Country",
        ]
    ].head()
)

print("\nFinal shape:")
print(transformed_df.shape)

print("\nCancellation breakdown:")
print(transformed_df["IsCancelled"].value_counts())