import re
import pandas as pd

# 1. Đọc nội dung từ file .txt
txt_path = "cau_hoi.txt"

with open(txt_path, "r", encoding="utf-8") as f:
    full_text = f.read()

# 2. Dùng Regex để tách từng câu hỏi
# Regex này nhận diện chữ "Câu" theo sau là khoảng trắng, các chữ số, và có thể có dấu hoặc không (dấu :, dấu . hoặc khoảng trắng)
questions_raw = re.split(r'(?=Câu\s+\d+[:\.\s])', full_text)

data = []
stt = 1

for q_block in questions_raw:
    if not q_block.strip():
        continue
    
    # Chuyển đổi khối văn bản thành một chuỗi duy nhất trên một dòng để dễ quét đáp án
    # (Tránh trường hợp đáp án A, B, C, D bị xuống dòng làm sót dữ liệu)
    single_line_text = " ".join([line.strip() for line in q_block.split('\n') if line.strip()])
    
    # Tách phần câu hỏi gốc (nội dung trước chữ A.)
    match_q = re.search(r'(.*?)(?=A\.)', single_line_text)
    if not match_q:
        continue  # Nếu câu không có đáp án A. thì bỏ qua vì không phải câu hỏi trắc nghiệm hợp lệ
        
    raw_question = match_q.group(1).strip()
    
    # Làm sạch tiêu đề câu hỏi: bỏ chữ "Câu X:" hoặc "Câu X " ở đầu câu
    clean_question = re.sub(r'^Câu\s+\d+[:\.\s]*', '', raw_question).strip()
    
    # Quét chính xác nội dung của các lựa chọn A, B, C, D
    match_a = re.search(r'A\.\s*(.*?)(?=B\.)', single_line_text)
    match_b = re.search(r'B\.\s*(.*?)(?=C\.)', single_line_text)
    match_c = re.search(r'C\.\s*(.*?)(?=D\.)', single_line_text)
    match_d = re.search(r'D\.\s*(.*)', single_line_text)
    
    ans_a = match_a.group(1).strip() if match_a else ""
    ans_b = match_b.group(1).strip() if match_b else ""
    ans_c = match_c.group(1).strip() if match_c else ""
    ans_d = match_d.group(1).strip() if match_d else ""
    
    # Thêm vào danh sách dữ liệu
    data.append({
        "STT": stt,
        "Câu hỏi": clean_question,
        "A": ans_a,
        "B": ans_b,
        "C": ans_c,
        "D": ans_d,
        "Đáp án đúng": ""  # Để trống để bạn điền sau
    })
    stt += 1

# 3. Xuất dữ liệu ra file Excel
df = pd.DataFrame(data)
df.to_excel("ngan_hang_cau_hoi_chuyen_doi.xlsx", index=False)

print(f"Xử lý thành công! Đã trích xuất được {len(data)} câu hỏi vào file 'ngan_hang_cau_hoi_chuyen_doi.xlsx'.")