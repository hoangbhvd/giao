import streamlit as st
import pandas as pd
import random

# Tối ưu giao diện trực quan
st.set_page_config(page_title="Trắc nghiệm Lòng Yêu Nước", page_icon="🎯", layout="centered")

# 1. Đọc dữ liệu từ file Excel và đánh dấu số câu gốc
@st.cache_data
def load_data():
    try:
        df = pd.read_excel('ngan_hang_cau_hoi_hoan_thinh.xlsx') 
        records = df.to_dict('records')
        
        # Thêm một trường 'index_goc' vào từng câu hỏi (bắt đầu từ 1)
        for i, record in enumerate(records):
            record['index_goc'] = i + 1  # Câu 1, Câu 2 trong Excel...
            
        return records
    except Exception as e:
        st.error(f"Không thể đọc file Excel. Lỗi: {e}")
        return []

data = load_data()

# Hàm xử lý khi bấm nút "Nộp bài"
def submit_answer():
    st.session_state.answered = True

# Hàm xử lý khi bấm nút "Câu tiếp theo"
def next_question():
    st.session_state.current_index += 1
    st.session_state.answered = False

# Hàm xử lý khi bấm "Làm lại từ đầu"
def reset_quiz():
    shuffled = data.copy()
    # random.shuffle(shuffled)
    st.session_state.shuffled_questions = shuffled
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    for key in list(st.session_state.keys()):
        if key.startswith("scored_"):
            del st.session_state[key]

# 2. Khởi tạo bộ nhớ tạm ban đầu nếu chưa có
if 'shuffled_questions' not in st.session_state and len(data) > 0:
    reset_quiz()

# --- GIAO DIỆN CHÍNH ---
st.title("🎯 Ứng Dụng Trắc Nghiệm Lòng Yêu Nước")

if len(data) == 0:
    st.warning("Dữ liệu câu hỏi trống. Vui lòng kiểm tra lại file Excel.")
else:
    questions = st.session_state.shuffled_questions
    current_idx = st.session_state.current_index

    if current_idx < len(questions):
        item = questions[current_idx]
        
        # HIỂN THỊ CẢ LƯỢT CHƠI VÀ SỐ CÂU THỰC TẾ TRONG FILE EXCEL
        # Ví dụ: Lượt làm câu: 1/50 | (Câu gốc trong file Excel: Số 42)
        st.write(f"### 📝 Câu hỏi: {current_idx + 1} / {len(questions)}")
        st.caption(f"🔍 **Câu hỏi gốc: Số {item['index_goc']}**")
        
        # Phần hiển thị nội dung câu hỏi
        st.info(item['Câu hỏi'])
        
        # Làm sạch khoảng trắng dữ liệu đầu vào từ Excel
        opt_A = str(item['A']).strip()
        opt_B = str(item['B']).strip()
        opt_C = str(item['C']).strip()
        opt_D = str(item['D']).strip()
        options = [opt_A, opt_B, opt_C, opt_D]
        
        # Lựa chọn đáp án
        choice = st.radio("Chọn câu trả lời của bạn:", options, key=f"radio_{current_idx}", disabled=st.session_state.answered)
        
        st.write("---")
        
        # Khu vực nút điều hướng xử lý an toàn qua callback (on_click)
        if not st.session_state.answered:
            st.button("Nộp bài 📝", on_click=submit_answer, type="primary")
        else:
            # Xử lý tính điểm thông minh
            correct_ans_raw = str(item['Đáp án đúng']).strip()
            if correct_ans_raw.upper() == 'A': correct_val = opt_A
            elif correct_ans_raw.upper() == 'B': correct_val = opt_B
            elif correct_ans_raw.upper() == 'C': correct_val = opt_C
            elif correct_ans_raw.upper() == 'D': correct_val = opt_D
            else: correct_val = correct_ans_raw

            # Hiển thị kết quả đúng/sai trực quan
            if str(choice).strip() == correct_val:
                st.success("Chính xác! 🎉")
                if f"scored_{current_idx}" not in st.session_state:
                    st.session_state.score += 1
                    st.session_state[f"scored_{current_idx}"] = True
            else:
                st.error(f"Sai rồi! Đáp án đúng phải là: **{correct_val}**")
                
            st.button("Câu tiếp theo ➡️", on_click=next_question)
                    
    else:
        st.balloons()
        st.write("## 🎉 Bạn đã hoàn thành tất cả các câu hỏi!")
        st.metric(label="Số điểm đạt được", value=f"{st.session_state.score} / {len(questions)}")
        st.button("🔄 Làm lại từ đầu (Trộn lượt mới)", on_click=reset_quiz)