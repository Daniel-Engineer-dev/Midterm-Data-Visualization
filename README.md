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
- `report/`: Chứa khung báo cáo LaTeX hoàn thiện cho dự án.
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

## Hướng dẫn Cài đặt MiKTeX & Biên dịch Báo cáo LaTeX

### Bước 1: Tải và cài đặt MiKTeX

1. Truy cập trang chủ MiKTeX: [https://miktex.org/download](https://miktex.org/download)
2. Tải bản cài đặt phù hợp với hệ điều hành (Windows / macOS / Linux).
3. Chạy file cài đặt và làm theo hướng dẫn:
   - Chọn **"Install missing packages on-the-fly: Yes"** để MiKTeX tự động tải các gói LaTeX khi cần.
   - Chọn cài đặt cho **All Users** (khuyến nghị) hoặc **Current User**.
4. Sau khi cài đặt xong, mở **MiKTeX Console** và chọn **Updates > Check for updates** để cập nhật các gói mới nhất.

### Bước 2: Cài đặt Perl (bắt buộc cho `latexmk`)

`latexmk` yêu cầu Perl để hoạt động:

- **Windows**: Tải và cài đặt [Strawberry Perl](https://strawberryperl.com/). Sau khi cài, khởi động lại máy tính.
- **macOS / Linux**: Perl đã được cài sẵn.

Kiểm tra Perl đã cài thành công:
```bash
perl --version
```

### Bước 3: Thêm MiKTeX vào biến môi trường PATH (nếu cần)

Nếu các lệnh `pdflatex`, `latexmk` không nhận được trong terminal, cần thêm MiKTeX vào PATH:

- **Windows**:
  1. Tìm thư mục cài đặt MiKTeX, thường là: `C:\Users\<TenUser>\AppData\Local\Programs\MiKTeX\miktex\bin\x64\`
  2. Mở **Settings > System > About > Advanced system settings > Environment Variables**.
  3. Trong **System variables**, chọn `Path` > **Edit** > **New** > dán đường dẫn trên > **OK**.
  4. Khởi động lại terminal / VS Code.

Kiểm tra cài đặt thành công:
```bash
pdflatex --version
latexmk --version
```

### Bước 4: Cài đặt Extension LaTeX Workshop (VS Code)

1. Mở VS Code, vào tab **Extensions** (`Ctrl+Shift+X`).
2. Tìm kiếm **"LaTeX Workshop"** (tác giả: James Yu).
3. Nhấn **Install**.
4. Sau khi cài, mở file `.tex` bất kỳ và nhấn `Ctrl+Alt+B` để biên dịch hoặc lưu file (`Ctrl+S`) để tự động biên dịch.

### Bước 5: Biên dịch báo cáo

#### Cách 1: Biên dịch bằng VS Code (LaTeX Workshop)
- Mở file `report/main.tex` trong VS Code.
- Lưu file (`Ctrl+S`) → LaTeX Workshop sẽ tự động biên dịch.
- File PDF sẽ được tạo tại `report/main.pdf`.

#### Cách 2: Biên dịch bằng dòng lệnh
```bash
cd report
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```
> **Lưu ý:** Chạy `pdflatex` nhiều lần để cập nhật mục lục, tham chiếu chéo và danh mục tài liệu tham khảo. Lệnh `biber` dùng để xử lý file `.bib` (tài liệu tham khảo).

#### Cách 3: Biên dịch bằng `latexmk` (khuyến nghị)
```bash
cd report
latexmk -pdf main.tex
```

## Kế hoạch Thực hiện
- **Tuần 3**: Nộp Proposal + Thu thập & làm sạch dữ liệu.
- **Tuần 4**: Phân tích What-Why chi tiết + Tạo biến phái sinh.
- **Tuần 5**: Thiết kế & cài đặt Dashboard + Viết báo cáo.
- **Tuần 6**: Hoàn thiện Dashboard, báo cáo & Trình bày.
