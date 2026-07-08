import streamlit as st
import pandas as pd
import random

# 1. Đọc dữ liệu từ file Excel
@st.cache_data
def load_data():
    df = pd.read_excel('ngan_hang_cau_hoi_hoan_thinh.xlsx') 
    return df.to_dict('records')

data = load_data()

# 2. Khởi tạo bộ nhớ tạm
if 'shuffled_questions' not in st.session_state:
    shuffled = data.copy()
    random.shuffle(shuffled)
    st.session_state.shuffled_questions = shuffled
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.answered = False

questions = st.session_state.shuffled_questions
current_idx = st.session_state.current_index

st.title("🎯 Trắc Nghiệm Yêu Nước")

if current_idx < len(questions):
    item = questions[current_idx]
    
    st.write(f"### Câu hỏi {current_idx + 1} / {len(questions)}")
    st.info(item['Câu hỏi'])
    
    # Ép kiểu dữ liệu về chuỗi (string) và xóa khoảng trắng thừa ở hai đầu bằng lệnh strip()
    opt_A = str(item['A']).strip()
    opt_B = str(item['B']).strip()
    opt_C = str(item['C']).strip()
    opt_D = str(item['D']).strip()
    
    options = [opt_A, opt_B, opt_C, opt_D]
    
    choice = st.radio("Chọn câu trả lời của bạn:", options, key=f"radio_{current_idx}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        submit_button = st.button("Nộp bài", disabled=st.session_state.answered)
        if submit_button:
            st.session_state.answered = True
            st.rerun()

    if st.session_state.answered:
        # Lấy đáp án trong Excel và làm sạch khoảng trắng
        correct_ans_raw = str(item['Đáp án đúng']).strip()
        
        # LOGIC THÔNG MINH: Nếu trong Excel cột đáp án chỉ ghi A, B, C, D
        if correct_ans_raw.upper() == 'A':
            correct_val = opt_A
        elif correct_ans_raw.upper() == 'B':
            correct_val = opt_B
        elif correct_ans_raw.upper() == 'C':
            correct_val = opt_C
        elif correct_ans_raw.upper() == 'D':
            correct_val = opt_D
        else:
            # Nếu cột đáp án ghi đầy đủ nội dung
            correct_val = correct_ans_raw

        # So sánh lựa chọn của người dùng với đáp án chuẩn
        if str(choice).strip() == correct_val:
            st.success("Chính xác! 🎉 Tổng điểm đã được cộng.")
            if f"scored_{current_idx}" not in st.session_state:
                st.session_state.score += 1
                st.session_state[f"scored_{current_idx}"] = True
        else:
            st.error(f"Sai rồi! Đáp án đúng phải là: {correct_val}")
            
        with col2:
            if st.button("Câu tiếp theo ➡️"):
                st.session_state.current_index += 1
                st.session_state.answered = False
                st.rerun()
                
else:
    st.balloons()
    st.write("## 🎉 Bạn đã hoàn thành tất cả các câu hỏi!")
    st.metric(label="Số điểm đạt được", value=f"{st.session_state.score} / {len(questions)}")
    
    if st.button("🔄 Làm lại từ đầu (Trộn lượt mới)"):
        del st.session_state.shuffled_questions
        if 'current_index' in st.session_state: del st.session_state.current_index
        if 'score' in st.session_state: del st.session_state.score
        if 'answered' in st.session_state: del st.session_state.answered
        st.rerun()