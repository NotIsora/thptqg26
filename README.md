# So Sánh Tổ Hợp Xét Tuyển THPT 2025

Ứng dụng web được xây dựng bằng Python (Flask) và HTML/CSS/JS (giao diện Glassmorphism hiện đại) giúp học sinh tra cứu, tính toán và so sánh trực quan thứ hạng điểm thi THPT của mình giữa các tổ hợp môn khác nhau.

## Tính Năng Nổi Bật

- **Tính điểm thi tốt nghiệp thuần**: Không cộng điểm học bạ hay tự động làm tròn điểm ngoại ngữ, phản ánh chính xác điểm thi thực tế.
- **So sánh đa tổ hợp**: Cho phép chọn nhiều khối thi cùng lúc (Khối A, B, C, D, các tổ hợp mới có Tin học và Công nghệ).
- **Thống kê chi tiết**:
  - Thứ hạng của bạn trên tổng số thí sinh của toàn Thành phố Hồ Chí Minh.
  - Số lượng thí sinh đạt điểm cao hơn bạn.
  - Tỉ lệ phần trăm vượt qua.
  - Điểm trung bình, trung vị và điểm cao nhất của từng tổ hợp.
- **Biểu đồ trực quan (Chart.js)**: So sánh thứ hạng và tỉ lệ cạnh tranh bằng biểu đồ cột tương tác.
- **Giao diện Glassmorphism**: Thiết kế tối màu hiện đại, hiệu ứng kính mờ tinh tế và tương thích tốt trên mọi thiết bị di động/máy tính.

## Hướng Dẫn Sử Dụng

### 1. Yêu cầu hệ thống
Đảm bảo máy tính của bạn đã cài đặt Python 3.x.

### 2. Cài đặt các thư viện cần thiết
Mở terminal tại thư mục dự án và chạy lệnh:
```bash
pip install flask pandas openpyxl
```

### 3. Chuẩn bị file dữ liệu
Đặt file điểm thi Excel (ví dụ: `diem_thi_hcm.xlsx`) vào thư mục gốc của dự án. 
*(Lưu ý: File dữ liệu này đã được thêm vào `.gitignore` để tránh bị đẩy lên GitHub công khai).*

### 4. Khởi động ứng dụng
Chạy lệnh khởi động server:
```bash
python app.py
```

Truy cập địa chỉ `http://127.0.0.1:5000` trên trình duyệt để sử dụng ứng dụng.
