import pandas as pd
import os

print("Starting data cleaning process...")

# Load raw data
raw_path = "ecommerce_sales_34500.csv"
if not os.path.exists(raw_path):
    print(f"Error: {raw_path} not found!")
    exit(1)

df = pd.read_csv(raw_path)
print(f"Original data shape: {df.shape}")

# 1. Drop duplicates
initial_len = len(df)
df = df.drop_duplicates()
print(f"Removed {initial_len - len(df)} duplicate rows. New shape: {df.shape}")

# 2. Check Missing values
print("\nMissing values before cleaning:")
print(df.isna().sum())

# Drop rows where critical columns (like order_id) are missing
df = df.dropna(subset=['order_id', 'customer_id'])

# For numerical columns, fill with median if necessary
numeric_cols = ['price', 'discount', 'quantity', 'total_amount', 'shipping_cost', 'profit_margin']
for col in numeric_cols:
    if col in df.columns and df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].median())

# 3. Data type conversion
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df = df.dropna(subset=['order_date'])

# 4. Feature engineering (derived variables)
df['order_year'] = df['order_date'].dt.year
df['order_month'] = df['order_date'].dt.month
df['order_quarter'] = df['order_date'].dt.quarter
df['order_day_of_week'] = df['order_date'].dt.day_name()

# Add binary return column for easier aggregation
if 'returned' in df.columns:
    df['is_returned'] = df['returned'].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)

# 5. Review and Save Output
print("\nFinal data shape:", df.shape)

output_dir = "data"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "ecommerce_sales_cleaned.csv")

df.to_csv(output_path, index=False)
print(f"\nData successfully cleaned and saved to: {output_path}")

# Preview data
print("\nSample derived features preview:")
print(df[['order_id', 'order_date', 'order_month', 'returned', 'is_returned']].head())
