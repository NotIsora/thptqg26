# So Sánh Tổ Hợp Xét Tuyển THPT 2025

Ứng dụng giúp học sinh tra cứu, tính toán và so sánh trực quan thứ hạng điểm thi THPT của mình giữa các tổ hợp môn khác nhau trên toàn TP.HCM.

> [!TIP]
> **Xem trực tiếp (Không cần cài đặt)**: Dự án đã được đóng gói thành phiên bản tĩnh, bạn chỉ cần mở file `index.html` trực tiếp trong trình duyệt hoặc kích hoạt **GitHub Pages** trên repository này để xem online mọi lúc mọi nơi!

## Tính Năng Nổi Bật

- **Tính điểm thi tốt nghiệp thuần**: Không cộng điểm học bạ hay tự động làm tròn điểm ngoại ngữ, phản ánh chính xác điểm thi thực tế.
- **So sánh đa tổ hợp**: Cho phép chọn nhiều khối thi cùng lúc (Khối A, B, C, D, các tổ hợp mới có Tin học và Công nghệ).
- **Thống kê chi tiết**:
  - Thứ hạng của bạn trên tổng số thí sinh của toàn Thành phố Hồ Chí Minh.
  - Số lượng thí sinh đạt điểm cao hơn bạn.
  - Tỉ lệ phần trăm vượt qua.
  - Điểm trung bình, trung vị và điểm cao nhất của từng tổ hợp.
- **Biểu đồ trực quan (Chart.js)**: So sánh thứ hạng và tỉ lệ cạnh tranh bằng biểu đồ cột tương tác.
- **Chạy offline 100%**: Sử dụng dữ liệu thống kê tần suất nén trong `data.js`, tải tức thì và không cần database server.

## Hướng Dẫn Sử Dụng

### Cách 1: Sử dụng Bản Tĩnh (Nhanh nhất & Chạy offline)
Bạn chỉ cần mở trực tiếp file [index.html](index.html) bằng bất kỳ trình duyệt nào (Edge, Chrome, Safari, Firefox). Ứng dụng sẽ đọc trực tiếp dữ liệu từ file `data.js` và thực hiện mọi tính toán ngay trong trình duyệt của bạn.

Để xuất bản lên mạng qua **GitHub Pages**:
1. Vào phần cài đặt (Settings) của Repository này trên GitHub.
2. Chọn mục **Pages** ở thanh bên trái.
3. Trong phần **Build and deployment** -> **Source**, chọn **Deploy from a branch**.
4. Chọn nhánh **main** (hoặc master) và thư mục gốc `/ (root)`, sau đó nhấn **Save**.
5. Đợi 1-2 phút, GitHub sẽ cung cấp cho bạn một đường link chạy online miễn phí!

---

### Cách 2: Sử dụng Bản Động (Python Flask Backend)
Nếu bạn muốn tự cập nhật/chạy dữ liệu Excel mới hoặc phát triển thêm tính năng backend:

1. **Cài đặt thư viện**:
   ```bash
   pip install flask pandas openpyxl
   ```
2. **Chuẩn bị dữ liệu**: Đặt file Excel điểm thi vào thư mục gốc với tên `diem_thi_hcm.xlsx` (đã được ẩn trong `.gitignore` để tránh bị đẩy lên GitHub).
3. **Cập nhật dữ liệu tĩnh (tùy chọn)**: Nếu có file Excel mới, bạn có thể chạy lệnh sau để xuất bản lại file dữ liệu tĩnh `data.js`:
   ```bash
   python build_static_data.py
   ```
4. **Khởi động server**:
   ```bash
   python app.py
   ```
   Truy cập `http://127.0.0.1:5000` trên trình duyệt của bạn.
