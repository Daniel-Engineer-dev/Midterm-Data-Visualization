import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
import numpy as np
import os

print("Starting chart generation process...")

# Ensure directories exist
os.makedirs("report/images", exist_ok=True)

# Load cleaned data
df = pd.read_csv("data/ecommerce_sales_cleaned.csv")
print(f"Data loaded successfully: {df.shape[0]} rows.")

# Set visual style
sns.set_theme(style="whitegrid")

# 1. Bar Chart: Revenue by Category
revenue_by_cat = df.groupby('category')['total_amount'].sum().sort_values(ascending=False).reset_index()

plt.figure(figsize=(10, 6))
# Popout effect: Highlight the highest revenue category
clrs = ['#e74c3c' if x == revenue_by_cat['total_amount'].max() else '#3498db' for x in revenue_by_cat['total_amount']]
ax = sns.barplot(x='category', y='total_amount', data=revenue_by_cat, palette=clrs, hue='category', legend=False)
plt.title("Tổng Doanh Thu Theo Danh Mục Sản Phẩm", fontsize=14, pad=15, fontweight="bold")
plt.ylabel("Doanh Thu ($)", fontsize=12)
plt.xlabel("Danh Mục", fontsize=12)
plt.xticks(rotation=45)

for i, v in enumerate(revenue_by_cat['total_amount']):
    ax.text(i, v + (v*0.01), f'${v:,.0f}', ha='center', fontsize=10)

# Legend Note
top_rev = mpatches.Patch(color='#e74c3c', label='Nhóm Doanh thu cao nhất')
other_rev = mpatches.Patch(color='#3498db', label='Nhóm khác')
plt.legend(handles=[top_rev, other_rev], title="Chú thích", loc='upper right')

plt.tight_layout()
plt.savefig("report/images/cat_revenue.png", dpi=300)
plt.close()


# 2. Return Rate by Category
return_by_cat = df.groupby('category').agg(
    total_orders=('order_id', 'count'),
    returned_orders=('is_returned', 'sum')
).reset_index()
return_by_cat['return_rate'] = (return_by_cat['returned_orders'] / return_by_cat['total_orders']) * 100
return_by_cat = return_by_cat.sort_values(by='return_rate', ascending=False)

plt.figure(figsize=(10, 6))
# Popout effect: Highlight highest return rate
clrs_ret = ['#c0392b' if x == return_by_cat['return_rate'].max() else '#95a5a6' for x in return_by_cat['return_rate']]
ax2 = sns.barplot(x='category', y='return_rate', data=return_by_cat, palette=clrs_ret, hue='category', legend=False)
plt.title("Tỷ Lệ Hoàn Trả Theo Danh Mục (%)", fontsize=14, pad=15, fontweight="bold")
plt.ylabel("Tỷ Lệ Hoàn Trả (%)", fontsize=12)
plt.xlabel("Danh Mục", fontsize=12)
plt.xticks(rotation=45)

for i, v in enumerate(return_by_cat['return_rate']):
    ax2.text(i, v + 0.1, f'{v:.1f}%', ha='center', fontsize=10)

# Legend Note
top_ret = mpatches.Patch(color='#c0392b', label='Rủi ro hoàn trả cao nhất')
other_ret = mpatches.Patch(color='#95a5a6', label='Bình thường')
plt.legend(handles=[top_ret, other_ret], title="Chú thích", loc='upper right')

plt.tight_layout()
plt.savefig("report/images/cat_return_rate.png", dpi=300)
plt.close()


# 3. Scatter/Bubble Chart: Discount vs Profit
discount_stats = df.groupby('discount').agg(
    avg_profit_margin=('profit_margin', 'mean'),
    total_revenue=('total_amount', 'sum'),
    order_count=('order_id', 'count')
).reset_index()

discount_stats['discount_pct'] = discount_stats['discount'] * 100
discount_stats = discount_stats.sort_values('discount_pct')

plt.figure(figsize=(10, 6))
# Using line + scatter to show trend clearly
plt.plot(discount_stats['discount_pct'], discount_stats['avg_profit_margin'], color='gray', linestyle='--', zorder=1)

# Popout: Highlight 0% discount
colors = ['#27ae60' if d == 0 else '#e67e22' for d in discount_stats['discount_pct']]

scatter = plt.scatter(
    x=discount_stats['discount_pct'], 
    y=discount_stats['avg_profit_margin'], 
    s=discount_stats['order_count'] * 0.3, # Size slightly scaled down
    c=colors,
    alpha=0.9,
    zorder=2
)

plt.title("Biên Lợi Nhuận Trung Bình Theo Mức Giảm Giá", fontsize=14, pad=15, fontweight="bold")
plt.ylabel("Biên Lợi Nhuận Trung Bình ($)", fontsize=12)
plt.xlabel("Mức Giảm Giá (%)", fontsize=12)

for i, row in discount_stats.iterrows():
    # Adjust overlap for 0 by pushing the text down and right
    if row['discount_pct'] == 0:
        y_offset = -15
        x_offset = 35
    else:
        y_offset = -8
        x_offset = 20
        
    plt.annotate(f"{int(row['order_count'])} đơn", 
                 (row['discount_pct'], row['avg_profit_margin']),
                 xytext=(x_offset, y_offset), textcoords='offset points', fontsize=9)

# Added neat Legend replacing the hardcoded floating text
zero_disc = mpatches.Patch(color='#27ae60', label='Không giảm giá (0%)\nHiệu quả cao nhất')
other_disc = mpatches.Patch(color='#e67e22', label='Có giảm giá')
plt.legend(handles=[zero_disc, other_disc], title="Chú thích", loc='upper right')

# Increase margins to prevent large scatter points from being cut off
plt.margins(0.15) 

plt.tight_layout()
plt.savefig("report/images/discount_profit.png", dpi=300, bbox_inches='tight')
plt.close()

print("\nDone generating charts with neat legends and fixed labels! Images saved to report/images/")
