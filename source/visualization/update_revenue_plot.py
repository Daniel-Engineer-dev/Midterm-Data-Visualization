import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# Ensure image directory exists
os.makedirs("report/images", exist_ok=True)

# Load data
df = pd.read_csv("data/ecommerce_sales_cleaned.csv")
df["order_date"] = pd.to_datetime(df["order_date"])

# Process data by month
df["month_year"] = df["order_date"].dt.to_period("M")
monthly_revenue = df.groupby("month_year")["total_amount"].sum().reset_index()
monthly_revenue["month_year_dt"] = monthly_revenue["month_year"].dt.to_timestamp()

# Plotting with larger fonts and NO seaborn for maximum compatibility
plt.figure(figsize=(14, 8))
plt.grid(True, linestyle="--", alpha=0.7)

# 1. Main Trend Line
plt.plot(
    monthly_revenue["month_year_dt"],
    monthly_revenue["total_amount"],
    marker="o",
    markersize=8,
    linewidth=3,
    color="#2c3e50",
    label="Doanh thu hàng tháng",
)

# 4. Update Title size
plt.title(
    "Xu hướng Doanh thu hàng tháng (2023 - 2025)",
    fontsize=18,
    fontweight="bold",
    pad=25,
)

# 5. Update Axis Labels size
plt.xlabel("Tháng/Năm", fontsize=15, labelpad=15)
plt.ylabel("Tổng Doanh thu ($)", fontsize=15, labelpad=15)

# 6. Update Scale/Tick size
plt.xticks(rotation=45, fontsize=13)
plt.yticks(fontsize=13)

# Add more space at top for labels
plt.ylim(
    monthly_revenue["total_amount"].min() * 0.85,
    monthly_revenue["total_amount"].max() * 1.2,
)

# Format X axis for dates
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m/%Y"))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))

# Legend and Layout
plt.legend(fontsize=12, loc="upper right", frameon=True)
plt.tight_layout()

# Save the updated image
plt.savefig("report/images/revenue_trend.png", dpi=300)
plt.close()

# ----------------- 2. DAY OF WEEK TREND (IMPROVED) -----------------
import numpy as np
from matplotlib.patches import Patch

# Mapping sang tiếng Việt
dow_mapping = {
    "Monday": "Thứ 2",
    "Tuesday": "Thứ 3",
    "Wednesday": "Thứ 4",
    "Thursday": "Thứ 5",
    "Friday": "Thứ 6",
    "Saturday": "Thứ 7",
    "Sunday": "Chủ nhật",
}

dow_order_vi = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]

# Xử lý dữ liệu
dow_counts = (
    df["order_day_of_week"]
    .map(dow_mapping)
    .value_counts()
    .reindex(dow_order_vi, fill_value=0)
    .reset_index()
)

dow_counts.columns = ["Day", "Orders"]

plt.figure(figsize=(11, 6))
plt.grid(axis="y", linestyle="--", alpha=0.6, zorder=0)

# Dùng trục số để giãn cách đẹp hơn
x = np.arange(len(dow_counts))

# Highlight ngày cao điểm
peak_days_vi = ["Thứ 3", "Thứ 4", "Thứ 5"]
colors = ["#e74c3c" if d in peak_days_vi else "#3498db" for d in dow_counts["Day"]]

bars = plt.bar(
    x, dow_counts["Orders"], color=colors, width=0.55, zorder=3  # 👈 giãn cột
)

# Title + Label
plt.title(
    "Lượng Đơn Hàng Theo Thứ Trong Tuần",
    fontsize=16,
    fontweight="bold",
    pad=20,
)

plt.xlabel("Thứ trong tuần", fontsize=14, labelpad=10)
plt.ylabel("Số lượng đơn hàng", fontsize=14, labelpad=10)

# Tick
plt.xticks(x, dow_counts["Day"], fontsize=12)
plt.yticks(fontsize=12)

# Value labels
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2.0,
        height + 10,
        f"{int(height)}",
        ha="center",
        va="bottom",
        fontsize=11,
        fontweight="bold",
    )

# Legend phía dưới biểu đồ để cân đối
legend_elements = [
    Patch(facecolor="#e74c3c", label="Ngày cao điểm (Thứ 3, Thứ 4, Thứ 5)"),
    Patch(facecolor="#3498db", label="Ngày bình thường"),
]

plt.legend(
    handles=legend_elements,
    fontsize=11,
    loc="upper center",
    bbox_to_anchor=(0.5, -0.15),
    ncol=2,
    title="Phân loại",
    title_fontsize=12,
    frameon=True,
)

plt.tight_layout()
# plt.subplots_adjust(left=0.1, right=0.75) # Bỏ phần này để biểu đồ không bị lệch trái

plt.savefig("report/images/dow_trend.png", dpi=300, bbox_inches="tight")
plt.close()
