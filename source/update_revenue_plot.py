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

# 2. Highlight April outlier (Month 4) - Popout effect
outlier_month = pd.Timestamp("2024-04-01")
outlier_data = monthly_revenue[monthly_revenue["month_year_dt"] == outlier_month]
if not outlier_data.empty:
    plt.scatter(
        outlier_data["month_year_dt"],
        outlier_data["total_amount"],
        color="#e74c3c",
        s=250,
        edgecolor="black",
        linewidth=1.5,
        zorder=5,
        label="Điểm đột biến (Tháng 4)",
    )
    plt.annotate(
        "Đột biến (Tháng 4)",
        (outlier_data["month_year_dt"].iloc[0], outlier_data["total_amount"].iloc[0]),
        xytext=(0, 20),
        textcoords="offset points",
        ha="center",
        fontsize=13,
        fontweight="bold",
        color="#c0392b",
    )

# 3. Highlight high season areas
plt.axvspan(
    pd.Timestamp("2023-10-01"),
    pd.Timestamp("2023-12-31"),
    color="green",
    alpha=0.1,
    label="Dịp lễ cuối năm 2023",
)
plt.axvspan(
    pd.Timestamp("2024-10-01"),
    pd.Timestamp("2024-12-31"),
    color="green",
    alpha=0.1,
    label="Dịp lễ cuối năm 2024",
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
plt.ylabel("Tổng Doanh thu (USD)", fontsize=15, labelpad=15)

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

print("Successfully updated revenue_trend.png with outlier highlight and large fonts!")
