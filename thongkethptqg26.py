import pandas as pd
from bisect import bisect_right
import math
import sys

def get_score(diem_thi, subject):
    idx = diem_thi.find(subject)
    if idx == -1:
        return None
    
    start = idx + len(subject)
    while start < len(diem_thi) and diem_thi[start] in (' ', '\t'):
        start += 1
    end = start
    while end < len(diem_thi) and diem_thi[end] not in (' ', '\t'):
        end += 1
        
    try:
        val = float(diem_thi[start:end])
        if math.isnan(val):
            return None
        return val
    except ValueError:
        return None

def solve():
    # Cấu hình UTF-8 cho console để in tiếng Việt không bị lỗi UnicodeEncodeError trên Windows
    if sys.platform.startswith('win'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')

    # Danh sách tất cả tổ hợp xét tuyển truyền thống 2026 (Khối A, B, C, D)
    combinations_list = [
        # Khối A
        ("Toán", "Vật lí", "Hóa học"),     # A00
        ("Toán", "Vật lí", "Tiếng Anh"),    # A01
        ("Toán", "Vật lí", "Sinh học"),    # A02
        ("Toán", "Vật lí", "Lịch sử"),      # A03
        ("Toán", "Vật lí", "Địa lí"),      # A04
        ("Toán", "Hóa học", "Lịch sử"),     # A05
        ("Toán", "Hóa học", "Địa lí"),     # A06
        ("Toán", "Lịch sử", "Địa lí"),     # A07
        ("Toán", "Lịch sử", "Giáo dục kinh tế và pháp luật"), # A08
        ("Toán", "Địa lí", "Giáo dục kinh tế và pháp luật"), # A09
        ("Toán", "Vật lí", "Giáo dục kinh tế và pháp luật"), # A10
        ("Toán", "Hóa học", "Giáo dục kinh tế và pháp luật"), # A11

        # Khối B
        ("Toán", "Hóa học", "Sinh học"),   # B00
        ("Toán", "Sinh học", "Địa lí"),   # B02
        ("Toán", "Sinh học", "Ngữ văn"),   # B03
        ("Toán", "Sinh học", "Giáo dục kinh tế và pháp luật"), # B04
        ("Toán", "Sinh học", "Tiếng Anh"),  # B08

        # Khối C
        ("Ngữ văn", "Lịch sử", "Địa lí"),  # C00
        ("Ngữ văn", "Toán", "Vật lí"),     # C01
        ("Ngữ văn", "Toán", "Hóa học"),    # C02
        ("Ngữ văn", "Toán", "Lịch sử"),    # C03
        ("Ngữ văn", "Toán", "Địa lí"),     # C04
        ("Ngữ văn", "Vật lí", "Hóa học"),  # C05
        ("Ngữ văn", "Vật lí", "Sinh học"), # C06
        ("Ngữ văn", "Hóa học", "Sinh học"), # C08
        ("Ngữ văn", "Lịch sử", "Sinh học"), # C12
        ("Ngữ văn", "Sinh học", "Địa lí"), # C13
        ("Ngữ văn", "Toán", "Giáo dục kinh tế và pháp luật"), # C14
        ("Ngữ văn", "Hóa học", "Giáo dục kinh tế và pháp luật"), # C17
        ("Ngữ văn", "Lịch sử", "Giáo dục kinh tế và pháp luật"), # C19
        ("Ngữ văn", "Địa lí", "Giáo dục kinh tế và pháp luật"), # C20

        # Khối D (Anh, Nga, Pháp, Trung, Đức, Nhật)
        ("Ngữ văn", "Toán", "Tiếng Anh"),  # D01
        ("Ngữ văn", "Toán", "Tiếng Nga"),  # D02
        ("Ngữ văn", "Toán", "Tiếng Pháp"), # D03
        ("Ngữ văn", "Toán", "Tiếng Trung"),# D04
        ("Ngữ văn", "Toán", "Tiếng Đức"),  # D05
        ("Ngữ văn", "Toán", "Tiếng Nhật"), # D06
        ("Toán", "Hóa học", "Tiếng Anh"),  # D07
        ("Toán", "Sinh học", "Tiếng Anh"), # D08
        ("Toán", "Lịch sử", "Tiếng Anh"),  # D09
        ("Toán", "Địa lí", "Tiếng Anh"),   # D10
        ("Ngữ văn", "Vật lí", "Tiếng Anh"), # D11
        ("Ngữ văn", "Hóa học", "Tiếng Anh"), # D12
        ("Ngữ văn", "Sinh học", "Tiếng Anh"), # D13
        ("Ngữ văn", "Lịch sử", "Tiếng Anh"), # D14
        ("Ngữ văn", "Địa lí", "Tiếng Anh"), # D15
        ("Toán", "Địa lí", "Tiếng Trung"), # D20
        ("Toán", "Hóa học", "Tiếng Đức"),  # D21
        ("Toán", "Hóa học", "Tiếng Nga"),  # D22
        ("Toán", "Hóa học", "Tiếng Nhật"), # D23
        ("Toán", "Hóa học", "Tiếng Pháp"), # D24
        ("Toán", "Hóa học", "Tiếng Trung"),# D25
        ("Toán", "Vật lí", "Tiếng Đức"),  # D26
        ("Toán", "Vật lí", "Tiếng Nga"),  # D27
        ("Toán", "Vật lí", "Tiếng Nhật"), # D28
        ("Toán", "Vật lí", "Tiếng Pháp"), # D29
        ("Toán", "Vật lí", "Tiếng Trung"), # D30
        ("Toán", "Sinh học", "Tiếng Đức"), # D31
        ("Toán", "Sinh học", "Tiếng Nga"), # D32
        ("Toán", "Sinh học", "Tiếng Nhật"),# D33
        ("Toán", "Sinh học", "Tiếng Pháp"),# D34
        ("Toán", "Sinh học", "Tiếng Trung"),# D35
        ("Ngữ văn", "Địa lí", "Tiếng Nga"), # D42
        ("Ngữ văn", "Địa lí", "Tiếng Nhật"),# D43
        ("Ngữ văn", "Địa lí", "Tiếng Pháp"),# D44
        ("Ngữ văn", "Địa lí", "Tiếng Trung"),# D45
        ("Ngữ văn", "Vật lí", "Tiếng Trung"),# D55
        ("Ngữ văn", "Lịch sử", "Tiếng Nhật"),# D63
        ("Ngữ văn", "Lịch sử", "Tiếng Pháp"),# D64
        ("Ngữ văn", "Lịch sử", "Tiếng Trung"),# D65
        ("Ngữ văn", "Giáo dục kinh tế và pháp luật", "Tiếng Anh"), # D66
        ("Ngữ văn", "Giáo dục kinh tế và pháp luật", "Tiếng Nga"), # D68
        ("Ngữ văn", "Giáo dục kinh tế và pháp luật", "Tiếng Pháp"),# D70
        ("Ngữ văn", "Giáo dục kinh tế và pháp luật", "Tiếng Trung"),# D71
        ("Toán", "Tiếng Anh", "Giáo dục kinh tế và pháp luật"),  # D84

        # Các tổ hợp môn mới liên quan đến Tin học & Công nghệ (2026)
        ("Toán", "Tin học", "Tiếng Anh"),
        ("Toán", "Tin học", "Vật lí"),
        ("Toán", "Tin học", "Hóa học"),
        ("Toán", "Tin học", "Sinh học"),
        ("Toán", "Công nghệ", "Tiếng Anh"),
        ("Toán", "Công nghệ", "Vật lí"),
        ("Toán", "Công nghệ", "Hóa học"),
        ("Toán", "Công nghệ", "Sinh học"),
    ]

    scores = []
    file_path = 'diem_thi_hcm.xlsx'
    
    print("Đang đọc dữ liệu từ file Excel (có thể mất vài giây)...")
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Lỗi: Không thể đọc file Excel: {e}")
        return
        
    # Tự động dò tìm cột chứa chuỗi điểm thi
    diem_thi_col = None
    for col in df.columns:
        sample = df[col].dropna().head(10)
        if any(isinstance(val, str) and 'Toán:' in val for val in sample):
            diem_thi_col = col
            break
            
    if not diem_thi_col:
        # Fallback về cột thứ 3 nếu không tự động tìm được
        if len(df.columns) >= 3:
            diem_thi_col = df.columns[2]
        else:
            diem_thi_col = df.columns[-1]
            
    print(f"-> Đã tìm thấy cột chứa điểm: '{diem_thi_col}'")

    # 2. Bắt đầu pipeline xử lý dữ liệu
    for val in df[diem_thi_col]:
        if not isinstance(val, str):
            continue
            
        diem_thi = val
        
        toan = get_score(diem_thi, "Toán:")
        van = get_score(diem_thi, "Ngữ văn:")
        ly = get_score(diem_thi, "Vật lí:")
        hoa = get_score(diem_thi, "Hóa học:")
        sinh = get_score(diem_thi, "Sinh học:")
        su = get_score(diem_thi, "Lịch sử:")
        dia = get_score(diem_thi, "Địa lí:")
        gdktpl = get_score(diem_thi, "KTPL:") or get_score(diem_thi, "Giáo dục công dân:")
        tin = get_score(diem_thi, "TI:") or get_score(diem_thi, "Tin học:")
        cong_nghe = get_score(diem_thi, "CNCN:") or get_score(diem_thi, "CNNN:") or get_score(diem_thi, "Công nghệ:")
        
        # Lấy điểm Ngoại ngữ thực tế từ dữ liệu
        anh = get_score(diem_thi, "Tiếng Anh:")
        phap = get_score(diem_thi, "Tiếng Pháp:")
        trung = get_score(diem_thi, "Tiếng Trung:")
        nhat = get_score(diem_thi, "Tiếng Nhật:")
        duc = get_score(diem_thi, "Tiếng Đức:")
        nga = get_score(diem_thi, "Tiếng Nga:")
        han = get_score(diem_thi, "Tiếng Hàn:")
        
        # Định dạng kỳ thi tốt nghiệp 2026: Bắt buộc Toán + Ngữ văn, và chọn 2 môn tự chọn
        if toan is None or van is None:
            continue
            
        electives_list = [
            "Vật lí", "Hóa học", "Sinh học", "Lịch sử", "Địa lí", "Giáo dục kinh tế và pháp luật", 
            "Tin học", "Công nghệ",
            "Tiếng Anh", "Tiếng Pháp", "Tiếng Trung", "Tiếng Nhật", "Tiếng Đức", "Tiếng Nga", "Tiếng Hàn"
        ]
        
        subject_scores = {
            "Toán": toan,
            "Ngữ văn": van,
            "Vật lí": ly,
            "Hóa học": hoa,
            "Sinh học": sinh,
            "Lịch sử": su,
            "Địa lí": dia,
            "Giáo dục kinh tế và pháp luật": gdktpl,
            "Tin học": tin,
            "Công nghệ": cong_nghe,
            "Tiếng Anh": anh,
            "Tiếng Pháp": phap,
            "Tiếng Trung": trung,
            "Tiếng Nhật": nhat,
            "Tiếng Đức": duc,
            "Tiếng Nga": nga,
            "Tiếng Hàn": han
        }
        
        # Lọc các môn tự chọn mà thí sinh có điểm
        active_electives = [e for e in electives_list if subject_scores[e] is not None]
        
        # Phải thi tối thiểu 2 môn tự chọn
        if len(active_electives) < 2:
            continue
            
        max_exam = 0.0
        valid = False
        
        # Xét tất cả các cặp 2 môn tự chọn (để mô phỏng tối ưu hóa việc chọn 2 môn tự chọn của thí sinh)
        for i in range(len(active_electives)):
            for j in range(i + 1, len(active_electives)):
                e1 = active_electives[i]
                e2 = active_electives[j]
                
                allowed_subjects = {"Toán", "Ngữ văn", e1, e2}
                
                # Tìm điểm cao nhất trong các tổ hợp xét tuyển hợp lệ được tạo từ 4 môn này
                for comb in combinations_list:
                    # Kiểm tra xem tổ hợp xét tuyển 3 môn này có nằm trong 4 môn thi hay không
                    is_valid_comb = True
                    for s in comb:
                        if s not in allowed_subjects:
                            is_valid_comb = False
                            break
                    
                    if is_valid_comb:
                        score_sum = subject_scores[comb[0]] + subject_scores[comb[1]] + subject_scores[comb[2]]
                        max_exam = max(max_exam, score_sum)
                        valid = True
                        
        if valid:
            # Tính điểm thuần không cần xét học bạ
            final_score = max_exam
            scores.append(final_score)
            
    # 3. Sort lại mảng để chuẩn bị Binary Search O(log N)
    scores.sort()
    total_valid = len(scores)
    print(f"Đã load và xử lý xong {total_valid} thí sinh có tổ hợp hợp lệ.")
    
    # 4. Vòng lặp Query
    while True:
        try:
            query_str = input("\nNhập điểm xét tuyển (hoặc gõ 'exit' để thoát): ")
            if query_str.lower() in ('exit', 'quit'):
                break
            
            target = float(query_str)
            
            # Tìm vị trí index lớn hơn target bằng thuật toán tìm kiếm nhị phân
            idx = bisect_right(scores, target)
            count = total_valid - idx
            
            print(f"-> Có {count} thí sinh đạt điểm xét tuyển cao hơn {target}.")
            
        except ValueError:
            print("Lỗi: Vui lòng nhập một con số hợp lệ.")
        except (EOFError, KeyboardInterrupt):
            print("\nĐã thoát chương trình.")
            break

if __name__ == '__main__':
    solve()