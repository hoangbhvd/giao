import streamlit as st
import pandas as pd

# Tối ưu giao diện trực quan
st.set_page_config(page_title="Trắc nghiệm Lòng Yêu Nước", page_icon="🎯", layout="centered")

# 1. Đọc dữ liệu từ file Excel và đánh dấu số câu gốc
@st.cache_data
def load_data():
    try:
        df = pd.read_excel('ngan_hang_cau_hoi_hoan_thinh.xlsx') 
        records = df.to_dict('records')
        
        # Giữ số thứ tự dòng gốc (bắt đầu từ 1)
        for i, record in enumerate(records):
            record['index_goc'] = i + 1  
            
        return records
    except Exception as e:
        st.error(f"Không thể đọc file Excel. Lỗi: {e}")
        return []

data = load_data()

# Hàm xử lý khi bấm nút "Nộp bài"
def submit_answer():
    current_idx = st.session_state.current_index
    # Đánh dấu câu này đã được trả lời
    st.session_state.answered_status[current_idx] = True

# Hàm xử lý khi bấm nút "Câu tiếp theo"
def next_question():
    st.session_state.current_index += 1

# Hàm xử lý khi bấm nút "Câu trước"
def prev_question():
    if st.session_state.current_index > 0:
        st.session_state.current_index -= 1

# Hàm xử lý khi bấm "Làm lại từ đầu"
def reset_quiz():
    st.session_state.shuffled_questions = data.copy()
    st.session_state.current_index = 0
    st.session_state.score = 0
    # Lưu trạng thái đã nộp bài của từng câu (Ví dụ câu 0: True/False)
    st.session_state.answered_status = {i: False for i in range(len(data))}
    # Lưu điểm số thực tế đã tính của từng câu để không bị cộng dồn khi bấm qua lại
    st.session_state.scored_status = {i: False for i in range(len(data))}

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
        
        # Kiểm tra xem câu hiện tại đã bấm nộp bài trước đó chưa
        is_current_answered = st.session_state.answered_status.get(current_idx, False)
        
        # Hiển thị tiến trình làm bài theo thứ tự chuẩn
        st.write(f"### 📝 Câu hỏi: {current_idx + 1} / {len(questions)}")
        st.caption(f"🔍 **Vị trí câu trong dữ liệu: Số {item['index_goc']}**")
        
        # Phần hiển thị nội dung câu hỏi
        st.info(item['Câu hỏi'])
        
        # Làm sạch khoảng trắng dữ liệu đầu vào từ Excel
        opt_A = str(item['A']).strip()
        opt_B = str(item['B']).strip()
        opt_C = str(item['C']).strip()
        opt_D = str(item['D']).strip()
        options = [opt_A, opt_B, opt_C, opt_D]
        
        # Lựa chọn đáp án (Khóa không cho chọn lại nếu câu này đã bấm Nộp bài rồi)
        choice = st.radio("Chọn câu trả lời của bạn:", options, key=f"radio_{current_idx}", disabled=is_current_answered)
        
        st.write("---")
        
        # Chia layout nút bấm bên dưới câu hỏi
        col_prev, col_submit, col_next = st.columns([1, 1, 1])
        
        # Nút Quay lại câu trước (Luôn hiện nếu không phải câu đầu tiên)
        with col_prev:
            if current_idx > 0:
                st.button("⬅️ Câu trước", on_click=prev_question)
        
        # Nút Nộp bài (Chỉ hiện khi chưa trả lời câu này)
        with col_submit:
            if not is_current_answered:
                st.button("Nộp bài 📝", on_click=submit_answer, type="primary")
        
        # Xử lý kết quả và nút Tiếp theo khi đã bấm nộp bài
        if is_current_answered:
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
                if not st.session_state.scored_status[current_idx]:
                    st.session_state.score += 1
                    st.session_state.scored_status[current_idx] = True
            else:
                st.error(f"Sai rồi! Đáp án đúng phải là: **{correct_val}**")
                
            with col_next:
                st.button("Câu tiếp theo ➡️", on_click=next_question)
                    
    else:
        st.balloons()
        st.write("## 🎉 Bạn đã hoàn thành tất cả các câu hỏi!")
        st.metric(label="Số điểm đạt được", value=f"{st.session_state.score} / {len(questions)}")
        
        # Nút quay lại câu cuối cùng từ màn hình kết quả để xem lại bài
        if st.button("⬅️ Quay lại xem lại các câu hỏi"):
            st.session_state.current_index = len(questions) - 1
            st.import_util.rerun() if hasattr(st, "import_util") else st.rerun()
            
        st.button("🔄 Làm lại từ đầu (Theo thứ tự)", on_click=reset_quiz)