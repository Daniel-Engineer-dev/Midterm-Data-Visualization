import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="E-Commerce Sales Dashboard", page_icon="🛒", layout="wide")

@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    data_path = os.path.join(project_dir, 'data', 'ecommerce_sales_cleaned.csv')
    
    if not os.path.exists(data_path):
        st.error(f"Cannot find data file at {data_path}. Please make sure the dataset is available.")
        st.stop()
        
    df = pd.read_csv(data_path)
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

st.title("🛒 E-Commerce Sales Performance Dashboard")
st.markdown("Dashboard phân tích hiệu suất kinh doanh qua các xu hướng thời gian, hành vi khách hàng và phân bổ địa lý.")

# Load data
df = load_data()

# ----------------- SIDEBAR -----------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3144/3144456.png", width=100)
st.sidebar.header("Bộ Lọc Dữ Liệu (Filters)")

region_list = sorted(df['region'].unique().tolist())
selected_regions = st.sidebar.multiselect("Chọn Khu Vực (Region)", region_list, default=region_list)

category_list = sorted(df['category'].unique().tolist())
selected_categories = st.sidebar.multiselect("Chọn Danh Mục (Category)", category_list, default=category_list)

filtered_df = df[df['region'].isin(selected_regions) & df['category'].isin(selected_categories)]

st.sidebar.markdown("---")
st.sidebar.markdown("**Phạm Quang Vinh** (23120202)")
st.sidebar.markdown("*Vai trò: Xử lý & Làm sạch dữ liệu*")

plot_df = filtered_df.copy()

# ----------------- TABS -----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Nhóm 1: Xu hướng Thời gian", 
    "🏷️ Nhóm 2: Sản phẩm & Danh mục", 
    "🤝 Nhóm 3: Khách hàng", 
    "🚚 Nhóm 4: Địa lý & Vận chuyển"
])

# ----- TAB 1: THỜI GIAN -----
with tab1:
    st.header("📈 Phân tích Xu hướng Thời gian")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Doanh thu theo tháng-năm")
        if not plot_df.empty:
            plot_df['year_month'] = plot_df['order_date'].dt.to_period('M').astype(str)
            rev_time = plot_df.groupby('year_month')['total_amount'].sum().reset_index()
            # String label for nice legend
            rev_time['Trạng Thái'] = ['Tháng Cao Điểm' if x else 'Tháng Thường' for x in rev_time['total_amount'] == rev_time['total_amount'].max()]
            
            fig_time = px.bar(rev_time, x='year_month', y='total_amount', 
                              color='Trạng Thái', color_discrete_map={'Tháng Cao Điểm': '#e74c3c', 'Tháng Thường': '#3498db'},
                              title="Doanh Thu Biến Động Qua Thời Gian",
                              labels={'year_month': 'Thời Gian (Tháng)', 'total_amount': 'Doanh Thu ($)'})
            st.plotly_chart(fig_time, use_container_width=True)
        else:
            st.warning("Không có dữ liệu trong khoảng đã chọn.")
        
    with col2:
        st.subheader("2. Số lượng đơn hàng theo thứ trong tuần")
        dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_counts = plot_df['order_day_of_week'].value_counts().reindex(dow_order, fill_value=0).reset_index()
        dow_counts.columns = ['Day', 'Orders']
        dow_counts['Trạng Thái'] = ['Ngày Cao Nhất' if x else 'Bình Thường' for x in dow_counts['Orders'] == dow_counts['Orders'].max()]
        
        fig_dow = px.bar(dow_counts, x='Day', y='Orders', 
                         color='Trạng Thái', color_discrete_map={'Ngày Cao Nhất': '#e74c3c', 'Bình Thường': '#3498db'},
                         title="Giao Dịch Theo Các Ngày Trong Tuần",
                         labels={'Day': 'Thứ', 'Orders': 'Số Đơn Hàng'})
        st.plotly_chart(fig_dow, use_container_width=True)

# ----- TAB 2: SẢN PHẨM & DANH MỤC -----
with tab2:
    st.header("🏷️ Phân tích Sản phẩm & Danh mục")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Doanh thu theo Danh mục")
        rev_cat = plot_df.groupby('category')['total_amount'].sum().reset_index().sort_values(by='total_amount', ascending=True)
        if not rev_cat.empty:
            rev_cat['Trạng Thái'] = ['Doanh thu top đầu' if x else 'Bình thường' for x in rev_cat['total_amount'] == rev_cat['total_amount'].max()]
            fig_cat = px.bar(rev_cat, x='total_amount', y='category', orientation='h', 
                             color='Trạng Thái', color_discrete_map={'Doanh thu top đầu': '#e74c3c', 'Bình thường': '#3498db'},
                             title="Tổng Doanh Thu Của Các Danh Mục",
                             labels={'total_amount': 'Doanh Thu ($)', 'category': 'Danh Mục'})
            st.plotly_chart(fig_cat, use_container_width=True)
        
    with col2:
        st.subheader("2. Tỷ lệ hoàn trả (Return Rate)")
        ret_cat = plot_df.groupby('category').agg(
            total_orders=('order_id', 'count'),
            returns=('is_returned', 'sum')
        ).reset_index()
        if not ret_cat.empty:
            ret_cat['return_rate'] = (ret_cat['returns'] / ret_cat['total_orders']) * 100
            ret_cat = ret_cat.sort_values(by='return_rate', ascending=True)
            
            ret_cat['Trạng Thái'] = ['Rủi ro hoàn trả cao nhất' if x else 'Bình thường' for x in ret_cat['return_rate'] == ret_cat['return_rate'].max()]
            fig_ret = px.bar(ret_cat, x='return_rate', y='category', orientation='h', 
                             color='Trạng Thái', color_discrete_map={'Rủi ro hoàn trả cao nhất': '#c0392b', 'Bình thường': '#95a5a6'},
                             title="Tỷ lệ hoàn trả (%) Theo Danh Mục",
                             labels={'return_rate': 'Tỷ Lệ Hoàn Trả (%)', 'category': 'Danh Mục'})
            st.plotly_chart(fig_ret, use_container_width=True)
        
    st.subheader("3. Mức Giảm Giá vs Biên Lợi Nhuận")
    disc_profit = plot_df.groupby('discount').agg(
        avg_profit=('profit_margin','mean'),
        orders=('order_id','count')
    ).reset_index()
    if not disc_profit.empty:
        disc_profit['discount_pct'] = disc_profit['discount'] * 100
        disc_profit['Nhóm'] = ['Hiệu quả cao nhất (0%)' if d == 0 else 'Có giảm giá' for d in disc_profit['discount_pct']]
        
        fig_scatter = px.scatter(disc_profit, x='discount_pct', y='avg_profit', size='orders', 
                                 color='Nhóm', color_discrete_map={'Hiệu quả cao nhất (0%)': '#27ae60', 'Có giảm giá': '#e67e22'},
                                 title="Tương Quan Bậc Giảm Giá và Biên lợi nhuận trung bình",
                                 labels={'discount_pct': 'Giảm Giá (%)', 'avg_profit': 'Biên Lợi Nhuận TB ($)', 'orders': 'Số đơn'})
        st.plotly_chart(fig_scatter, use_container_width=True)


# ----- TAB 3: KHÁCH HÀNG -----
with tab3:
    st.header("🤝 Phân tích Khách hàng")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Tổng Chi Tiêu Bằng Giới Tính")
        fig_gender = px.pie(plot_df, names='customer_gender', values='total_amount', 
                            title="Tỷ trọng doanh thu theo Giới tính", hole=0.4)
        st.plotly_chart(fig_gender, use_container_width=True)
        
    with col2:
        st.subheader("2. Phương thức thanh toán ưu chuộng")
        pm_counts = plot_df['payment_method'].value_counts().reset_index()
        pm_counts.columns = ['Method', 'Count']
        if not pm_counts.empty:
            pm_counts['Trạng Thái'] = ['Phổ biến nhất' if x else 'Bình thường' for x in pm_counts['Count'] == pm_counts['Count'].max()]
            fig_pm = px.bar(pm_counts, x='Method', y='Count', title="Sự phổ biến của Phương Thức Thanh Toán", 
                            color='Trạng Thái', color_discrete_map={'Phổ biến nhất': '#8e44ad', 'Bình thường': '#bdc3c7'})
            st.plotly_chart(fig_pm, use_container_width=True)
        
    st.subheader("3. Phân bổ độ tuổi mua sắm")
    fig_age = px.histogram(plot_df, x='customer_age', nbins=20, title="Phân bổ Độ tuổi Khách hàng",
                           labels={'customer_age': 'Tuổi'})
    st.plotly_chart(fig_age, use_container_width=True)


# ----- TAB 4: ĐỊA LÝ & VẬN CHUYỂN -----
with tab4:
    st.header("🚚 Phân bổ Khu vực & Vận chuyển")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Doanh thu phân bổ theo Khu vực")
        rev_reg = plot_df.groupby('region')['total_amount'].sum().reset_index()
        fig_reg = px.pie(rev_reg, names='region', values='total_amount', title="Tỷ trọng Doanh thu theo Khu Vực")
        st.plotly_chart(fig_reg, use_container_width=True)
        
    with col2:
        st.subheader("2. Chi phí & Thời gian giao hàng")
        ship_reg = plot_df.groupby('region').agg(
            avg_shipping=('shipping_cost', 'mean'),
            avg_delivery=('delivery_time_days', 'mean')
        ).reset_index()
        if not ship_reg.empty:
            ship_reg['Trạng Thái'] = ['Vùng Giao Chậm Nhất' if x else 'Bình thường' for x in ship_reg['avg_delivery'] == ship_reg['avg_delivery'].max()]
            fig_ship = px.bar(ship_reg, x='region', y='avg_shipping', 
                              color='Trạng Thái', color_discrete_map={'Vùng Giao Chậm Nhất': '#e74c3c', 'Bình thường': '#3498db'},
                              title="Phí Vận Chuyển TB và Trạng thái Giao Hàng",
                              labels={'region': 'Khu Vực', 'avg_shipping': 'Phí Vận Chuyển ($)'})
            st.plotly_chart(fig_ship, use_container_width=True)

st.markdown("---")
st.markdown("*Nền tảng được phát triển cho môn Trực quan hóa dữ liệu. Dashboard by Lê Lâm Trí Đức, Code Data by Phạm Quang Vinh.*")
