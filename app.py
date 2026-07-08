import streamlit as st
import pandas as pd
import random

# 1. Đọc dữ liệu từ file Excel (thay tên file của bạn vào đây)
@st.cache_data
def load_data():
    # Giả sử file của bạn có cột 'Câu hỏi', 'A', 'B', 'C', 'D', 'Đáp án đúng'
    df = pd.read_excel('ngan_hang_cau_hoi_hoan_thinh.xlsx') 
    return df.to_dict('records')

data = load_data()

# 2. Xáo trộn câu hỏi và lưu vào session_state để cố định vị trí trong suốt lượt chơi
if 'shuffled_questions' not in st.session_state:
    # Copy danh sách câu hỏi gốc ra một danh sách mới
    shuffled = data.copy()
    # Trộn ngẫu nhiên danh sách này
    random.shuffle(shuffled)
    # Lưu vào bộ nhớ tạm của Streamlit
    st.session_state.shuffled_questions = shuffled
    st.session_state.current_index = 0  # Chỉ số câu hỏi hiện tại
    st.session_state.score = 0          # Điểm số ban đầu

# 3. Lấy danh sách câu hỏi đã được trộn ra để sử dụng
questions = st.session_state.shuffled_questions
current_idx = st.session_state.current_index

# --- Phần hiển thị giao diện trắc nghiệm ---
if current_idx < len(questions):
    item = questions[current_idx]
    
    st.write(f"### Câu hỏi {current_idx + 1}: {item['Câu hỏi']}")
    
    # Tạo danh sách các lựa chọn
    options = [item['A'], item['B'], item['C'], item['D']]
    
    # Hiển thị các nút bấm chọn đáp án
    choice = st.radio("Chọn câu trả lời đúng:", options, key=f"q_{current_idx}")
    
    if st.button("Nộp bài"):
        if choice == item['Đáp án đúng']:
            st.success("Chính xác! 🎉")
            st.session_state.score += 1
        else:
            st.error(f"Sai rồi! Đáp án đúng là: {item['Đáp án đúng']}")
            
        # Bấm để qua câu tiếp theo
        if st.button("Câu tiếp theo"):
            st.session_state.current_index += 1
            st.rerun()
else:
    st.write("## Chúc mừng bạn đã hoàn thành bài trắc nghiệm! 🎉")
    st.write(f"Số điểm của bạn là: **{st.session_state.score} / {len(questions)}**")
    
    if st.button("Làm lại từ đầu (Trộn lượt mới)"):
        # Xóa bộ nhớ tạm để lượt sau tự động trộn lại theo thứ tự khác
        del st.session_state.shuffled_questions
        st.rerun()