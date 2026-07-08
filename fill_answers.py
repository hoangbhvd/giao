import pandas as pd
import re

# 1. Đọc file Excel hiện tại
excel_path = "ngan_hang_cau_hoi_chuyen_doi.xlsx"
df = pd.read_excel(excel_path)

# 2. Đọc chuỗi đáp án từ file ans.txt
ans_path = "ans.txt"
with open(ans_path, "r", encoding="utf-8") as f:
    ans_content = f.read()

# Chỉ lọc lấy các ký tự chữ cái (A, B, C, D, E, v.v.)
answers = re.findall(r'[A-Za-z]', ans_content)

print(f"Tìm thấy {len(answers)} đáp án trong file ans.txt")
print(f"Số lượng câu hỏi trong file Excel hiện tại là: {len(df)} câu")

# --- BƯỚC SỬA LỖI: Ép kiểu cột "Đáp án đúng" thành chuỗi (String) ---
df["Đáp án đúng"] = df["Đáp án đúng"].astype(object)
# ------------------------------------------------------------------

# 3. Điền đáp án vào cột "Đáp án đúng" dựa theo thứ tự tương ứng
for i in range(len(df)):
    if i < len(answers):
        # Chuyển đáp án thành chữ in hoa cho đồng bộ
        df.at[i, "Đáp án đúng"] = str(answers[i]).upper()
    else:
        # Trường hợp file đáp án bị thiếu so với số câu hỏi trong Excel
        df.at[i, "Đáp án đúng"] = ""

# 4. Lưu thành file mới hoàn chỉnh
output_path = "ngan_hang_cau_hoi_hoan_thinh.xlsx"
df.to_excel(output_path, index=False)

print(f"Cập nhật hoàn tất! File đầy đủ câu hỏi và đáp án đã được lưu tại: '{output_path}'")