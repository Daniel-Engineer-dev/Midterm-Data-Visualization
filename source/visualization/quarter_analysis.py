import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Cấu hình
os.makedirs("report/images", exist_ok=True)
data_path = "data/ecommerce_sales_cleaned.csv"

# Load dữ liệu
df = pd.read_csv(data_path)
df["order_date"] = pd.to_datetime(df["order_date"])

# Tạo cột Quý-Năm (ví dụ: 2024-Q1)
df["quarter_year"] = df["order_date"].dt.to_period("Q").astype(str)

# Tính tổng doanh thu theo Quý
quarter_rev = df.groupby("quarter_year")["total_amount"].sum().reset_index()

# Tính % tăng trưởng so với quý trước (Growth Rate)
quarter_rev["growth_rate"] = quarter_rev["total_amount"].pct_change() * 100

# Vẽ biểu đồ
plt.figure(figsize=(12, 7))
sns.set_theme(style="whitegrid")

# Biểu đồ cột doanh thu (Dùng 1 màu xanh nhạt duy nhất cho toàn bộ các cột)
ax = sns.barplot(
    x="quarter_year",
    y="total_amount",
    data=quarter_rev,
    color="#AED6F1"  # Một màu xanh nhạt duy nhất
)

# Vẽ đường xu hướng (Trendline)
plt.plot(
    range(len(quarter_rev)),
    quarter_rev["total_amount"],
    marker="o",
    color="#E74C3C",  # Màu đỏ đậm hơn
    linestyle="--",
    linewidth=2,
    label="Đường xu hướng",
)

# Thêm ghi chú giá trị và % tăng trưởng
for i, row in quarter_rev.iterrows():
    ax.text(
        i,
        row["total_amount"] + (row["total_amount"] * 0.02),
        f'${row["total_amount"]/1e3:,.1f}K',
        ha="center",
        fontsize=10,
        fontweight="bold",
    )

    # Ghi % tăng trưởng (Tô đậm và dùng màu có độ tương phản cao)
    if not pd.isna(row["growth_rate"]):
        # Xanh lá rất đậm cho tăng, Đỏ rất đậm cho giảm
        growth_color = "#145A32" if row["growth_rate"] > 0 else "#943126"
        plt.annotate(
            f"{row['growth_rate']:+.1f}%",
            xy=(i, row["total_amount"]),
            xytext=(0, -25),
            textcoords="offset points",
            ha="center",
            fontsize=11,
            fontweight="black", # Cực đậm
            color=growth_color,
        )

plt.title(
    "Tổng Doanh Thu và Tốc Độ Tăng Trưởng Theo Quý (2023 - 2025)",
    fontsize=16,
    fontweight="bold",
    pad=20,
)
plt.ylabel("Doanh thu ($)", fontsize=13)
plt.xlabel("Quý - Năm", fontsize=13)
plt.legend()

plt.tight_layout()
plt.savefig("report/images/quarterly_revenue.png", dpi=300)
plt.close()

print("Đã tạo biểu đồ quý tại report/images/quarterly_revenue.png")
