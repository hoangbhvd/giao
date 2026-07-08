import streamlit as st
import pandas as pd
import random

# 1. Đọc dữ liệu từ file Excel của bạn
@st.cache_data
def load_data():
    df = pd.read_excel('ngan_hang_cau_hoi_hoan_thinh.xlsx') 
    return df.to_dict('records')

data = load_data()

# 2. Khởi tạo các giá trị trong bộ nhớ tạm (Session State) nếu chưa có
if 'shuffled_questions' not in st.session_state:
    shuffled = data.copy()
    random.shuffle(shuffled)  # Trộn ngẫu nhiên câu hỏi
    st.session_state.shuffled_questions = shuffled
    st.session_state.current_index = 0  # Câu hỏi hiện tại
    st.session_state.score = 0          # Điểm số
    st.session_state.answered = False    # Trạng thái: Đã bấm "Nộp bài" hay chưa

questions = st.session_state.shuffled_questions
current_idx = st.session_state.current_index

# --- GIAO DIỆN CHÍNH ---
st.title("🎯 Ứng Dụng Trắc Nghiệm")

if current_idx < len(questions):
    item = questions[current_idx]
    
    st.write(f"### Câu hỏi {current_idx + 1} / {len(questions)}")
    st.info(item['Câu hỏi'])
    
    # Tạo danh sách các lựa chọn từ cột A, B, C, D trong file Excel
    options = [item['A'], item['B'], item['C'], item['D']]
    
    # Sử dụng key động dựa trên câu hỏi hiện tại để tránh xung đột dữ liệu giữa các câu
    choice = st.radio("Chọn câu trả lời của bạn:", options, key=f"radio_{current_idx}")
    
    # Tạo 2 cột để đặt nút bấm cho đẹp mắt
    col1, col2 = st.columns(2)
    
    with col1:
        # Nút "Nộp bài" chỉ bấm được khi chưa trả lời câu này
        submit_button = st.button("Nộp bài", disabled=st.session_state.answered)
        if submit_button:
            st.session_state.answered = True
            st.rerun()  # Chạy lại để cập nhật trạng thái hiển thị kết quả

    # Nếu đã bấm nộp bài, hiển thị kết quả đúng/sai ngay lập tức
    if st.session_state.answered:
        if choice == item['Đáp án đúng']:
            st.success("Chính xác! 🎉 Tổng điểm đã được cộng.")
            # Chỉ cộng điểm một lần duy nhất khi người dùng bấm nộp bài đúng
            if f"scored_{current_idx}" not in st.session_state:
                st.session_state.score += 1
                st.session_state[f"scored_{current_idx}"] = True
        else:
            st.error(f"Sai rồi! Đáp án đúng phải là: {item['Đáp án đúng']}")
            
        with col2:
            # Sau khi nộp bài xong thì hiện nút "Câu tiếp theo"
            if st.button("Câu tiếp theo ➡️"):
                st.session_state.current_index += 1  # Tăng chỉ số câu hỏi lên 1
                st.session_state.answered = False    # Reset trạng thái để câu sau trả lời tiếp
                st.rerun()  # Tải lại trang để nhảy sang câu mới
                
else:
    # Giao diện khi hoàn thành hết tất cả câu hỏi
    st.balloons()  # Hiệu ứng bóng bay chúc mừng
    st.write("## 🎉 Bạn đã hoàn thành tất cả các câu hỏi!")
    st.metric(label="Số điểm đạt được", value=f"{st.session_state.score} / {len(questions)}")
    
    if st.button("🔄 Làm lại từ đầu (Trộn lượt mới)"):
        # Xóa toàn bộ bộ nhớ tạm để hệ thống kích hoạt lượt trộn ngẫu nhiên mới
        del st.session_state.shuffled_questions
        if 'current_index' in st.session_state: del st.session_state.current_index
        if 'score' in st.session_state: del st.session_state.score
        if 'answered' in st.session_state: del st.session_state.answered
        st.rerun()