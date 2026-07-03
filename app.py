import os
import sys
import math
from flask import Flask, jsonify, request, render_template
import pandas as pd
from bisect import bisect_right

# Đảm bảo in tiếng Việt không bị lỗi encoding trên Windows console
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

app = Flask(__name__, template_folder='templates')

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

# Lưu trữ điểm của từng tổ hợp
combination_scores = {k: [] for k in combinations_dict}
is_loaded = False

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

def load_data():
    global is_loaded
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
    
    for val in df[diem_thi_col]:
        if not isinstance(val, str):
            continue
            
        toan = get_score(val, "Toán:")
        van = get_score(val, "Ngữ văn:")
        
        # Kỳ thi tốt nghiệp 2026: Bắt buộc Toán và Văn
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
        
        # Lấy điểm Ngoại ngữ thực tế từ dữ liệu
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

        # Kiểm tra điều kiện tối thiểu 2 môn tự chọn
        electives_list = [
            "Vật lí", "Hóa học", "Sinh học", "Lịch sử", "Địa lí", "Giáo dục kinh tế và pháp luật", 
            "Tin học", "Công nghệ",
            "Tiếng Anh", "Tiếng Pháp", "Tiếng Trung", "Tiếng Nhật", "Tiếng Đức", "Tiếng Nga", "Tiếng Hàn"
        ]
        active_electives = [e for e in electives_list if subject_scores[e] is not None]
        if len(active_electives) < 2:
            continue

        # Phân nhóm điểm vào từng tổ hợp
        for name, subjects in combinations_dict.items():
            s1, s2, s3 = subjects
            val1 = subject_scores.get(s1)
            val2 = subject_scores.get(s2)
            val3 = subject_scores.get(s3)

            if val1 is not None and val2 is not None and val3 is not None:
                # Tính điểm thuần không cần xét học bạ (tổng điểm 3 môn)
                score = round(val1 + val2 + val3, 4)
                combination_scores[name].append(score)

    # Sắp xếp các mảng điểm để phục vụ Binary Search
    for name in combination_scores:
        combination_scores[name].sort()

    is_loaded = True
    print("-> Đã tải và xử lý dữ liệu xong! Sẵn sàng phục vụ.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/combinations', methods=['GET'])
def get_combinations():
    return jsonify({
        "combinations": [
            {"code": k, "subjects": ", ".join(v)} for k, v in combinations_dict.items()
        ]
    })

@app.route('/api/compare', methods=['POST'])
def compare():
    if not is_loaded:
        return jsonify({"error": "Dữ liệu đang được tải, vui lòng quay lại sau ít giây."}), 503

    data = request.get_json() or {}
    try:
        user_score = float(data.get("score", 0))
    except ValueError:
        return jsonify({"error": "Điểm số không hợp lệ."}), 400

    selected_combs = data.get("combinations", [])
    if not selected_combs:
        return jsonify({"error": "Vui lòng chọn ít nhất một tổ hợp để so sánh."}), 400

    results = {}
    for code in selected_combs:
        if code not in combination_scores:
            continue
            
        scores = combination_scores[code]
        N = len(scores)
        if N == 0:
            results[code] = {
                "total": 0,
                "rank": 0,
                "better_count": 0,
                "percentile": 0.0,
                "avg": 0.0,
                "median": 0.0,
                "max": 0.0,
                "min": 0.0,
                "subjects": ", ".join(combinations_dict[code])
            }
            continue

        # Tìm vị trí thí sinh có điểm cao hơn user_score
        idx = bisect_right(scores, user_score)
        better_count = N - idx
        rank = better_count + 1
        percentile = round(((N - better_count) / N) * 100, 2)
        
        # Thống kê
        avg = round(sum(scores) / N, 2)
        median = round(scores[N // 2], 2)
        max_val = round(scores[-1], 2)
        min_val = round(scores[0], 2)

        results[code] = {
            "total": N,
            "rank": rank,
            "better_count": better_count,
            "percentile": percentile,
            "avg": avg,
            "median": median,
            "max": max_val,
            "min": min_val,
            "subjects": ", ".join(combinations_dict[code])
        }

    return jsonify({"score": user_score, "results": results})

if __name__ == '__main__':
    # Chạy load data trước khi khởi động server
    load_data()
    # Tắt use_reloader để tránh lỗi Errno 2 trên Windows environment
    app.run(debug=True, use_reloader=False, port=5000)
