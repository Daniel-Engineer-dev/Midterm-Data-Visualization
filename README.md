# Phân tích Hiệu suất Kinh doanh Thương mại Điện tử

## Giới thiệu Dự án
Dự án tập trung vào việc phân tích hiệu suất bán hàng thương mại điện tử qua các xu hướng thời gian, hành vi khách hàng và phân bổ địa lý. Mục tiêu chính là xây dựng một **Interactive Dashboard** (Bằng Streamlit/Dash hoặc Tableau) giúp giải quyết các câu hỏi kinh doanh quan trọng và trực quan hóa dữ liệu giao dịch từ Kaggle.

## Thành viên Nhóm
1.  **Lê Lâm Trí Đức (23120237)**: Trưởng nhóm --- Thiết kế Dashboard & Tổng hợp báo cáo
2.  **Phạm Quang Vinh (23120202)**: Xử lý & Làm sạch dữ liệu
3.  **Nguyễn Lê Thế Vinh (23120190)**: Phân tích What-Why & Viết báo cáo
4.  **Hoàng Quốc Việt (23120189)**: Thiết kế biểu đồ & Cài đặt tương tác

## Dữ liệu
- **Tên dataset**: E-commerce Sales Transactions Dataset
- **Nguồn**: [Kaggle](https://www.kaggle.com/datasets/miadul/e-commerce-sales-transactions-dataset)
- **Quy mô**: 34,500 bản ghi với 17 thuộc tính.
- **Giấy phép**: Apache 2.0

## Cấu trúc Thư mục
- `Requirements/`: Chứa các yêu cầu và ảnh chụp đề bài.
- `Proposal/`: Chứa các tệp nguồn LaTeX cho bản đề xuất dự án.
- `data/`: Chứa dữ liệu gốc (raw) và dữ liệu đã qua xử lý (processed).
- `dashboard/`: Chứa mã nguồn của interactive dashboard (Python/Streamlit).
- `notebook/`: Chứa các file Jupyter Notebook phục vụ quá trình làm sạch và phân tích dữ liệu (EDA).

## Hướng dẫn Cài đặt & Chạy Dashboard
*Đang cập nhật (Dành cho bản Streamlit)*

1. Cài đặt môi trường ảo:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Trên Windows: venv\Scripts\activate
   ```
2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```
3. Chạy dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```

## Kế hoạch Thực hiện
- **Tuần 3**: Nộp Proposal + Thu thập & làm sạch dữ liệu.
- **Tuần 4**: Phân tích What-Why chi tiết + Tạo biến phái sinh.
- **Tuần 5**: Thiết kế & cài đặt Dashboard + Viết báo cáo.
- **Tuần 6**: Hoàn thiện Dashboard, báo cáo & Trình bày.
