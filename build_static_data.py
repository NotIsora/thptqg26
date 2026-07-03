import os
import sys
import math
import json
import pandas as pd

# Đảm bảo in tiếng Việt không bị lỗi encoding trên Windows console
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Cấu hình danh sách tổ hợp
combinations_dict = {
    # Khối A
    "A00": ("Toán", "Vật lí", "Hóa học"),
    "A01": ("Toán", "Vật lí", "Tiếng Anh"),
    "A02": ("Toán", "Vật lí", "Sinh học"),
    "A03": ("Toán", "Vật lí", "Lịch sử"),
    "A04": ("Toán", "Vật lí", "Địa lí"),
    "A05": ("Toán", "Hóa học", "Lịch sử"),
    "A06": ("Toán", "Hóa học", "Địa lí"),
    "A07": ("Toán", "Lịch sử", "Địa lí"),
    "A08": ("Toán", "Lịch sử", "Giáo dục kinh tế và pháp luật"),
    "A09": ("Toán", "Địa lí", "Giáo dục kinh tế và pháp luật"),
    "A10": ("Toán", "Vật lí", "Giáo dục kinh tế và pháp luật"),
    "A11": ("Toán", "Hóa học", "Giáo dục kinh tế và pháp luật"),

    # Khối B
    "B00": ("Toán", "Hóa học", "Sinh học"),
    "B02": ("Toán", "Sinh học", "Địa lí"),
    "B03": ("Toán", "Sinh học", "Ngữ văn"),
    "B04": ("Toán", "Sinh học", "Giáo dục kinh tế và pháp luật"),
    "B08": ("Toán", "Sinh học", "Tiếng Anh"),

    # Khối C
    "C00": ("Ngữ văn", "Lịch sử", "Địa lí"),
    "C01": ("Ngữ văn", "Toán", "Vật lí"),
    "C02": ("Ngữ văn", "Toán", "Hóa học"),
    "C03": ("Ngữ văn", "Toán", "Lịch sử"),
    "C04": ("Ngữ văn", "Toán", "Địa lí"),
    "C05": ("Ngữ văn", "Vật lí", "Hóa học"),
    "C06": ("Ngữ văn", "Vật lí", "Sinh học"),
    "C08": ("Ngữ văn", "Hóa học", "Sinh học"),
    "C12": ("Ngữ văn", "Lịch sử", "Sinh học"),
    "C13": ("Ngữ văn", "Sinh học", "Địa lí"),
    "C14": ("Ngữ văn", "Toán", "Giáo dục kinh tế và pháp luật"),
    "C17": ("Ngữ văn", "Hóa học", "Giáo dục kinh tế và pháp luật"),
    "C19": ("Ngữ văn", "Lịch sử", "Giáo dục kinh tế và pháp luật"),
    "C20": ("Ngữ văn", "Địa lí", "Giáo dục kinh tế và pháp luật"),

    # Khối D
    "D01": ("Ngữ văn", "Toán", "Tiếng Anh"),
    "D02": ("Ngữ văn", "Toán", "Tiếng Nga"),
    "D03": ("Ngữ văn", "Toán", "Tiếng Pháp"),
    "D04": ("Ngữ văn", "Toán", "Tiếng Trung"),
    "D05": ("Ngữ văn", "Toán", "Tiếng Đức"),
    "D06": ("Ngữ văn", "Toán", "Tiếng Nhật"),
    "D07": ("Toán", "Hóa học", "Tiếng Anh"),
    "D08": ("Toán", "Sinh học", "Tiếng Anh"),
    "D09": ("Toán", "Lịch sử", "Tiếng Anh"),
    "D10": ("Toán", "Địa lí", "Tiếng Anh"),
    "D11": ("Ngữ văn", "Vật lí", "Tiếng Anh"),
    "D12": ("Ngữ văn", "Hóa học", "Tiếng Anh"),
    "D13": ("Ngữ văn", "Sinh học", "Tiếng Anh"),
    "D14": ("Ngữ văn", "Lịch sử", "Tiếng Anh"),
    "D15": ("Ngữ văn", "Địa lí", "Tiếng Anh"),
    "D66": ("Ngữ văn", "Giáo dục kinh tế và pháp luật", "Tiếng Anh"),
    "D68": ("Ngữ văn", "Giáo dục kinh tế và pháp luật", "Tiếng Nga"),
    "D70": ("Ngữ văn", "Giáo dục kinh tế và pháp luật", "Tiếng Pháp"),
    "D71": ("Ngữ văn", "Giáo dục kinh tế và pháp luật", "Tiếng Trung"),
    "D84": ("Toán", "Tiếng Anh", "Giáo dục kinh tế và pháp luật"),

    # Khối môn mới Tin học & Công nghệ
    "Toán-Tin-Anh": ("Toán", "Tin học", "Tiếng Anh"),
    "Toán-Tin-Lý": ("Toán", "Tin học", "Vật lí"),
    "Toán-Tin-Hóa": ("Toán", "Tin học", "Hóa học"),
    "Toán-Tin-Sinh": ("Toán", "Tin học", "Sinh học"),
    "Toán-CN-Anh": ("Toán", "Công nghệ", "Tiếng Anh"),
    "Toán-CN-Lý": ("Toán", "Công nghệ", "Vật lí"),
    "Toán-CN-Hóa": ("Toán", "Công nghệ", "Hóa học"),
    "Toán-CN-Sinh": ("Toán", "Công nghệ", "Sinh học"),
}

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

def build():
    file_path = 'diem_thi_hcm.xlsx'
    if not os.path.exists(file_path):
        print(f"Lỗi: Không tìm thấy file {file_path}")
        return

    print("Đang đọc dữ liệu từ file Excel (diem_thi_hcm.xlsx)...")
    df = pd.read_excel(file_path)
    
    # Tìm cột điểm thi
    diem_thi_col = None
    for col in df.columns:
        sample = df[col].dropna().head(10)
        if any(isinstance(val, str) and 'Toán:' in val for val in sample):
            diem_thi_col = col
            break
    if not diem_thi_col:
        diem_thi_col = df.columns[2] if len(df.columns) >= 3 else df.columns[-1]

    print(f"-> Bắt đầu xử lý cột '{diem_thi_col}'...")
    
    # Lưu danh sách điểm của từng tổ hợp
    combination_scores = {k: [] for k in combinations_dict}

    for val in df[diem_thi_col]:
        if not isinstance(val, str):
            continue
            
        toan = get_score(val, "Toán:")
        van = get_score(val, "Ngữ văn:")
        if toan is None or van is None:
            continue
            
        ly = get_score(val, "Vật lí:")
        hoa = get_score(val, "Hóa học:")
        sinh = get_score(val, "Sinh học:")
        su = get_score(val, "Lịch sử:")
        dia = get_score(val, "Địa lí:")
        gdcd = get_score(val, "Giáo dục công dân:")
        tin = get_score(val, "Tin học:")
        cong_nghe = get_score(val, "Công nghệ:")
        
        anh = get_score(val, "Tiếng Anh:")
        phap = get_score(val, "Tiếng Pháp:")
        trung = get_score(val, "Tiếng Trung:")
        nhat = get_score(val, "Tiếng Nhật:")
        duc = get_score(val, "Tiếng Đức:")
        nga = get_score(val, "Tiếng Nga:")
        han = get_score(val, "Tiếng Hàn:")

        subject_scores = {
            "Toán": toan,
            "Ngữ văn": van,
            "Vật lí": ly,
            "Hóa học": hoa,
            "Sinh học": sinh,
            "Lịch sử": su,
            "Địa lí": dia,
            "Giáo dục kinh tế và pháp luật": gdcd,
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

        electives_list = [
            "Vật lí", "Hóa học", "Sinh học", "Lịch sử", "Địa lí", "Giáo dục kinh tế và pháp luật", 
            "Tin học", "Công nghệ",
            "Tiếng Anh", "Tiếng Pháp", "Tiếng Trung", "Tiếng Nhật", "Tiếng Đức", "Tiếng Nga", "Tiếng Hàn"
        ]
        active_electives = [e for e in electives_list if subject_scores[e] is not None]
        if len(active_electives) < 2:
            continue

        for name, subjects in combinations_dict.items():
            s1, s2, s3 = subjects
            val1 = subject_scores.get(s1)
            val2 = subject_scores.get(s2)
            val3 = subject_scores.get(s3)

            if val1 is not None and val2 is not None and val3 is not None:
                score = round(val1 + val2 + val3, 2)
                combination_scores[name].append(score)

    # Gom nhóm theo tần suất và sắp xếp
    static_data = {}
    for name in combination_scores:
        scores = combination_scores[name]
        freq = {}
        for s in scores:
            freq[s] = freq.get(s, 0) + 1
        
        # Chuyển thành danh sách các cặp [điểm, số lượng] sắp xếp tăng dần theo điểm
        sorted_freq = [[round(k, 2), v] for k, v in sorted(freq.items())]
        
        static_data[name] = {
            "subjects": ", ".join(combinations_dict[name]),
            "data": sorted_freq
        }

    # Xuất ra file JS
    js_content = f"const COMBINATION_DATA = {json.dumps(static_data, ensure_ascii=False)};"
    with open("data.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print("-> Đã xuất dữ liệu tĩnh ra file 'data.js' thành công!")

if __name__ == '__main__':
    build()
