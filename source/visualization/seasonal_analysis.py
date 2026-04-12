import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib.patches as mpatches

# Cấu hình đường dẫn
os.makedirs("report/images", exist_ok=True)
data_path = "data/ecommerce_sales_cleaned.csv"

# Load dữ liệu
df = pd.read_csv(data_path)
df["order_date"] = pd.to_datetime(df["order_date"])

# Chuyển tên tháng sang tiếng Việt
month_mapping_vi = {
    1: "Tháng 1",
    2: "Tháng 2",
    3: "Tháng 3",
    4: "Tháng 4",
    5: "Tháng 5",
    6: "Tháng 6",
    7: "Tháng 7",
    8: "Tháng 8",
    9: "Tháng 9",
    10: "Tháng 10",
    11: "Tháng 11",
    12: "Tháng 12",
}

# Tính doanh thu trung bình theo tháng (Mùa vụ)
# Logic: Phải tính Tổng doanh thu theo từng Tháng-Năm trước, sau đó mới tính Trung bình của các tổng đó theo Tháng
# Điều này giúp khớp với Dashboard và phản ánh đúng quy mô doanh thu thay vì trung bình trên mỗi đơn hàng.
df['year'] = df['order_date'].dt.year
monthly_totals = df.groupby(['year', 'order_month'])['total_amount'].sum().reset_index()
seasonal_data = monthly_totals.groupby('order_month')['total_amount'].mean().reset_index()
seasonal_data["Month_VI"] = seasonal_data["order_month"].map(month_mapping_vi)

# Sắp xếp theo thứ tự tháng 1-12
seasonal_data = seasonal_data.sort_values("order_month")

# Vẽ biểu đồ
plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")

# Highlight các điểm cao nhất và thấp nhất theo yêu cầu
# Tháng 4, 10, 12 là cao điểm (Đỏ)
# Tháng 9 là thấp điểm (Xám đậm)
colors = []
for m in seasonal_data["order_month"]:
    if m in [4, 10, 12]:
        colors.append("#e74c3c")  # Đỏ cho cao điểm
    elif m == 9:
        colors.append("#34495e")  # Xám đậm cho thấp điểm (T9)
    else:
        colors.append("#3498db")  # Xanh cho bình thường

ax = sns.barplot(
    x="Month_VI",
    y="total_amount",
    data=seasonal_data,
    palette=colors,
    hue="Month_VI",
    legend=False,
)

# Thêm tiêu đề và nhãn
plt.title(
    "Doanh thu Trung bình Theo Tháng (Tính Mùa Vụ 2023 - 2025)",
    fontsize=16,
    fontweight="bold",
    pad=20,
)
plt.ylabel("Doanh thu Trung bình ($)", fontsize=13)
plt.xlabel("Tháng trong năm", fontsize=13)
plt.xticks(rotation=30)

# Thêm ghi chú giá trị trên đầu cột
for i, v in enumerate(seasonal_data["total_amount"]):
    ax.text(
        i, v + (v * 0.01), f"${v:,.0f}", ha="center", fontsize=10, fontweight="bold"
    )

# Legend giải thích màu sắc (Đưa xuống dưới biểu đồ)
peak_patch = mpatches.Patch(color="#e74c3c", label="Tháng Cao điểm")
normal_patch = mpatches.Patch(color="#3498db", label="Trung bình")
low_patch = mpatches.Patch(color="#34495e", label="Tháng Thấp điểm")
plt.legend(
    handles=[peak_patch, normal_patch, low_patch],
    loc="upper center",
    bbox_to_anchor=(0.5, -0.25),  # Kéo Legend gần lại biểu đồ hơn
    ncol=3,  # Xếp thành hàng ngang
    title="Phân loại mùa vụ",
)

plt.tight_layout()
plt.savefig("report/images/seasonal_revenue.png", dpi=300)
plt.close()

print("Đã tạo biểu đồ mùa vụ tại report/images/seasonal_revenue.png")
