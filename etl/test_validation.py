from etl.extract import extract_data
from etl.transform import transform_transactions
from etl.validate import validate_transactions


df = extract_data()

transactions = transform_transactions(df)

validate_transactions(transactions)