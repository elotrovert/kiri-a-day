import os
from pathlib import Path
from typing import Optional

import streamlit as st

from audio import play_wav_bytes_autoplay
from machi import MachiWeb


st.set_page_config(
    page_title="Kiri's Adoption Day",
    page_icon="🎈",
    layout="centered",
)


QUIZ_QUESTIONS = [
    {
        "image": "assets/quiz/q1-closeup.png",
        "question": "What are we celebrating today?",
        "options": [
            "Kiri's adoption day",
            "A random Tuesday",
            "National sock sorting day",
            "The invention of toast",
        ],
        "answer": "Kiri's adoption day",
        "info": "Correct. Today is all about celebrating the day Kiri became family.",
    },
    {
        "image": "assets/quiz/q2-closeup.png",
        "question": "What is the best way to mark Kiri's special day?",
        "options": [
            "Extra love and attention",
            "Ignoring her completely",
            "Doing taxes",
            "Cancelling all snacks",
        ],
        "answer": "Extra love and attention",
        "info": "Exactly. Adoption days deserve affection, fuss, and a proper little celebration.",
    },
    {
        "image": "assets/quiz/q3-closeup.png",
        "question": "What should Kiri receive for being wonderful?",
        "options": [
            "A treat",
            "A boring spreadsheet",
            "A stern email",
            "Nothing at all",
        ],
        "answer": "A treat",
        "info": "Yes. A treat is the official currency of being excellent.",
    },
    {
        "image": "assets/quiz/q4-closeup.png",
        "question": "What is Kiri's official adoption day status?",
        "options": [
            "Deeply loved",
            "Mildly tolerated",
            "Under review",
            "Pending paperwork",
        ],
        "answer": "Deeply loved",
        "info": "Correct. Deeply loved, today and every day.",
    },
]


def get_app_password() -> str:
    """Read the password from Streamlit secrets or an environment variable."""
    try:
        secret_password = st.secrets.get("APP_PASSWORD")
    except Exception:
        secret_password = None

    return os.environ.get("KIRI_APP_PASSWORD") or secret_password or "kiri"


def init_state() -> None:
    defaults = {
        "authenticated": False,
        "page": "Home",
        "question_index": 0,
        "balloons_launched": False,
        "sound_enabled": False,
        "play_beep": False,
        "beep_bytes": None,
    }

    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


@st.cache_resource
def get_machi() -> MachiWeb:
    return MachiWeb()


def set_machi_beep(wav_bytes: bytes) -> None:
    st.session_state.beep_bytes = wav_bytes
    st.session_state.play_beep = True


def render_pending_audio() -> None:
    if not st.session_state.get("play_beep"):
        return

    if st.session_state.get("sound_enabled") and st.session_state.get("beep_bytes"):
        play_wav_bytes_autoplay(st.session_state.beep_bytes, volume=0.45)

    st.session_state.play_beep = False
    st.session_state.beep_bytes = None


def render_styles() -> None:
    st.markdown(
        """
        <style>
          .machi-card {
            border: 1px solid rgba(255, 184, 76, 0.35);
            border-radius: 12px;
            padding: 1rem 1.1rem;
            margin: 1rem 0;
            background:
              linear-gradient(135deg, rgba(255, 246, 214, 0.95), rgba(232, 248, 244, 0.95));
            box-shadow: 0 10px 28px rgba(43, 62, 80, 0.08);
          }

          .machi-label {
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: #7a5a18;
            margin-bottom: 0.35rem;
          }

          .machi-line {
            color: #24303f;
            font-size: 1rem;
            line-height: 1.5;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def machi_speech(text: str) -> None:
    st.markdown(
        f"""
        <div class="machi-card">
          <div class="machi-label">Machi transmission</div>
          <div class="machi-line">🤖 {text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quiz_image(image_path: Optional[str]) -> None:
    if not image_path:
        return

    path = Path(image_path)
    if path.exists():
        st.image(str(path), use_container_width=True)
    else:
        st.info(f"Add this question's close-up image at `{image_path}`.")


def password_gate() -> bool:
    if st.session_state.authenticated:
        return True

    st.title("Kiri's Adoption Day")
    st.write("Enter the password to open the celebration.")

    with st.form("password_form"):
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Unlock")

    if submitted:
        if password == get_app_password():
            st.session_state.authenticated = True
            set_machi_beep(get_machi().beep_happy())
            st.rerun()
        else:
            st.error("Incorrect password, please try again.")

    return False


@st.dialog("Incorrect")
def show_incorrect_dialog() -> None:
    machi_speech("bzzzt. incorrect answer detected. recalibrating optimism...")
    st.write("incorrect, plrease try again")
    if st.button("Try again"):
        st.rerun()


@st.dialog("Correct")
def show_correct_dialog(info: str) -> None:
    machi_speech("answer accepted. celebratory tiny noises deployed.")
    st.write(info)

    if st.button("Next question"):
        st.session_state.question_index += 1
        set_machi_beep(get_machi().beep_question())
        st.rerun()


def render_sidebar() -> None:
    st.sidebar.title("Kiri")

    if st.sidebar.button("Enable sound" if not st.session_state.sound_enabled else "Sound enabled"):
        st.session_state.sound_enabled = True
        set_machi_beep(get_machi().machi_talk_wav(syllables=10))
        st.rerun()

    st.sidebar.caption("Browsers need one click before Machi can beep.")

    selected_page = st.sidebar.radio(
        "Go to",
        ["Home", "Adoption day quiz"],
        index=["Home", "Adoption day quiz"].index(st.session_state.page),
    )
    st.session_state.page = selected_page

    if st.sidebar.button("Restart quiz"):
        st.session_state.question_index = 0
        st.session_state.page = "Adoption day quiz"
        st.rerun()


def render_home() -> None:
    st.title("happy adoption day kiri!")

    if not st.session_state.balloons_launched:
        st.balloons()
        st.session_state.balloons_launched = True

    st.write("A tiny celebration app, made especially for Kiri.")
    machi_speech("beep boop. adoption day celebration systems online.")

    if st.button("Start the adoption day quiz", type="primary"):
        st.session_state.page = "Adoption day quiz"
        set_machi_beep(get_machi().beep_question())
        st.rerun()


def render_quiz() -> None:
    st.title("Adoption day quiz")

    question_index = st.session_state.question_index
    total_questions = len(QUIZ_QUESTIONS)

    if question_index >= total_questions:
        st.success("Quiz complete. Happy adoption day, Kiri!")
        machi_speech("quiz complete. maximum Kiri appreciation achieved.")
        st.balloons()

        if st.button("Play again"):
            st.session_state.question_index = 0
            set_machi_beep(get_machi().beep_happy())
            st.rerun()
        return

    question = QUIZ_QUESTIONS[question_index]
    machi_speech("question loaded. please select the most emotionally correct answer.")
    st.progress((question_index + 1) / total_questions)
    st.caption(f"Question {question_index + 1} of {total_questions}")
    render_quiz_image(question.get("image"))

    selected_answer = st.radio(
        question["question"],
        question["options"],
        index=None,
        key=f"question_{question_index}",
    )

    if st.button("Submit answer", disabled=selected_answer is None):
        if selected_answer == question["answer"]:
            set_machi_beep(get_machi().machi_talk_wav(syllables=12))
            show_correct_dialog(question["info"])
        else:
            set_machi_beep(get_machi().beep_error())
            show_incorrect_dialog()


def main() -> None:
    init_state()
    render_styles()

    if not password_gate():
        render_pending_audio()
        return

    render_sidebar()

    if st.session_state.page == "Home":
        render_home()
    else:
        render_quiz()

    render_pending_audio()


if __name__ == "__main__":
    main()
