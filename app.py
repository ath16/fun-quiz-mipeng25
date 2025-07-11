import streamlit as st
import json
import time

def run():
    st.set_page_config(
        page_title="Fun Quiz MIPENG 2025",
        page_icon="logo-mipeng25.png",
    )
if __name__ == "__main__":
    run()

st.markdown("""
<style>
div.stButton > button:first-child {
    display: block;
    margin: 0 auto;
    height: 4em; /* Menambah tinggi tombol */
}
</style>
""", unsafe_allow_html=True)

st.session_state.setdefault('page', 'start')
st.session_state.setdefault('current_index', 0)
st.session_state.setdefault('answer_submitted', False)

try:
    with open('quiz_data.json', 'r', encoding='utf-8') as f:
        quiz_data = json.load(f)
except FileNotFoundError:
    st.error("File 'quiz_data.json' tidak ditemukan. Pastikan file ada di folder yang sama.")
    st.stop()
except json.JSONDecodeError:
    st.error("Format file 'quiz_data.json' salah. Mohon periksa kembali.")
    st.stop()

def go_to_start():
    st.session_state.page = 'start'
    st.session_state.current_index = 0
    st.session_state.answer_submitted = False

def start_quiz():
    st.session_state.page = 'quiz'

def check_answer(user_answer, correct_answer):
    if user_answer == correct_answer:
        st.session_state.answer_submitted = True
    else:
        st.error("Yah, jawabanmu kurang tepat. Coba lagi ya!", icon="❌")
        time.sleep(1)

def next_question():
    if st.session_state.current_index < len(quiz_data) - 1:
        st.session_state.current_index += 1
        st.session_state.answer_submitted = False
    else:
        st.session_state.page = 'end'

if st.session_state.page == 'start':
    st.title("Fun Quiz - Kloter 3 - MIPENG 2025")
    st.header("Sudah siap?")
    st.button("Mulai Kuis", on_click=start_quiz, use_container_width=True)

elif st.session_state.page == 'quiz':
    question_item = quiz_data[st.session_state.current_index]
    st.subheader(f"{question_item['question']}")
    st.markdown("""___""")

    options = question_item['options']
    correct_answer = question_item['answer']

    if not st.session_state.answer_submitted:
        row1_cols = st.columns(2)
        row2_cols = st.columns(2)
        all_cols = row1_cols + row2_cols
        for i, option in enumerate(options):
            with all_cols[i]:
                st.button(
                    option, 
                    key=f"q{st.session_state.current_index}_opt{i}", 
                    on_click=check_answer, 
                    args=(option, correct_answer),
                    use_container_width=True
                )
    else:
        st.balloons()
        st.success("Benar Sekali! Jawabanmu Tepat!", icon="✅")
        st.success(f"Jawaban yang benar adalah: **{correct_answer}**")
        st.button("Lanjut", on_click=next_question, use_container_width=True)

elif st.session_state.page == 'end':
    st.title("Kuis Selesai!")
    st.balloons()
    st.success(f"Selamat! Kamu berhasil menyelesaikan semua soal!", icon="🎉")
    st.button('Selesai', on_click=go_to_start, use_container_width=True)
