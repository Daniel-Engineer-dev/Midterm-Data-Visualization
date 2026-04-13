import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np

# ══════════════════════════════════════════════════════════════
# PAGE CONFIG — MUST BE FIRST STREAMLIT COMMAND
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════
# DESIGN SYSTEM — Colors, Fonts, Global CSS
# Follows: UI/UX Pro Max + Design Spells + KPI Dashboard Design
# ══════════════════════════════════════════════════════════════

# Color Palette — Cohesive, accessible, professional
COLORS = {
    'primary':     '#0F172A',  # Slate 900 — deep anchoring
    'secondary':   '#1E293B',  # Slate 800
    'accent':      '#3B82F6',  # Blue 500 — primary action
    'accent_light':'#60A5FA',  # Blue 400
    'success':     '#10B981',  # Emerald 500
    'warning':     '#F59E0B',  # Amber 500
    'danger':      '#EF4444',  # Red 500
    'purple':      '#8B5CF6',  # Violet 500
    'pink':        '#EC4899',  # Pink 500
    'cyan':        '#06B6D4',  # Cyan 500
    'surface':     '#F8FAFC',  # Slate 50
    'text':        '#0F172A',  # Slate 900
    'muted':       '#64748B',  # Slate 500
    'border':      '#E2E8F0',  # Slate 200
}

# Plotly chart template — consistent across all tabs
CHART_FONT = dict(family="'Fira Sans', 'Inter', -apple-system, sans-serif", size=12, color=COLORS['text'])
CHART_LAYOUT = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=CHART_FONT,
    margin=dict(t=80, b=40, l=40, r=20),
    hoverlabel=dict(bgcolor='white', font_size=12, font_family="Inter"),
)

# Plotly color sequences per group
SEQ_BLUE   = ['#3B82F6', '#60A5FA', '#93C5FD', '#BFDBFE']
SEQ_MULTI  = ['#3B82F6', '#8B5CF6', '#EC4899', '#F59E0B', '#10B981', '#06B6D4']
SEQ_GENDER = {'Female': '#EC4899', 'Male': '#3B82F6', 'Other': '#10B981'}

# ══════════════════════════════════════════════════════════════
# MASTER CSS — Design Spells: Glassmorphism, Gradients, Animations
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Google Fonts: Dashboard Data pairing (UI Pro Max) ── */
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Fira+Sans:wght@300;400;500;600;700;800&display=swap');

/* ── Global Reset & Typography ── */
html, body, [class*="css"] {
    font-family: 'Fira Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* ── Streamlit overrides ── */
.stApp {
    background: linear-gradient(170deg, #F8FAFC 0%, #EFF6FF 40%, #F0F4FF 70%, #F8FAFC 100%);
    background-attachment: fixed;
}
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}
[data-testid="stSidebarUserContent"] {
    padding-top: 2rem !important;
}
header[data-testid="stHeader"] { background: transparent; }

/* ── Sidebar: Light theme with blue accent ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #F0F4FF 40%, #EBF0FF 100%) !important;
    border-right: 1px solid rgba(59,130,246,0.12) !important;
    box-shadow: 4px 0 24px rgba(59,130,246,0.06);
}
[data-testid="stSidebar"]::after {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(59,130,246,0.05) 0%, transparent 60%);
    pointer-events: none;
}
[data-testid="stSidebar"] * { color: #1E293B !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {
    color: #475569 !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    font-family: 'Fira Sans', sans-serif !important;
}
[data-testid="stSidebar"] hr { border-color: rgba(30,64,175,0.1) !important; }

/* ── Dashboard Title Area: Light blue gradient with shimmer ── */
.dashboard-header {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 50%, #E0E7FF 100%);
    border-radius: 18px;
    padding: 22px 36px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(59,130,246,0.1), 0 2px 8px rgba(139,92,246,0.06);
    border: 1px solid rgba(59,130,246,0.15);
}
.dashboard-header::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 15% 50%, rgba(59,130,246,0.12) 0%, transparent 55%),
                radial-gradient(ellipse at 85% 20%, rgba(139,92,246,0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 100%, rgba(6,182,212,0.04) 0%, transparent 40%);
    animation: headerPulse 6s ease-in-out infinite alternate;
}
@keyframes headerPulse {
    0%   { opacity: 0.7; }
    100% { opacity: 1; }
}
.dashboard-header h1 {
    color: #0F172A !important; font-size: 1.85em !important; font-weight: 800 !important;
    letter-spacing: -0.025em; position: relative; z-index: 1; margin: 0 !important;
    font-family: 'Fira Sans', sans-serif !important;
    text-shadow: none;
}
.dashboard-header p {
    color: #475569 !important; font-size: 0.92em; position: relative; z-index: 1;
    margin: 6px 0 0 0 !important; font-family: 'Fira Sans', sans-serif !important;
    letter-spacing: 0.01em;
}

/* ── KPI Metric Cards — Glassmorphism + Micro-animation ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 28px;
}
@media (max-width: 768px)  { .kpi-grid { grid-template-columns: repeat(2, 1fr); } }

.kpi-card {
    background: rgba(255,255,255,0.88);
    backdrop-filter: blur(16px) saturate(180%);
    -webkit-backdrop-filter: blur(16px) saturate(180%);
    border: 1px solid rgba(226,232,240,0.7);
    border-radius: 16px;
    padding: 22px 20px 18px;
    text-align: left;
    transition: all 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    border-radius: 16px 16px 0 0;
}
.kpi-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 22px 42px rgba(0,0,0,0.08), 0 8px 16px rgba(59,130,246,0.12);
    border-color: rgba(59,130,246,0.25);
}
.kpi-card { transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
/* Per-card gradient top bar */
.kpi-card.blue::before   { background: linear-gradient(90deg, #1E40AF, #3B82F6, #60A5FA); }
.kpi-card.green::before  { background: linear-gradient(90deg, #047857, #10B981, #34D399); }
.kpi-card.amber::before  { background: linear-gradient(90deg, #B45309, #F59E0B, #FBBF24); }
.kpi-card.red::before    { background: linear-gradient(90deg, #B91C1C, #EF4444, #F87171); }
.kpi-card.purple::before { background: linear-gradient(90deg, #6D28D9, #8B5CF6, #A78BFA); }
.kpi-card.slate::before  { background: linear-gradient(90deg, #334155, #475569, #64748B); }

.kpi-header-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
}
.kpi-icon {
    width: 32px; height: 32px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1em;
    transition: transform 0.3s ease;
}
.kpi-card:hover .kpi-icon { transform: scale(1.1); }
.kpi-icon.blue   { background: #EFF6FF; color: #1E40AF; }
.kpi-icon.green  { background: #ECFDF5; color: #047857; }
.kpi-icon.amber  { background: #FFFBEB; color: #B45309; }
.kpi-icon.red    { background: #FEF2F2; color: #B91C1C; }
.kpi-icon.purple { background: #F5F3FF; color: #6D28D9; }
.kpi-icon.slate  { background: #F1F5F9; color: #334155; }

.kpi-label {
    font-size: 0.75em; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.06em; color: #64748B; margin-bottom: 0px;
    font-family: 'Fira Sans', sans-serif;
}
.kpi-value {
    font-size: 1.7em; font-weight: 700; color: #0F172A;
    letter-spacing: -0.03em; line-height: 1.1;
    font-family: 'Fira Code', monospace;
}
.kpi-delta {
    font-size: 0.73em; font-weight: 600; margin-top: 8px;
    display: inline-flex; align-items: center; gap: 3px;
    padding: 3px 10px; border-radius: 20px;
    font-family: 'Fira Sans', sans-serif;
}
.kpi-delta.up   { background: #ECFDF5; color: #047857; }
.kpi-delta.down { background: #FEF2F2; color: #B91C1C; }

/* ── Section Headers ── */
.section-header {
    display: flex; align-items: center; gap: 12px;
    margin: 32px 0 16px 0; padding-bottom: 12px;
    border-bottom: 2px solid rgba(226,232,240,0.6);
}
.section-header .badge {
    background: linear-gradient(135deg, #1E40AF, #7C3AED);
    color: white; font-size: 0.68em; font-weight: 700;
    padding: 5px 12px; border-radius: 20px;
    text-transform: uppercase; letter-spacing: 0.07em;
    font-family: 'Fira Sans', sans-serif;
    box-shadow: 0 2px 8px rgba(30,64,175,0.2);
}
.section-header h3 {
    font-size: 1.08em !important; font-weight: 700 !important;
    color: #0F172A !important; margin: 0 !important;
    font-family: 'Fira Sans', sans-serif !important;
}

/* ── Insight Cards — Glassmorphism + border glow ── */
.insight-card {
    background: linear-gradient(135deg, rgba(240,249,255,0.95), rgba(239,246,255,0.9));
    backdrop-filter: blur(8px);
    border: 1px solid rgba(191,219,254,0.6);
    border-left: 4px solid #1E40AF;
    border-radius: 12px;
    padding: 16px 20px;
    margin: 12px 0 18px 0;
    font-size: 0.87em;
    color: #1E293B;
    line-height: 1.6;
    transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    font-family: 'Fira Sans', sans-serif;
}
.insight-card:hover {
    border-left-color: #7C3AED;
    background: linear-gradient(135deg, rgba(245,243,255,0.95), rgba(239,246,255,0.9));
    box-shadow: 0 4px 16px rgba(59,130,246,0.1);
    transform: translateX(2px);
}
.insight-card strong { color: #1E40AF; font-weight: 700; }
.insight-card.warning {
    background: linear-gradient(135deg, rgba(255,251,235,0.95), rgba(254,243,199,0.9));
    border-color: rgba(253,230,138,0.6);
    border-left-color: #D97706;
}
.insight-card.warning strong { color: #92400E; }
.insight-card.danger {
    background: linear-gradient(135deg, rgba(254,242,242,0.95), rgba(254,226,226,0.9));
    border-color: rgba(254,202,202,0.6);
    border-left-color: #DC2626;
}
.insight-card.danger strong { color: #991B1B; }

/* ── Chart Container ── */
.chart-container {
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(12px) saturate(150%);
    -webkit-backdrop-filter: blur(12px) saturate(150%);
    border: 1px solid rgba(226,232,240,0.5);
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 18px;
    transition: all 0.3s ease;
}
.chart-container:hover {
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
    border-color: rgba(59,130,246,0.12);
}

/* ── Footer ── */
.dashboard-footer {
    text-align: center; padding: 32px 20px 24px;
    margin-top: 48px;
    border-top: 1px solid rgba(226,232,240,0.5);
    color: #94A3B8; font-size: 0.78em;
    font-family: 'Fira Sans', sans-serif;
    letter-spacing: 0.01em;
}
.dashboard-footer strong { color: #64748B; font-weight: 700; }
.dashboard-footer a { color: #3B82F6; text-decoration: none; }

/* ── Tab Styling — Pill-style with smooth transitions ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(12px);
    border-radius: 14px;
    padding: 5px 6px;
    border: 1px solid rgba(226,232,240,0.6);
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.84em;
    padding: 10px 18px;
    font-family: 'Fira Sans', sans-serif !important;
    transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(59,130,246,0.06);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1E40AF, #3B82F6) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(30,64,175,0.25);
}

/* ── Streamlit metric overrides ── */
[data-testid="stMetricValue"] {
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    font-family: 'Fira Code', monospace !important;
}

/* ── Plotly chart containers ── */
[data-testid="stPlotlyChart"] {
    border-radius: 12px;
    overflow: hidden;
}

/* ── Scrollbar styling ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(148,163,184,0.3);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(148,163,184,0.5); }
/* ── Custom Sidebar Navigation Menu using active Tabs logic ── */
[data-testid="stSidebar"] div[role="radiogroup"] > label input[type="radio"] { display: none !important; }
[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-of-type { display: none !important; }

/* Force exact width of the sidebar ONLY when expanded */
section[data-testid="stSidebar"][aria-expanded="true"] {
    width: 260px !important;
    min-width: 260px !important;
    max-width: 260px !important;
}

/* Force radiogroup to fill width */
/* Ensure ST Radio fills the Sidebar */
[data-testid="stSidebar"] .stRadio {
    width: 100% !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] {
    width: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: stretch !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] > label {
    padding: 10px 14px;
    margin-bottom: 4px;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.95em;
    color: #475569;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    border-bottom: 2px solid transparent;
    width: 100% !important;
    display: block !important;
    box-sizing: border-box;
}

[data-testid="stSidebarUserContent"], [data-testid="stSidebar"] > div:first-child {
    padding-top: 0.5rem !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    background-color: rgba(59, 130, 246, 0.05);
}

[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
    background-color: #EFF6FF !important; /* Xanh nhạt */
    border-bottom: 2px solid #3B82F6 !important; /* Viền gạch chân xanh */
    color: #1E40AF !important; 
}

</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    data_path = os.path.join(project_dir, 'data', 'ecommerce_sales_cleaned.csv')
    if not os.path.exists(data_path):
        st.error(f"Không tìm thấy file dữ liệu tại: {data_path}")
        st.stop()
    df = pd.read_csv(data_path)
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

# ══════════════════════════════════════════════════════════════
# SIDEBAR — Professional Filter Panel
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="font-size: 1.12em; font-weight: 800; color: #0F172A !important; margin-top: -42px; margin-bottom: 15px; margin-right: 25px; line-height: 1.3;">
        E-Commerce Sales Analytics
    </div>
    """, unsafe_allow_html=True)
    PAGE_ICONS = {
        "Tổng Quan": "🔎  Tổng Quan",
        "Xu Hướng Thời Gian": "⏳  Xu Hướng Thời Gian",
        "Sản Phẩm & Danh Mục": "🛒  Sản Phẩm & Danh Mục",
        "Khách Hàng": "👥  Khách Hàng",
        "Địa Lý & Logistics": "✈️  Địa Lý & Logistics",
    }
    page = st.radio(
        "Menu",
        list(PAGE_ICONS.keys()),
        format_func=lambda x: PAGE_ICONS[x],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Date Range Filter
    st.markdown('<p style="font-size:0.72em; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#475569 !important; margin-bottom:4px;">Khoảng thời gian</p>', unsafe_allow_html=True)
    min_date = df['order_date'].min().date()
    max_date = df['order_date'].max().date()
    date_range = st.date_input(
        "Chọn ngày bắt đầu & kết thúc",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Dataset Info
    st.markdown(f"""
    <div style="background: rgba(30,64,175,0.06); border-radius: 10px; padding: 14px; margin-top:8px; border: 1px solid rgba(59,130,246,0.1);">
        <div style="font-size: 0.7em; font-weight: 700; text-transform: uppercase;
                    letter-spacing: 0.08em; color: #475569 !important; margin-bottom: 8px;">
            Thống kê Dataset
        </div>
        <div style="font-size: 0.82em; line-height: 2;">
            <span style="color: #64748B !important;">Tổng bản ghi:</span>
            <span style="color: #0F172A !important; font-weight: 700;">{len(df):,}</span><br>
            <span style="color: #64748B !important;">Khoảng thời gian:</span>
            <span style="color: #0F172A !important; font-weight: 700;">2023–2025</span><br>
            <span style="color: #64748B !important;">Khu vực:</span>
            <span style="color: #0F172A !important; font-weight: 700;">{df['region'].nunique()}</span><br>
            <span style="color: #64748B !important;">Danh mục:</span>
            <span style="color: #0F172A !important; font-weight: 700;">{df['category'].nunique()}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# APPLY FILTERS
# ══════════════════════════════════════════════════════════════
# Handle date_range
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_d, end_d = date_range
else:
    start_d, end_d = min_date, max_date

base_df = df[
    (df['order_date'].dt.date >= start_d) &
    (df['order_date'].dt.date <= end_d)
]

col_main, col_filter = st.columns([3.8, 1], gap="large")

with col_filter:
    st.markdown('<div id="sticky-filter-marker"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header" style="margin-bottom:12px;"><h3 style="font-size:1.1em;">Bộ lọc Nâng cao</h3></div>', unsafe_allow_html=True)
    
    all_regions = sorted(df['region'].unique().tolist())
    all_categories = sorted(df['category'].unique().tolist())
    all_genders = sorted(df['customer_gender'].unique().tolist())
    
    selected_regions = all_regions[:]
    selected_categories = all_categories[:]
    selected_genders = all_genders[:]

    if page in ["Tổng Quan", "Xu Hướng Thời Gian", "Địa Lý & Logistics", "Khách Hàng"]:
        with st.expander("Khu vực", expanded=False):
            selected_regions = [r for r in all_regions if st.checkbox(r, value=True, key=f"reg_{r}")]
        
    if page in ["Tổng Quan", "Sản Phẩm & Danh Mục", "Xu Hướng Thời Gian", "Địa Lý & Logistics"]:
        with st.expander("Danh mục", expanded=False):
            selected_categories = [c for c in all_categories if st.checkbox(c, value=True, key=f"cat_{c}")]

    if page in ["Tổng Quan", "Khách Hàng", "Sản Phẩm & Danh Mục"]:
        with st.expander("Giới tính", expanded=False):
            selected_genders = [g for g in all_genders if st.checkbox(g, value=True, key=f"gen_{g}")]

filtered_df = base_df[
    (base_df['region'].isin(selected_regions)) &
    (base_df['category'].isin(selected_categories)) &
    (base_df['customer_gender'].isin(selected_genders))
]
plot_df = filtered_df.copy()

# Global age binning
bins_age = [18, 25, 35, 45, 55, 70]
labels_age = ['18-24', '25-34', '35-44', '45-54', '55-69']
plot_df['age_group'] = pd.cut(plot_df['customer_age'], bins=bins_age, labels=labels_age, right=False)

def style_fig(fig, height=380, show_xgrid=False, show_ygrid=True):
    """Apply consistent styling to any Plotly figure."""
    fig.update_layout(
        **CHART_LAYOUT,
        height=height,
        xaxis=dict(showgrid=show_xgrid, gridcolor='#F1F5F9', zeroline=False),
        yaxis=dict(showgrid=show_ygrid, gridcolor='#F1F5F9', zeroline=False),
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5,
            font=dict(size=11), bgcolor='rgba(255,255,255,0.6)',
        ),
    )
    return fig

# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════
with col_main:
    st.markdown(f"""
    <div class="dashboard-header">
        <h1>{page}</h1>
        <p>E-Commerce Sales Analytics  ·  <strong style="color:#1E40AF;">{len(plot_df):,}</strong> bản ghi phù hợp điều kiện lọc</p>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# HELPER: Plotly chart styling
# ══════════════════════════════════════════════════════════════



# ┌─────────────────────────────────────────────────────────────┐
# │  TAB: TỔNG QUAN — Executive Overview                       │
# └─────────────────────────────────────────────────────────────┘
    if page == "Tổng Quan":
        if plot_df.empty:
            st.warning("Không có dữ liệu — vui lòng điều chỉnh bộ lọc trên thanh bên trái.")
        else:
            # ─── KPI Calculations ───
            df_success = plot_df[plot_df['is_returned'] == 0]
            total_rev      = df_success['total_amount'].sum()
            total_orders   = len(plot_df)
            completed_orders = len(df_success)
            avg_order_val  = total_rev / completed_orders if completed_orders > 0 else 0
            total_returned = int(plot_df['is_returned'].sum())
            return_rate    = (total_returned / total_orders * 100) if total_orders > 0 else 0
            avg_ship       = plot_df['shipping_cost'].mean()
            total_profit   = df_success['profit_margin'].sum()

            # ─── KPI Cards Grid — 6 cards ───
            st.markdown(f"""
            <div class="kpi-grid">
                <div class="kpi-card blue">
                    <div class="kpi-header-row">
                        <div class="kpi-label">Tổng Doanh Thu (Revenue)</div>
                    </div>
                    <div class="kpi-value">${total_rev/1e6:.2f}M</div>
                    <div class="kpi-delta up">Tổng doanh thu từ đơn hàng thành công</div>
                </div>
                <div class="kpi-card green">
                    <div class="kpi-header-row">
                        <div class="kpi-label">Tổng Số Đơn Hàng (Orders)</div>
                    </div>
                    <div class="kpi-value">{total_orders:,}</div>
                    <div class="kpi-delta up">{completed_orders:,} đơn giao thành công</div>
                </div>
                <div class="kpi-card amber">
                    <div class="kpi-header-row">
                        <div class="kpi-label">Giá Trị Trung Bình Đơn Hàng (AOV)</div>
                    </div>
                    <div class="kpi-value">${avg_order_val:,.0f}</div>
                    <div class="kpi-delta up">Trung bình mỗi đơn hàng</div>
                </div>
                <div class="kpi-card red">
                    <div class="kpi-header-row">
                        <div class="kpi-label">Tỷ Lệ Hoàn Trả / Hủy Đơn</div>
                    </div>
                    <div class="kpi-value">{return_rate:.1f}%</div>
                    <div class="kpi-delta down">{total_returned:,} đơn bị hoàn trả</div>
                </div>
                <div class="kpi-card purple">
                    <div class="kpi-header-row">
                        <div class="kpi-label">Cước Phí Vận Chuyển Trung Bình</div>
                    </div>
                    <div class="kpi-value">${avg_ship:.2f}</div>
                    <div class="kpi-delta up">Chi phí ship trung bình mỗi đơn</div>
                </div>
                <div class="kpi-card slate">
                    <div class="kpi-header-row">
                        <div class="kpi-label">Tổng Lợi Nhuận Ròng (Profit)</div>
                    </div>
                    <div class="kpi-value">${total_profit/1e6:.2f}M</div>
                    <div class="kpi-delta up">Biên lợi nhuận tích lũy</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ─── KPI ALERTS (Pattern from kpi-dashboard-design) ───
            overall_return_rate = plot_df['is_returned'].mean() * 100
            if overall_return_rate > 5:
                st.error(f"🔴 **Cảnh báo (Chỉ số KPI):** Tỷ lệ hoàn trả toàn hệ thống đang ở mức {overall_return_rate:.1f}% (Vượt ngưỡng an toàn 5%).")
            
            if avg_ship > 6:
                st.warning(f"🟡 **Lưu ý (Logistics):** Chi phí vận chuyển trung bình (${avg_ship:.2f}) khá cao. Cần xem lại các tuyến giao hàng xa.")

            # ─── ROW 1: Revenue Trend + Category Breakdown ───
            st.markdown('<div class="section-header"><span class="badge">Nhóm 1 & 2</span><h3>Xu hướng Doanh thu · Hiệu suất Danh mục</h3></div>', unsafe_allow_html=True)

            ov_c1, ov_c2 = st.container(), st.container()

            with ov_c1:
                plot_df['order_date'] = pd.to_datetime(plot_df['order_date'])
                rev_time = plot_df.groupby(plot_df['order_date'].dt.to_period('M'))['total_amount'].sum().reset_index()
                rev_time['month_ts'] = rev_time['order_date'].dt.to_timestamp()

                fig_ov1 = go.Figure()
                fig_ov1.add_trace(go.Scatter(
                    x=rev_time['month_ts'], y=rev_time['total_amount'],
                    mode='lines+markers',
                    line=dict(color='#3B82F6', width=2.5, shape='spline'),
                    marker=dict(size=6, color='#2563EB', line=dict(width=2, color='white')),
                    fill='tozeroy', fillcolor='rgba(59,130,246,0.08)',
                    name='Doanh thu',
                    hovertemplate='<b>%{x|%b %Y}</b><br>$%{y:,.0f}<extra></extra>'
                ))
                fig_ov1.update_layout(title=dict(text='Xu hướng Doanh thu Hàng tháng', font=dict(size=14, color='#1E293B')))
                fig_ov1.update_xaxes(rangeslider_visible=True, rangeselector=dict(
                    buttons=list([
                        dict(count=3, label="3m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(step="all")
                    ])
                ))
                style_fig(fig_ov1, height=380)
                st.plotly_chart(fig_ov1, use_container_width=True)

                st.markdown('<div class="insight-card"><strong>Nhóm 1:</strong> Doanh thu tăng mạnh Quý 4 (tháng 10, 12) — phù hợp mùa lễ hội. Giữa tuần (Thứ 3–5) là cao điểm giao dịch.</div>', unsafe_allow_html=True)

            with ov_c2:
                rev_cat = plot_df.groupby('category')['total_amount'].sum().reset_index()
                ret_cat = plot_df.groupby('category').agg(total=('order_id','count'), ret=('is_returned','sum')).reset_index()
                ret_cat['return_rate'] = ret_cat['ret'] / ret_cat['total'] * 100
                merged = rev_cat.merge(ret_cat[['category','return_rate']], on='category').sort_values('total_amount', ascending=False)

                fig_ov2 = go.Figure()
                fig_ov2.add_trace(go.Bar(
                    x=merged['category'], y=merged['total_amount']/1e6,
                    name='Doanh thu (M$)', marker_color='#8B5CF6', marker_cornerradius=6,
                    text=[f"${v:.2f}M" for v in merged['total_amount']/1e6],
                    textposition='outside', textfont=dict(size=10, color='#475569'),
                    hovertemplate='<b>%{x}</b><br>Doanh thu: $%{y:.2f}M<extra></extra>'
                ))
                fig_ov2.add_trace(go.Scatter(
                    x=merged['category'], y=merged['return_rate'],
                    name='Tỷ lệ Hoàn (%)', mode='lines+markers',
                    marker=dict(color='#EF4444', size=9, symbol='diamond'),
                    line=dict(color='#EF4444', width=2, dash='dot'),
                    yaxis='y2',
                    hovertemplate='<b>%{x}</b><br>Hoàn: %{y:.1f}%<extra></extra>'
                ))
                fig_ov2.update_layout(
                    title=dict(text='Doanh thu & Tỷ lệ Hoàn trả theo Danh mục', font=dict(size=14, color='#1E293B')),
                    yaxis=dict(title='Doanh thu (M$)', showgrid=False),
                    yaxis2=dict(title='Tỷ lệ Hoàn (%)', overlaying='y', side='right', showgrid=False),
                )
                style_fig(fig_ov2, height=340)
                st.plotly_chart(fig_ov2, use_container_width=True)

                st.markdown('<div class="insight-card warning"><strong>Nhóm 2:</strong> Electronics dẫn đầu doanh thu ($3.3M). Fashion có tỷ lệ hoàn hàng cao nhất (8.3%) — cần kiểm soát sizing.</div>', unsafe_allow_html=True)

            # ─── ROW 2: Customer + Logistics ───
            st.markdown('<div class="section-header"><span class="badge">Nhóm 3 & 4</span><h3>Phân tầng Khách hàng · Hiệu suất Logistics</h3></div>', unsafe_allow_html=True)

            ov_c3, ov_c4 = st.container(), st.container()

            with ov_c3:
                df_valid_ov = plot_df[plot_df['is_returned']==0].copy()
                t_ov = df_valid_ov.groupby(['age_group', 'customer_gender'], observed=True)['total_amount'].sum().reset_index()
                t_ov['total_k'] = t_ov['total_amount'] / 1000

                fig_ov3 = px.bar(t_ov, x='age_group', y='total_k', color='customer_gender', barmode='group',
                                 color_discrete_map=SEQ_GENDER,
                                 labels={'age_group': 'Nhóm tuổi', 'total_k': 'Chi tiêu (K$)', 'customer_gender': 'Giới tính'},
                                 text_auto='.0f')
                fig_ov3.update_traces(textposition='outside', textangle=0, marker_cornerradius=4)
                fig_ov3.update_layout(title=dict(text='Chi tiêu theo Độ tuổi & Giới tính (K$)', font=dict(size=14, color='#1E293B')))
                style_fig(fig_ov3, height=340)
                st.plotly_chart(fig_ov3, use_container_width=True)

                st.markdown('<div class="insight-card"><strong>Nhóm 3:</strong> Nhóm 55-69 tuổi chi tiêu cao nhất. Nữ giới vượt nam giới ở nhóm 45+.</div>', unsafe_allow_html=True)

            with ov_c4:
                ship_ov = plot_df.groupby('region').agg(
                    avg_delivery=('delivery_time_days', 'mean'),
                    avg_shipping=('shipping_cost', 'mean'),
                    orders=('order_id', 'count')
                ).reset_index()

                fig_ov4 = px.scatter(ship_ov, x='avg_shipping', y='avg_delivery',
                                    size='orders', color='region', text='region',
                                    size_max=55,
                                    color_discrete_sequence=SEQ_MULTI,
                                    labels={'avg_shipping': 'Cước Phí TB ($)', 'avg_delivery': 'Thời Gian Giao (Ngày)', 'region': 'Vùng'})
                fig_ov4.update_traces(textposition='top center', textfont=dict(size=11, color='#1E293B'))
                fig_ov4.add_hrect(y0=5.5, y1=ship_ov['avg_delivery'].max()*1.08,
                                  fillcolor='rgba(239,68,68,0.06)', line_width=0,
                                  annotation_text='⚠ Vùng nguy hiểm', annotation_position='top left',
                                  annotation_font=dict(size=10, color='#EF4444'))
                fig_ov4.update_layout(
                    title=dict(text='Cước phí vs Tốc độ Giao hàng (Size = Đơn)', font=dict(size=14, color='#1E293B')),
                    showlegend=False,
                )
                style_fig(fig_ov4, height=340, show_xgrid=True)
                st.plotly_chart(fig_ov4, use_container_width=True)

                st.markdown('<div class="insight-card danger"><strong>Nhóm 4:</strong> Khu vực Đông — cước cao nhất + giao chậm nhất. Pearson +0.97 giữa phí ship và tỷ lệ bùng hàng.</div>', unsafe_allow_html=True)


    # ┌─────────────────────────────────────────────────────────────┐
    # │  TAB 1: XU HƯỚNG THỜI GIAN                                 │
    # └─────────────────────────────────────────────────────────────┘
    elif page == "Xu Hướng Thời Gian":
        st.markdown('<div class="section-header"><span class="badge">Nhóm 1</span><h3>Phân tích Xu hướng Doanh thu theo Thời gian</h3></div>', unsafe_allow_html=True)
        st.markdown("Theo dõi biến động doanh thu theo tháng/quý, xác định mùa vụ cao điểm và thói quen mua sắm theo ngày trong tuần.")

        if not plot_df.empty:
            plot_df['order_date'] = pd.to_datetime(plot_df['order_date'])

            # ── 1. Monthly Trend ──
            st.markdown("#### Biến động Doanh thu Hàng tháng")
            rev_time = plot_df.groupby(plot_df['order_date'].dt.to_period('M'))['total_amount'].sum().reset_index()
            rev_time['month_ts'] = rev_time['order_date'].dt.to_timestamp()

            # Interactive metric selector
            metric_choice = st.radio("Chọn chế độ xem:", ["Doanh thu tuyệt đối", "Tỷ lệ tăng trưởng (%)"],
                                     horizontal=True, key='t1_metric')

            if metric_choice == "Doanh thu tuyệt đối":
                fig_t1 = go.Figure()
                fig_t1.add_trace(go.Scatter(
                    x=rev_time['month_ts'], y=rev_time['total_amount'],
                    mode='lines+markers', name='Doanh thu',
                    line=dict(color='#3B82F6', width=2.5, shape='spline'),
                    marker=dict(size=7, color='#2563EB', line=dict(width=2, color='white')),
                    fill='tozeroy', fillcolor='rgba(59,130,246,0.06)',
                    hovertemplate='<b>%{x|%b %Y}</b><br>$%{y:,.0f}<extra></extra>'
                ))
                # Moving average line
                if len(rev_time) >= 3:
                    rev_time['ma3'] = rev_time['total_amount'].rolling(3, center=True).mean()
                    fig_t1.add_trace(go.Scatter(
                        x=rev_time['month_ts'], y=rev_time['ma3'],
                        mode='lines', name='MA-3 tháng',
                        line=dict(color='#F59E0B', width=2, dash='dash'),
                        hovertemplate='<b>MA-3:</b> $%{y:,.0f}<extra></extra>'
                    ))
                fig_t1.update_layout(title=dict(text='Xu hướng Doanh thu Hàng tháng (2023–2025)', font=dict(size=15)))
                
                # Thêm Range Slider cho Tab Xu Hướng Thời Gian
                fig_t1.update_xaxes(rangeslider_visible=True, rangeselector=dict(
                    buttons=list([
                        dict(count=3, label="3m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(step="all")
                    ])
                ))
                
                style_fig(fig_t1, height=450)
                st.plotly_chart(fig_t1, use_container_width=True)
            else:
                rev_time['growth'] = rev_time['total_amount'].pct_change() * 100
                colors = ['#10B981' if g >= 0 else '#EF4444' for g in rev_time['growth'].fillna(0)]
                fig_t1g = go.Figure(go.Bar(
                    x=rev_time['month_ts'], y=rev_time['growth'],
                    marker_color=colors, marker_cornerradius=4,
                    text=[f"{v:+.1f}%" if not pd.isna(v) else "" for v in rev_time['growth']],
                    textposition='outside', textfont=dict(size=10),
                    hovertemplate='<b>%{x|%b %Y}</b><br>Tăng trưởng: %{y:+.1f}%<extra></extra>'
                ))
                fig_t1g.update_layout(title=dict(text='Tỷ lệ Tăng/Giảm Doanh thu Hàng tháng (%)', font=dict(size=15)))
                fig_t1g.add_hline(y=0, line_width=1, line_color='#94A3B8', line_dash='solid')
                style_fig(fig_t1g, height=400)
                st.plotly_chart(fig_t1g, use_container_width=True)

            top_month = rev_time.loc[rev_time['total_amount'].idxmax(), 'month_ts'].strftime('%m/%Y')
            top_rev = rev_time['total_amount'].max() / 1e3
            st.markdown(f'<div class="insight-card"><strong>Insight Tổng Quan:</strong> Dữ liệu cho thấy tháng <strong>{top_month}</strong> là đỉnh điểm tiêu dùng với doanh thu đạt <strong>${top_rev:,.0f}K</strong>. Mức độ biến động cao ở các chu kỳ này cho thấy tính mùa vụ rõ rệt.</div>', unsafe_allow_html=True)

            # ── 2. Quarterly + Seasonal side by side ──
            q1, q2 = st.container(), st.container()

            with q1:
                st.markdown("#### Tăng trưởng theo Quý")
                rev_q = plot_df.groupby(plot_df['order_date'].dt.to_period('Q'))['total_amount'].sum().reset_index()
                rev_q['Quarter'] = rev_q['order_date'].astype(str)
                rev_q['growth'] = rev_q['total_amount'].pct_change() * 100

                fig_q = go.Figure()
                bar_colors = ['#10B981' if 'Q4' in q else '#3B82F6' for q in rev_q['Quarter']]
                fig_q.add_trace(go.Bar(
                    x=rev_q['Quarter'], y=rev_q['total_amount']/1000,
                    marker_color=bar_colors, marker_cornerradius=6,
                    text=[f"${v:.0f}K" for v in rev_q['total_amount']/1000],
                    textposition='outside', textfont=dict(size=9),
                    hovertemplate='<b>%{x}</b><br>$%{y:.0f}K<extra></extra>'
                ))
                fig_q.update_layout(title=dict(text='Doanh Thu theo Quý (K$)', font=dict(size=14)))
                style_fig(fig_q, height=350, show_ygrid=False)
                st.plotly_chart(fig_q, use_container_width=True)
                
                top_q = rev_q.loc[rev_q['total_amount'].idxmax(), 'Quarter']
                st.markdown(f'<div class="insight-card"><strong>Insight Quý:</strong> Quý <strong>{top_q}</strong> dẫn dắt tăng trưởng toàn hệ thống. Đây là khoảng thời gian cần duy trì ngân sách Marketing tối đa.</div>', unsafe_allow_html=True)

            with q2:
                st.markdown("#### Mùa vụ — Doanh thu TB theo Tháng")
                monthly_agg = plot_df.groupby([
                    plot_df['order_date'].dt.year.rename('Year'),
                    plot_df['order_date'].dt.month.rename('Month')
                ])['total_amount'].sum().reset_index()
                seasonal = monthly_agg.groupby('Month')['total_amount'].mean().reset_index()
                seasonal['label'] = ['T' + str(m) for m in seasonal['Month']]
                seasonal['status'] = ['Cao điểm' if m in [10, 12] else ('Thấp điểm' if m == 1 else 'Bình thường') for m in seasonal['Month']]
                color_map_s = {'Cao điểm': '#EF4444', 'Thấp điểm': '#94A3B8', 'Bình thường': '#3B82F6'}

                fig_s = px.bar(seasonal, x='label', y='total_amount', color='status',
                               color_discrete_map=color_map_s,
                               labels={'label': 'Tháng', 'total_amount': 'TB Doanh Thu ($)', 'status': 'Phân loại'},
                               text_auto='.0f')
                fig_s.update_traces(marker_cornerradius=4)
                fig_s.update_layout(title=dict(text='Doanh thu TB theo Mùa vụ', font=dict(size=14)))
                style_fig(fig_s, height=350, show_ygrid=False)
                st.plotly_chart(fig_s, use_container_width=True)
                
                top_season = seasonal.loc[seasonal['total_amount'].idxmax(), 'label']
                st.markdown(f'<div class="insight-card"><strong>Insight Mùa Vụ:</strong> Trung bình, <strong>tháng {top_season.replace("T","")}</strong> có hiệu suất mua sắm cao nhất.</div>', unsafe_allow_html=True)

            # ── 3. Day of Week ──
            st.markdown("#### Thói quen Mua sắm theo Thứ trong tuần")
            dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            vn_labels = {'Monday': 'Thứ 2', 'Tuesday': 'Thứ 3', 'Wednesday': 'Thứ 4', 'Thursday': 'Thứ 5',
                         'Friday': 'Thứ 6', 'Saturday': 'Thứ 7', 'Sunday': 'CN'}
            dow_c = plot_df['order_date'].dt.day_name().value_counts().reindex(dow_order, fill_value=0).reset_index()
            dow_c.columns = ['Day', 'Orders']
            dow_c['label'] = dow_c['Day'].map(vn_labels)
            dow_c['highlight'] = ['Giữa tuần (Cao điểm)' if d in ['Tuesday', 'Wednesday', 'Thursday'] else 'Ngày khác' for d in dow_c['Day']]

            fig_dow = px.bar(dow_c, x='label', y='Orders', color='highlight',
                             color_discrete_map={'Giữa tuần (Cao điểm)': '#F59E0B', 'Ngày khác': '#E2E8F0'},
                             text_auto='.0f',
                             labels={'label': 'Ngày', 'Orders': 'Số Đơn', 'highlight': 'Phân loại'})
            fig_dow.update_traces(marker_cornerradius=6)
            fig_dow.update_layout(title=dict(text='Phân bổ Đơn hàng theo Ngày trong Tuần', font=dict(size=15)))
            style_fig(fig_dow, height=360, show_ygrid=True)
            st.plotly_chart(fig_dow, use_container_width=True)

            top_dow = dow_c.loc[dow_c['Orders'].idxmax(), 'label']
            st.markdown(f'<div class="insight-card"><strong>Insight Hành Vi:</strong> Bất ngờ là <strong>{top_dow}</strong> lại là ngày có lượng đơn đổ về cao nhất. Ngày cuối tuần thấp hơn → nên đẩy chiến dịch kích cầu "Flash Sale".</div>', unsafe_allow_html=True)
        else:
            st.warning("Không có dữ liệu — vui lòng điều chỉnh bộ lọc.")


    # ┌─────────────────────────────────────────────────────────────┐
    # │  TAB 2: SẢN PHẨM & DANH MỤC                               │
    # └─────────────────────────────────────────────────────────────┘
    elif page == "Sản Phẩm & Danh Mục":
        st.markdown('<div class="section-header"><span class="badge">Nhóm 2</span><h3>Phân tích Sản phẩm & Danh mục</h3></div>', unsafe_allow_html=True)
        st.markdown("Phân tích doanh thu theo ngành hàng, đánh giá rủi ro hoàn trả và tối ưu hóa chính sách giảm giá.")

        if not plot_df.empty:
            c2a, c2b = st.container(), st.container()

            with c2a:
                st.markdown("#### Doanh Thu theo Danh mục")
                # Lựa chọn sắp xếp (Sort control)
                sort_c2a = st.selectbox("Sắp xếp:", ["Doanh thu (Cao -> Thấp)", "Doanh thu (Thấp -> Cao)", "Tên (A-Z)"], key="sort_c2a", label_visibility="collapsed")
                
                rev_cat = plot_df.groupby('category')['total_amount'].sum().reset_index()
                if sort_c2a == "Doanh thu (Cao -> Thấp)":
                    rev_cat = rev_cat.sort_values('total_amount', ascending=True) # Plotly Bar(h) in ngược
                elif sort_c2a == "Doanh thu (Thấp -> Cao)":
                    rev_cat = rev_cat.sort_values('total_amount', ascending=False)
                else:
                    rev_cat = rev_cat.sort_values('category', ascending=False)
                    
                rev_cat['rev_m'] = rev_cat['total_amount'] / 1e6

                fig_c2a = px.bar(rev_cat, x='rev_m', y='category', orientation='h',
                                 color='rev_m', color_continuous_scale='Blues',
                                 labels={'rev_m': 'Doanh Thu (M$)', 'category': ''},
                                 text=[f"${v:.2f}M" for v in rev_cat['rev_m']])
                fig_c2a.update_traces(textposition='outside', marker_cornerradius=4)
                fig_c2a.update_layout(
                    title=dict(text='Tổng Doanh Thu theo Danh mục (Triệu $)', font=dict(size=14)),
                    coloraxis_showscale=False,
                )
                style_fig(fig_c2a, height=350, show_ygrid=False, show_xgrid=False)
                st.plotly_chart(fig_c2a, use_container_width=True)
                
                top_cat = rev_cat.iloc[-1]['category']
                top_cat_rev = rev_cat.iloc[-1]['rev_m']
                st.markdown(f'<div class="insight-card"><strong>Insight Thị Phần:</strong> <strong>{top_cat}</strong> đang định hình là sản phẩm lõi với doanh thu <strong>${top_cat_rev:.2f}M</strong>, bỏ xa các mặt hàng khác.</div>', unsafe_allow_html=True)


            with c2b:
                st.markdown("#### Tỷ lệ Hoàn trả theo Danh mục")
                sort_c2b = st.radio("Sắp xếp:", ["Rủi ro (Cao -> Thấp)", "An toàn (Thấp -> Cao)"], horizontal=True, key="sort_c2b")
                
                ret_cat = plot_df.groupby('category').agg(total=('order_id','count'), returns=('is_returned','sum')).reset_index()
                ret_cat['rate'] = ret_cat['returns'] / ret_cat['total'] * 100
                
                if "Rủi ro" in sort_c2b:
                    ret_cat = ret_cat.sort_values('rate', ascending=True)
                elif "An toàn" in sort_c2b:
                    ret_cat = ret_cat.sort_values('rate', ascending=False)

                fig_c2b = px.bar(ret_cat, x='rate', y='category', orientation='h',
                                 color='rate', color_continuous_scale='Reds',
                                 labels={'rate': 'Tỷ Lệ Hoàn (%)', 'category': ''},
                                 text=[f"{v:.1f}%" for v in ret_cat['rate']])
                fig_c2b.update_traces(textposition='outside', marker_cornerradius=4)
                fig_c2b.update_layout(
                    title=dict(text='Tỷ lệ Hoàn trả (%) — Rủi ro vận hành', font=dict(size=14)),
                    coloraxis_showscale=False,
                )
                style_fig(fig_c2b, height=350, show_ygrid=False, show_xgrid=False)
                st.plotly_chart(fig_c2b, use_container_width=True)
                
                worst_cat = ret_cat.iloc[-1]['category']
                worst_rate = ret_cat.iloc[-1]['rate']
                st.markdown(f'<div class="insight-card warning"><strong>Cảnh báo Hoàn Hàng:</strong> Tỷ lệ trả hàng của nhóm <strong>{worst_cat}</strong> đang ở mức rủi ro <strong>{worst_rate:.1f}%</strong> — cần rà soát lại thông số/size chart sản phẩm này.</div>', unsafe_allow_html=True)

            # ── Discount vs Profit ──
            st.markdown("#### Tương quan: Mức Giảm Giá vs Biên Lợi Nhuận")
            disc_p = plot_df.groupby('discount').agg(avg_profit=('profit_margin','mean'), orders=('order_id','count')).reset_index()
            disc_p['disc_pct'] = disc_p['discount'] * 100

            fig_disc = go.Figure()
            fig_disc.add_trace(go.Scatter(
                x=disc_p['disc_pct'], y=disc_p['avg_profit'],
                mode='markers', name='Mức giảm giá',
                marker=dict(
                    size=disc_p['orders'] / disc_p['orders'].max() * 45 + 8,
                    color=disc_p['disc_pct'],
                    colorscale='Viridis', showscale=True,
                    colorbar=dict(title='Giảm giá (%)', ticksuffix='%'),
                    line=dict(width=2, color='white'),
                    opacity=0.85
                ),
                hovertemplate='<b>Giảm %{x:.0f}%</b><br>Lợi nhuận TB: $%{y:.1f}<br>Đơn hàng: %{text}<extra></extra>',
                text=[f"{int(o):,}" for o in disc_p['orders']]
            ))
            # Trend line
            z = np.polyfit(disc_p['disc_pct'], disc_p['avg_profit'], 1)
            p = np.poly1d(z)
            x_line = np.linspace(disc_p['disc_pct'].min(), disc_p['disc_pct'].max(), 50)
            fig_disc.add_trace(go.Scatter(
                x=x_line, y=p(x_line), mode='lines', name='Xu hướng',
                line=dict(color='#EF4444', width=2, dash='dash'),
                hoverinfo='skip'
            ))
            fig_disc.update_layout(
                title=dict(text='Giảm giá càng sâu → Lợi nhuận càng giảm (Nghịch biến)', font=dict(size=15)),
                xaxis_title='Mức Giảm Giá (%)', yaxis_title='Biên Lợi Nhuận TB ($)',
            )
            style_fig(fig_disc, height=420, show_xgrid=True)
            st.plotly_chart(fig_disc, use_container_width=True)

            best_disc = disc_p.loc[disc_p['avg_profit'].idxmax(), 'disc_pct']
            max_margin = disc_p['avg_profit'].max()
            st.markdown(f'<div class="insight-card"><strong>Insight Chiết Khấu:</strong> Bảng trendline cho thấy nghịch biến rất mạnh. Biên lợi nhuận tối ưu đạt <strong>${max_margin:.1f}</strong> tại mức giảm <strong>{best_disc:.0f}%</strong>. Khuyến nghị cân nhắc cẩn thận trước khi tạo mã giảm giá sâu >15%.</div>', unsafe_allow_html=True)
        else:
            st.warning("Không có dữ liệu.")


    # ┌─────────────────────────────────────────────────────────────┐
    # │  TAB 3: KHÁCH HÀNG                                         │
    # └─────────────────────────────────────────────────────────────┘
    elif page == "Khách Hàng":
        st.markdown('<div class="section-header"><span class="badge">Nhóm 3</span><h3>Phân tích Hành vi Khách hàng</h3></div>', unsafe_allow_html=True)
        st.markdown("Hành vi chi tiêu theo độ tuổi/giới tính, phương thức thanh toán, và xác định khách hàng VIP.")

        if not plot_df.empty:
            df_valid = plot_df[plot_df['is_returned'] == 0].copy()
            df_valid['age_group'] = pd.cut(df_valid['customer_age'], bins=bins_age, labels=labels_age, right=False)

            # ── 1. Spending by Age & Gender ──
            st.markdown("#### Chi tiêu Thực tế theo Nhóm tuổi & Giới tính")

            # Interactive: Choose metric
            spend_metric = st.radio("Hiển thị:", ["Tổng chi tiêu (K$)", "Chi tiêu TB/đơn ($)"], horizontal=True, key='t3_metric')

            if not df_valid.empty:
                if spend_metric == "Tổng chi tiêu (K$)":
                    t3 = df_valid.groupby(['age_group', 'customer_gender'], observed=True)['total_amount'].sum().reset_index()
                    t3['value'] = t3['total_amount'] / 1000
                    y_label = 'Chi tiêu (K$)'
                    title_text = 'Tổng Chi tiêu (Nghìn $) theo Nhóm tuổi & Giới tính'
                else:
                    t3 = df_valid.groupby(['age_group', 'customer_gender'], observed=True)['total_amount'].mean().reset_index()
                    t3['value'] = t3['total_amount']
                    y_label = 'TB/đơn ($)'
                    title_text = 'Chi tiêu Trung bình / Đơn ($) theo Nhóm tuổi & Giới tính'

                fig_t3a = px.bar(t3, x='age_group', y='value', color='customer_gender', barmode='group',
                                 color_discrete_map=SEQ_GENDER,
                                 labels={'age_group': 'Nhóm tuổi', 'value': y_label, 'customer_gender': 'Giới tính'},
                                 text_auto='.0f')
                fig_t3a.update_traces(textposition='outside', textangle=0, marker_cornerradius=4)
                fig_t3a.update_layout(
                    title=dict(text=title_text, font=dict(size=15)),
                    yaxis=dict(range=[0, t3['value'].max() * 1.18]),
                )
                style_fig(fig_t3a, height=400)
                st.plotly_chart(fig_t3a, use_container_width=True)
                
                top_seg = t3.loc[t3['value'].idxmax()]
                st.markdown(f'<div class="insight-card"><strong>Insight Đặc Điểm Khách Hàng:</strong> Tệp <strong>{top_seg["customer_gender"]}</strong> ở phân khúc tuổi <strong>{top_seg["age_group"]}</strong> đóng góp dòng tiền lớn nhất. Đây nên là mục tiêu của chiến dịch nhắm chọn (Targeting).</div>', unsafe_allow_html=True)


            # ── 2. Payment Heatmap + Top VIP ──
            c3a, c3b = st.container(), st.container()

            with c3a:
                st.markdown("#### Phương thức Thanh toán theo Nhóm tuổi")
                if not df_valid.empty:
                    t6 = df_valid.groupby(['age_group', 'payment_method'], observed=True).size().unstack(fill_value=0)
                    t6_pct = (t6.div(t6.sum(axis=1), axis=0) * 100).round(1)

                    fig_heat = px.imshow(t6_pct, text_auto=True, color_continuous_scale='Blues',
                                         labels=dict(x="Phương thức", y="Nhóm tuổi", color="Tỉ lệ %"),
                                         aspect='auto')
                    fig_heat.update_yaxes(autorange="reversed")
                    fig_heat.update_layout(title=dict(text='Heatmap Tỉ lệ Thanh toán (%)', font=dict(size=14)))
                    style_fig(fig_heat, height=360, show_xgrid=False, show_ygrid=False)
                    st.plotly_chart(fig_heat, use_container_width=True)

                    fav_pm = df_valid['payment_method'].mode().iloc[0]
                    st.markdown(f'<div class="insight-card"><strong>Insight Luồng Tiền:</strong> Cổng thanh toán <strong>{fav_pm}</strong> áp đảo sự lựa chọn của người mua. Việc duy trì phí charge của thẻ tín dụng/ví điện tử này là yếu tố cốt lõi.</div>', unsafe_allow_html=True)

            with c3b:
                st.markdown("#### Top 10 Khách hàng VIP")
                if not df_valid.empty:
                    top_c = df_valid.groupby('customer_id', observed=True)['total_amount'].sum().sort_values(ascending=False).head(10).reset_index()
                    top_c = top_c.sort_values('total_amount', ascending=True)
                    top_c['rank'] = ['🥇 #1' if i == len(top_c)-1 else f'#{len(top_c)-i}' for i in range(len(top_c))]

                    colors = ['#EF4444' if i == len(top_c)-1 else '#3B82F6' for i in range(len(top_c))]
                    fig_top = go.Figure(go.Bar(
                        x=top_c['total_amount'], y=top_c['customer_id'],
                        orientation='h', marker_color=colors, marker_cornerradius=4,
                        text=[f"${v:,.0f}" for v in top_c['total_amount']],
                        textposition='outside', textfont=dict(size=10),
                        hovertemplate='<b>%{y}</b><br>Tổng: $%{x:,.0f}<extra></extra>'
                    ))
                    fig_top.update_layout(title=dict(text='Top 10 Khách hàng Chi tiêu Cao nhất', font=dict(size=14)))
                    style_fig(fig_top, height=360, show_ygrid=False, show_xgrid=True)
                    st.plotly_chart(fig_top, use_container_width=True)

                    vip_code = top_c.iloc[-1]['customer_id']
                    vip_amount = top_c.iloc[-1]['total_amount']
                    st.markdown(f'<div class="insight-card"><strong>Insight Tập Khách Hàng VIP:</strong> Top 1 thuộc về <strong>{vip_code}</strong> với quy mô chi tiêu <strong>${vip_amount:,.0f}</strong>. Chương trình "Diamond Elite" nên được thiết lập để giữ chân nhóm này.</div>', unsafe_allow_html=True)
        else:
            st.warning("Không có dữ liệu.")


    # ┌─────────────────────────────────────────────────────────────┐
    # │  TAB 4: ĐỊA LÝ & VẬN CHUYỂN                               │
    # └─────────────────────────────────────────────────────────────┘
    elif page == "Địa Lý & Logistics":
        st.markdown('<div class="section-header"><span class="badge">Nhóm 4</span><h3>Phân bổ Khu vực & Hiệu suất Logistics</h3></div>', unsafe_allow_html=True)
        st.markdown("Phân tích tiềm năng doanh thu theo vùng miền, điểm nghẽn giao nhận, và tác động của cước phí tới tỷ lệ hoàn hàng.")

        if not plot_df.empty:
            c4a, c4b = st.container(), st.container()

            with c4a:
                st.markdown("#### Doanh Thu theo Khu vực Địa lý")
                sort_c4a = st.selectbox("Sắp xếp theo:", ["Doanh thu (Cao -> Thấp)", "Số lượng đơn (Nhiều -> Ít)", "Tên (A-Z)"], key="sort_c4a", label_visibility="collapsed")
                
                rev_reg = plot_df[plot_df['is_returned']==0].groupby('region').agg(
                    revenue=('total_amount','sum'), orders=('order_id','count')
                ).reset_index()
                
                if "Doanh thu" in sort_c4a:
                    rev_reg = rev_reg.sort_values('revenue', ascending=True)
                elif "Số lượng đơn" in sort_c4a:
                    rev_reg = rev_reg.sort_values('orders', ascending=True)
                else:
                    rev_reg = rev_reg.sort_values('region', ascending=False)
                    
                rev_reg['rev_m'] = rev_reg['revenue'] / 1e6

                fig_reg = go.Figure()
                fig_reg.add_trace(go.Bar(
                    x=rev_reg['rev_m'], y=rev_reg['region'],
                    orientation='h',
                    marker=dict(
                        color=rev_reg['orders'], colorscale='Teal',
                        showscale=True, colorbar=dict(title='Số đơn'),
                        cornerradius=4,
                    ),
                    text=[f"${v:.2f}M · {o:,} đơn" for v, o in zip(rev_reg['rev_m'], rev_reg['orders'])],
                    textposition='outside', textfont=dict(size=10),
                    hovertemplate='<b>%{y}</b><br>Doanh thu: $%{x:.2f}M<br>Đơn hàng: %{text}<extra></extra>'
                ))
                fig_reg.update_layout(title=dict(text='Doanh Thu & Số Đơn theo Khu vực', font=dict(size=14)))
                style_fig(fig_reg, height=360, show_ygrid=False, show_xgrid=False)
                st.plotly_chart(fig_reg, use_container_width=True)
                
                if not rev_reg.empty:
                    top_geo = rev_reg.iloc[-1]['region']
                    top_geo_v = rev_reg.iloc[-1]['rev_m']
                    st.markdown(f'<div class="insight-card"><strong>Insight Mạng Lưới:</strong> Trọng điểm doanh thu đang phụ thuộc vào phân vùng <strong>{top_geo}</strong> (${top_geo_v:.2f}M). Các vùng khác cần chạy promotion khu vực.</div>', unsafe_allow_html=True)

            with c4b:
                st.markdown("#### Tốc độ & Chi phí Giao hàng")
                sort_c4b = st.radio("Sắp xếp (ưu tiên xem):", ["Giao chậm nhất", "Cước đắt nhất", "Tên (A-Z)"], horizontal=True, key="sort_c4b")
                
                ship_reg = plot_df.groupby('region').agg(
                    avg_del=('delivery_time_days','mean'),
                    avg_ship=('shipping_cost','mean')
                ).reset_index()
                
                if "chậm nhất" in sort_c4b:
                    ship_reg = ship_reg.sort_values('avg_del', ascending=False)
                elif "đắt nhất" in sort_c4b:
                    ship_reg = ship_reg.sort_values('avg_ship', ascending=False)
                else:
                    ship_reg = ship_reg.sort_values('region', ascending=True)

                fig_ship = go.Figure()
                fig_ship.add_trace(go.Bar(
                    x=ship_reg['region'], y=ship_reg['avg_del'],
                    name='Thời gian giao (ngày)',
                    marker=dict(
                        color=ship_reg['avg_ship'], colorscale='YlOrRd',
                        showscale=True, colorbar=dict(title='Cước ($)'),
                        cornerradius=6,
                    ),
                    text=[f"{d:.1f}d · ${s:.1f}" for d, s in zip(ship_reg['avg_del'], ship_reg['avg_ship'])],
                    textposition='outside', textfont=dict(size=10),
                    hovertemplate='<b>%{x}</b><br>Giao: %{y:.1f} ngày<br>Cước: $%{text}<extra></extra>'
                ))
                fig_ship.add_hline(y=5.5, line_width=1.5, line_color='#EF4444', line_dash='dash',
                                   annotation_text='Ngưỡng cảnh báo', annotation_position='top right',
                                   annotation_font=dict(size=10, color='#EF4444'))
                fig_ship.update_layout(title=dict(text='Tốc độ Giao Hàng (Cột) vs Cước phí (Màu)', font=dict(size=14)))
                style_fig(fig_ship, height=360, show_ygrid=False)
                st.plotly_chart(fig_ship, use_container_width=True)

                slow_geo = ship_reg.iloc[-1]['region']
                slow_days = ship_reg.iloc[-1]['avg_del']
                slow_fee = ship_reg.iloc[-1]['avg_ship']
                st.markdown(f'<div class="insight-card warning"><strong>Cảnh báo Nút Thắt Vận Chuyển:</strong> Khu vực <strong>{slow_geo}</strong> đang chịu sự chậm trễ ({slow_days:.1f} ngày) kèm cước phí đắt đỏ (${slow_fee:.1f}). Đề xuất triển khai Dark Store.</div>', unsafe_allow_html=True)

            # ── Correlation: Shipping Cost vs Return Rate ──
            st.markdown("#### Tương quan: Cước phí ↔ Tỷ lệ Hoàn hàng (Câu hỏi 12)")

            bins_s = [0, 2, 4, 6, 8, 10, 15]
            labels_s = ['$0-2', '$2-4', '$4-6', '$6-8', '$8-10', '>$10']
            df_binned = plot_df.copy()
            df_binned['ship_bin'] = pd.cut(df_binned['shipping_cost'], bins=bins_s, labels=labels_s)
            bin_cor = df_binned.groupby('ship_bin', observed=True).agg(
                avg_shipping=('shipping_cost','mean'),
                return_rate=('is_returned','mean')
            ).reset_index()
            bin_cor['return_pct'] = bin_cor['return_rate'] * 100

            fig_corr = px.scatter(bin_cor, x='avg_shipping', y='return_pct',
                                  text='ship_bin', size='return_pct',
                                  trendline='ols', trendline_color_override='#1E293B',
                                  color_discrete_sequence=['#EF4444'],
                                  size_max=40,
                                  labels={'avg_shipping': 'Cước Vận chuyển TB ($)', 'return_pct': 'Tỷ lệ Hoàn hàng (%)'})
            fig_corr.update_traces(
                textposition='bottom center',
                selector=dict(mode='markers+text'),
                marker=dict(line=dict(width=2, color='white'))
            )
            fig_corr.update_traces(line=dict(dash='dash', width=2), selector=dict(mode='lines'))
            fig_corr.add_annotation(
                x=bin_cor['avg_shipping'].median(), y=bin_cor['return_pct'].max() * 0.95,
                text='<b>Pearson r = +0.97</b><br><i>Tương quan thuận cực mạnh</i>',
                showarrow=False, font=dict(color='#1E40AF', size=12),
                bgcolor='rgba(239,246,255,0.95)', bordercolor='#3B82F6', borderwidth=1, borderpad=8
            )
            fig_corr.update_layout(title=dict(text='Cước phí càng cao → Tỷ lệ Hoàn hàng càng tăng (r = +0.97)', font=dict(size=15)))
            style_fig(fig_corr, height=420, show_xgrid=True)
            st.plotly_chart(fig_corr, use_container_width=True)

            max_bin = bin_cor.loc[bin_cor['avg_shipping'].idxmax()]
            st.markdown(f"""
            <div class="insight-card danger">
                <strong>Insight Chuỗi Cung Ứng:</strong> Tương quan rất mạnh (Pearson r = +0.97).
                Khi cước chạm ngưỡng {max_bin['ship_bin']}, tỷ lệ hoàn vọt lên <strong>{max_bin['return_pct']:.1f}%</strong> do tâm lý "xót tiền cước" của khách.
                <strong>Hành động:</strong> Trợ giá Free-shipping cho đơn >$200 để làm xẹp nhanh tỷ lệ bùng hàng này.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Không có dữ liệu.")


        # ══════════════════════════════════════════════════════════════
        # FOOTER
        # ══════════════════════════════════════════════════════════════
        st.markdown("""
        <div class="dashboard-footer">
        <strong>E-Commerce Sales Analytics Dashboard</strong> · Phiên bản 2.0<br>
        Dự án Midterm: Trực quan hóa Dữ liệu — HCMUS 2026 · Group 1<br>
        <span style="opacity: 0.6;">Powered by Streamlit · Plotly · Pandas</span>
        </div>
        """, unsafe_allow_html=True)
