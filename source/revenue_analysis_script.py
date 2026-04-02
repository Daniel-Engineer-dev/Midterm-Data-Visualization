import pandas as pd
import os

# Load data
data_path = '../data/ecommerce_sales_cleaned.csv'
if not os.path.exists(data_path):
    data_path = 'data/ecommerce_sales_cleaned.csv'

df = pd.read_csv(data_path)
df['order_date'] = pd.to_datetime(df['order_date'])

# Group by Month-Year
df['month_year'] = df['order_date'].dt.to_period('M')
monthly_revenue = df.groupby('month_year')['total_amount'].sum()

print("--- Doanh thu hàng tháng ---")
print(monthly_revenue)

# Group by Month (Seasonal)
seasonal_revenue = df.groupby('order_month')['total_amount'].mean()
print("\n--- Doanh thu trung bình theo tháng ---")
print(seasonal_revenue)

# Identify peaks and troughs
max_month = seasonal_revenue.idxmax()
min_month = seasonal_revenue.idxmin()

print(f"\nTháng cao điểm: {max_month}")
print(f"Tháng thấp điểm: {min_month}")

# Yearly Trend
yearly_revenue = df.groupby('order_year')['total_amount'].sum()
print("\n--- Doanh thu hàng năm ---")
print(yearly_revenue)
