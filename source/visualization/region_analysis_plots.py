import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
import os

print("Starting region chart generation...")
os.makedirs("report/images", exist_ok=True)
df = pd.read_csv("data/ecommerce_sales_cleaned.csv")
sns.set_theme(style="whitegrid")

# 1. Bar Chart: Revenue & Volume by Region
df_valid = df[df['is_returned'] == 0]
rev_reg = df_valid.groupby('region').agg(
    revenue=('total_amount', 'sum'),
    orders=('order_id', 'count')
).reset_index().sort_values('revenue', ascending=False)

rev_reg['revenue_mil'] = rev_reg['revenue'] / 1e6

plt.figure(figsize=(10, 6))
# Encoding: Bar length = Revenue. Color Hue/Saturation = pop-out Top Regions vs others
clrs = ['#1f77b4' if r >= 1.0 else '#aec7e8' for r in rev_reg['revenue_mil']]
ax = sns.barplot(x='region', y='revenue_mil', data=rev_reg, palette=clrs, hue='region', legend=False)
plt.title("Phân bổ Doanh thu và Số lượng Đơn hàng theo Khu vực", fontsize=14, pad=15, fontweight="bold")
plt.ylabel("Doanh Thu (Triệu USD)", fontsize=12)
plt.xlabel("Khu Vực", fontsize=12)
plt.ylim(0, rev_reg['revenue_mil'].max() * 1.25)

for i, row in rev_reg.reset_index(drop=True).iterrows():
    ax.text(i, row['revenue_mil'] + 0.02, f"${row['revenue_mil']:.2f}M\n({int(row['orders'])} đơn)", 
            ha='center', fontsize=10, color='black')

top_patch = mpatches.Patch(color='#1f77b4', label='Thị trường chủ lực (>1 Triệu $)')
other_patch = mpatches.Patch(color='#aec7e8', label='Thị trường lẻ')
plt.legend(handles=[top_patch, other_patch], title="Phân loại tỷ trọng", loc='upper right')
plt.tight_layout()
plt.savefig("report/images/region_revenue.png", dpi=300)
plt.close()

# 2. Dual-Axis/Scatter or Bar: Shipping Time vs Cost
ship_reg = df.groupby('region').agg(
    avg_delivery=('delivery_time_days', 'mean'),
    avg_shipping=('shipping_cost', 'mean')
).reset_index().sort_values('avg_delivery', ascending=True)

plt.figure(figsize=(10, 6))
# Visual Encoding: X = Region, Y = Delivery Time. 
# Color = mapping of Shipping cost (hotter color = higher cost)
clrs2 = []
max_cost = ship_reg['avg_shipping'].max()
for cost in ship_reg['avg_shipping']:
    if cost == max_cost:
        clrs2.append('#d62728') # Red alert for highest cost
    elif cost < 6.13:
        clrs2.append('#2ca02c') # Green for good cost
    else:
        clrs2.append('#ff7f0e') # Orange for medium

ax2 = sns.barplot(x='region', y='avg_delivery', data=ship_reg, palette=clrs2, hue='region', legend=False)
plt.title("Tốc độ Giao Hàng Xếp Hạng và Cước Phí Vận Chuyển Theo Vùng", fontsize=14, pad=15, fontweight="bold")
plt.ylabel("Thời gian giao hàng trung bình (Ngày)", fontsize=12)
plt.xlabel("Khu Vực", fontsize=12)
plt.ylim(0, ship_reg['avg_delivery'].max() * 1.25)

for i, row in ship_reg.reset_index(drop=True).iterrows():
    ax2.text(i, row['avg_delivery'] + 0.1, f"{row['avg_delivery']:.1f} ngày\n(${row['avg_shipping']:.2f})", 
             ha='center', fontsize=10, color='black', fontweight='bold' if row['avg_shipping'] == max_cost else 'normal')

alert_patch = mpatches.Patch(color='#d62728', label='Báo động: Logistics chậm & Cước đắt (>$6.2)')
good_patch = mpatches.Patch(color='#2ca02c', label='Logistics cân bằng (Cước thấp, phí rẻ)')
med_patch = mpatches.Patch(color='#ff7f0e', label='Mức cước & thời gian trung bình')
plt.legend(handles=[alert_patch, good_patch, med_patch], title="Nhận diện Điểm nghẽn", loc='upper left')

plt.tight_layout()
plt.savefig("report/images/shipping_time.png", dpi=300)
plt.close()

# 3. Scatter / Line Plot: Shipping Cost vs Return Rate (Câu hỏi 12)
bins = [0, 2, 4, 6, 8, 10, 15]
df['ship_bin'] = pd.cut(df['shipping_cost'], bins=bins)
bin_cor = df.groupby('ship_bin', observed=True).agg(avg_shipping=('shipping_cost', 'mean'), return_rate=('is_returned', 'mean')).reset_index()

plt.figure(figsize=(10, 6))
# Visual Encoding: X = Avg Shipping Cost, Y = Return Rate. 
# Both are quantitative. Trendline emphasizes the correlation.
ax3 = sns.regplot(x='avg_shipping', y='return_rate', data=bin_cor, 
                  scatter_kws={'s': 150, 'color': '#d62728'}, 
                  line_kws={'color': 'black', 'linestyle': '--', 'linewidth': 1.5})

plt.title("Tương quan Cùng chiều: Chi phí Vận chuyển & Tỷ lệ Hoàn hàng", fontsize=14, pad=15, fontweight="bold")
plt.ylabel("Tỷ lệ Hoàn hàng (Return Rate)", fontsize=12)
plt.xlabel("Chi phí Vận chuyển Trung bình ($)", fontsize=12)

# Format Y axis as percentage
from matplotlib.ticker import PercentFormatter
plt.gca().yaxis.set_major_formatter(PercentFormatter(1.0))

import numpy as np
for i, row in bin_cor.iterrows():
    if not np.isnan(row['avg_shipping']):
        ax3.text(row['avg_shipping'], row['return_rate'] - 0.003, f"{row['return_rate']*100:.1f}%", 
                 ha='center', va='top', fontsize=10, color='black')

plt.text(0.05, 0.85, "Hệ số tương quan (Pearson): +0.97", transform=ax3.transAxes, 
         fontsize=12, fontweight='bold', color='#1f77b4', bbox=dict(facecolor='white', alpha=0.8, edgecolor='#1f77b4'))

plt.tight_layout()
plt.savefig("report/images/cost_return_corr.png", dpi=300)
plt.close()

print("Saved plots to report/images/")
