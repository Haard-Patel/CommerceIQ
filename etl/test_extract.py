from etl.extract import extract_data


df = extract_data()

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nDataset shape:")
print(df.shape)