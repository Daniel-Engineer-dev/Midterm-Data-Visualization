"""
Script: cust_analysis_plots.py
Tạo 3 biểu đồ phân tích khách hàng cho Nhóm 3 (tv3_quocviet)
"""

import os, sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter

BASE   = r"d:\Midterm-Data-Visualization"
DATA   = os.path.join(BASE, "data", "ecommerce_sales_cleaned.csv")
IMGDIR = os.path.join(BASE, "report", "images")
os.makedirs(IMGDIR, exist_ok=True)

# Load data and filter non-returned orders for accurate spend calculation
df = pd.read_csv(DATA)
df_valid = df[df['is_returned'] == 0].copy()

bins   = [18, 25, 35, 45, 55, 70]
labels = ['18–24', '25–34', '35–44', '45–54', '55–69']
df_valid['age_group'] = pd.cut(df_valid['customer_age'], bins=bins, labels=labels, right=False)

COLORS_GENDER = {'Female': '#D63384', 'Male': '#0D6EFD', 'Other': '#7C3AED'}

# PLOT 1: Grouped bar
t2 = (df_valid.groupby(['age_group', 'customer_gender'], observed=True)['total_amount']
        .sum().unstack(fill_value=0) / 1000)

fig, ax = plt.subplots(figsize=(12, 6))
x      = np.arange(len(t2.index))
width  = 0.24
genders = ['Female', 'Male', 'Other']

for i, g in enumerate(genders):
    offset = (i - 1) * width
    bars = ax.bar(x + offset, t2[g], width,
                  label=g, color=COLORS_GENDER[g], alpha=0.88,
                  edgecolor='white', linewidth=0.6, zorder=3)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 6,
                f'${h:.0f}K', ha='center', va='bottom',
                fontsize=7.5, fontweight='bold', color=COLORS_GENDER[g])

ax.set_xlabel('Nhóm tuổi', fontsize=12, labelpad=6)
ax.set_ylabel('Tổng chi tiêu (nghìn USD)', fontsize=12, labelpad=6)
ax.set_title('Tổng Chi Tiêu Kích Hoạt theo Nhóm Tuổi và Giới Tính', fontsize=14,
             fontweight='bold', pad=14)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=11)
ax.legend(title='Giới tính', fontsize=10, title_fontsize=11,
          framealpha=0.9, loc='upper left')
ax.set_facecolor('#F8F9FA')
fig.patch.set_facecolor('white')
ax.grid(axis='y', linestyle='--', alpha=0.45, zorder=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'${v:.0f}K'))

plt.tight_layout()
plt.savefig(os.path.join(IMGDIR, 'cust_spend_age_gender.png'), dpi=150, bbox_inches='tight')
plt.close()

# PLOT 2: Heatmap
# Tỉ lệ này nên tính trên toàn bộ df hay df_valid? Thường thói quen thanh toán tính trên toàn bộ orders cũng được, nhưng ta dùng df sẽ nhất quán. Thực tế heatmap dùng df để xem sở thích là đúng. Tuy nhiên dùng df_valid cũng tương tự.
t6     = (df_valid.groupby(['age_group', 'payment_method'], observed=True)
            .size().unstack(fill_value=0))
t6_pct = t6.div(t6.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(11, 5))
im = ax.imshow(t6_pct.values, cmap='Blues', aspect='auto',
               vmin=0, vmax=t6_pct.values.max() * 1.05)

ax.set_xticks(range(len(t6_pct.columns)))
ax.set_xticklabels(t6_pct.columns, rotation=20, ha='right', fontsize=11)
ax.set_yticks(range(len(t6_pct.index)))
ax.set_yticklabels(t6_pct.index, fontsize=11)

for i in range(len(t6_pct.index)):
    for j in range(len(t6_pct.columns)):
        val   = t6_pct.values[i, j]
        color = 'white' if val > 28 else 'black'
        ax.text(j, i, f'{val:.1f}%', ha='center', va='center',
                fontsize=10, fontweight='bold', color=color)

cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
cbar.set_label('Tỉ lệ (%)', fontsize=10)
ax.set_title('Heatmap: Tỉ lệ Phương thức Thanh toán theo Nhóm Tuổi (%)',
             fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Phương thức thanh toán', fontsize=12)
ax.set_ylabel('Nhóm tuổi', fontsize=12)
fig.patch.set_facecolor('white')

plt.tight_layout()
plt.savefig(os.path.join(IMGDIR, 'cust_payment_heatmap.png'), dpi=150, bbox_inches='tight')
plt.close()

# PLOT 3: Horizontal bar - Top 10 (Strictly by customer_id, regardless of demographic inconsistencies)
top_c = (df_valid.groupby('customer_id')
         ['total_amount'].sum().sort_values(ascending=False).head(10).reset_index())

top_c = top_c.sort_values('total_amount', ascending=True)

fig, ax = plt.subplots(figsize=(11, 6.5))
# Use exactly one cohesive color
bars = ax.barh(range(len(top_c)), top_c['total_amount'],
               color='#1A5276', alpha=0.88, edgecolor='white', linewidth=0.6,
               height=0.65)

for bar, (_, row) in zip(bars, top_c.iterrows()):
    ax.text(bar.get_width() + 50, bar.get_y() + bar.get_height() / 2,
            f'${row["total_amount"]:,.0f}', va='center', fontsize=10, fontweight='bold')

ytick_labels = top_c['customer_id'].tolist()
ax.set_yticks(range(len(top_c)))
ax.set_yticklabels(ytick_labels, fontsize=11, fontweight='bold')
ax.set_xlabel('Tổng chi tiêu tổng hợp từ mọi đơn hàng hợp lệ ($)', fontsize=12, labelpad=6)
ax.set_title('Top 10 Mã Khách hàng có Tổng Chi tiêu Cao nhất', fontsize=14,
             fontweight='bold', pad=14)
ax.set_facecolor('#F8F9FA')
fig.patch.set_facecolor('white')
ax.grid(axis='x', linestyle='--', alpha=0.45, zorder=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(os.path.join(IMGDIR, 'cust_top10.png'), dpi=150, bbox_inches='tight')
plt.close()

print('Charts correctly mapped.')
