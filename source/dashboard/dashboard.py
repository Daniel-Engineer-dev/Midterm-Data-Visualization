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
    st.header("🤝Phân tích Khách hàng")
    st.markdown("Tiêu điểm: Hành vi chi tiêu của khách hàng theo độ tuổi, giới tính, tỷ lệ sử dụng phương thức thanh toán và vinh danh Top 10 khách hàng VIP.")
    
    # Chuẩn bị dữ liệu như trong script báo cáo Nhóm 3
    # Chỉ tính các đơn giao dịch thành công để tính chi tiêu thực
    if not plot_df.empty:
        df_valid = plot_df[plot_df['is_returned'] == 0].copy()
        bins = [18, 25, 35, 45, 55, 70]
        labels = ['18-24', '25-34', '35-44', '45-54', '55-69']
        df_valid['age_group'] = pd.cut(df_valid['customer_age'], bins=bins, labels=labels, right=False)
        
        st.subheader("1. Tổng Chi Tiêu Thực Tế theo Nhóm Tuổi & Giới Tính")
        if not df_valid.empty:
            t2 = df_valid.groupby(['age_group', 'customer_gender'], observed=True)['total_amount'].sum().reset_index()
            t2['total_amount_k'] = t2['total_amount'] / 1000
            
            # [Visual Encoding]: Position (Y) cho Quantitative, Color (Hue) cho Categorical
            # [Color Theory]: Dùng Categorical/Qualitative Palette phân tách rõ ràng giới tính (Colorblind-friendly considerations)
            # [Interaction]: Custom tooltip cho Details-on-Demand
            fig_spend_age = px.bar(t2, x='age_group', y='total_amount_k', color='customer_gender', barmode='group',
                                   title="Tổng chi tiêu (Nghìn USD) theo Nhóm Tuổi và Giới Tính",
                                   color_discrete_map={'Female': '#D63384', 'Male': '#0D6EFD', 'Other': '#198754'},
                                   labels={'age_group': 'Nhóm tuổi', 'total_amount_k': 'Tổng chi tiêu (K$)', 'customer_gender': 'Giới tính'},
                                   text_auto='.0f',
                                   hover_data={'total_amount_k': ':.1f'}) # Details-on-demand
            
            # Ép chữ luôn nằm ngang (không bị dọc) và nới rộng trục y để hiện lưới 800k$
            fig_spend_age.update_traces(textposition='outside', textangle=0)
            
            # [Perception]: Dọn dẹp gridlines để tuân thủ Data-Ink Ratio, tập trung vào Data
            fig_spend_age.update_layout(
                yaxis_showgrid=True, 
                xaxis_showgrid=False, 
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(range=[0, t2['total_amount_k'].max() * 1.15]) # Nới rộng trục Y thêm 15%
            )
            st.plotly_chart(fig_spend_age, use_container_width=True)
            
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("2. Tỉ lệ Phương thức Thanh toán theo Tuổi")
            if not df_valid.empty:
                t6 = df_valid.groupby(['age_group', 'payment_method'], observed=True).size().unstack(fill_value=0)
                t6_pct = t6.div(t6.sum(axis=1), axis=0) * 100
                t6_pct = t6_pct.round(1)
                
                # [Visual Encoding & Color Theory]: Dùng Sequential Colormap (Blues) ánh xạ Value sang Color Luminance
                fig_heat = px.imshow(t6_pct, text_auto=True, color_continuous_scale='Blues',
                                     title="Heatmap Tỉ lệ Phương thức Thanh toán (%)",
                                     labels=dict(x="Phương thức", y="Nhóm tuổi", color="Tỉ lệ %"))
                fig_heat.update_yaxes(autorange="reversed")
                st.plotly_chart(fig_heat, use_container_width=True)
                
        with col2:
            st.subheader("3. Top 10 Khách Hàng VIP (Customer ID)")
            if not df_valid.empty:
                top_c = df_valid.groupby('customer_id', observed=True)['total_amount'].sum().sort_values(ascending=False).head(10).reset_index()
                top_c = top_c.sort_values('total_amount', ascending=True)
                
                # [Perception - Pre-attentive processing]: Tự động gán Pop-out Color để đập vào mắt điểm cao nhất (Red vs Blue)
                top_c['Trạng Thái'] = ['Top 1 VIP' if x == top_c['total_amount'].max() else 'VIP Khác' for x in top_c['total_amount']]
                
                fig_top10 = px.bar(top_c, x='total_amount', y='customer_id', orientation='h',
                                   title="Top 10 Khách hàng có Tổng Chi tiêu Cao nhất",
                                   color='Trạng Thái',
                                   color_discrete_map={'Top 1 VIP': '#e74c3c', 'VIP Khác': '#3498db'},
                                   labels={'total_amount': 'Tổng tiền ($)', 'customer_id': 'Mã KH', 'Trạng Thái': 'Phân Loại'},
                                   text_auto='.0f')
                
                fig_top10.update_layout(yaxis_showgrid=False, xaxis_showgrid=True, plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_top10, use_container_width=True)
    else:
        st.warning("Không có dữ liệu trong khoảng đã chọn.")


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
