import streamlit as st
import pandas as pd

# Cấu hình trang web app
st.set_page_config(page_title="App Luyện Thi Trắc Nghiệm", page_icon="📝", layout="centered")

# 1. Đọc dữ liệu từ file Excel hoàn chỉnh của bạn
@st.cache_data # Dùng cache để app load mượt và nhanh hơn
def load_data():
    df = pd.read_excel("ngan_hang_cau_hoi_hoan_thinh.xlsx")
    # Đảm bảo các cột trống hoặc NaN không làm app bị lỗi
    df = df.fillna("")
    return df

df = load_data()
total_questions = len(df)

# Tiêu đề ứng dụng
st.title("📝 Ứng Dụng Luyện Tập Trắc Nghiệm")
st.write(f"Tổng số câu hỏi hiện có: **{total_questions}** câu.")

# 2. Quản lý trạng thái câu hỏi bằng Session State của Streamlit
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False

idx = st.session_state.current_index

# Giao diện hiển thị khi chưa hết câu hỏi
if idx < total_questions:
    row = df.iloc[idx]
    
    st.subheader(f"Câu hỏi {idx + 1}/{total_questions}:")
    st.info(row["Câu hỏi"])
    
    # Chuẩn bị danh sách lựa chọn
    options = []
    if row["A"]: options.append(f"A. {row['A']}")
    if row["B"]: options.append(f"B. {row['B']}")
    if row["C"]: options.append(f"C. {row['C']}")
    if row["D"]: options.append(f"D. {row['D']}")
    
    # Ô chọn đáp án
    user_choice = st.radio("Chọn đáp án của bạn:", options, key=f"q_{idx}", index=None)
    
    # Nút bấm nộp bài kiểm tra đáp án
    if st.button("Nộp câu trả lời", disabled=st.session_state.answered or user_choice is None):
        st.session_state.answered = True
        correct_ans_letter = str(row["Đáp án đúng"]).strip().upper()
        user_ans_letter = user_choice[0] # Lấy ký tự đầu (A, B, C, hoặc D)
        
        if user_ans_letter == correct_ans_letter:
            st.success("🎉 Chính xác!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Sai rồi! Đáp án đúng là: {correct_ans_letter}")
            
    # Nút bấm chuyển sang câu tiếp theo
    if st.session_state.answered:
        if st.button("Câu tiếp theo ➡️"):
            st.session_state.current_index += 1
            st.session_state.answered = False
            st.rerun()

# Giao diện hiển thị khi đã hoàn thành hết bộ câu hỏi
else:
    st.balloons()
    st.success(f"🏆 Bạn đã hoàn thành tất cả câu hỏi!")
    st.metric(label="Điểm số của bạn", value=f"{st.session_state.score} / {total_questions}")
    
    if st.button("Làm lại từ đầu 🔄"):
        st.session_state.current_index = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.rerun()