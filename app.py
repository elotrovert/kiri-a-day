import base64
import html
import mimetypes
import os
from pathlib import Path
from typing import Optional

import streamlit as st
from PIL import Image

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
        "reveal_image": "assets/reveals/q1-reveal.png",
        "question": "Machi close-up scan 01: what is this tiny mystery detail?"
                    "hint: first cafe",
        "options": [
            "BD",
            "AB",
            "CD",
            "AA",
        ],
        "answer": "BD",
        "info": "Correct. Machi's sensors confirm this close-up belongs in the Kiri adoption day archive.",
    },
    {
        "image": "assets/quiz/q2-closeup.png",
        "reveal_image": "assets/reveals/q2-reveal.png",
        "question": "Machi close-up scan 02: identify the suspiciously adorable clue."
                    "hint: the best",
        "options": [
            "POLO",
            "OQCM",
            "MOIL",
            "OMQC",
        ],
        "answer": "OQCM",
        "info": "Exactly. Machi awards one ceremonial beep for expert close-up recognition.",
    },
    {
        "image": "assets/quiz/q3-closeup.png",
        "reveal_image": "assets/reveals/q3-reveal.png",
        "question": "Machi close-up scan 03: what object has been zoomed to maximum mystery?"
                    "hint: k",
        "options": [
            "C",
            "A",
            "K",
            "P",
        ],
        "answer": "K",
        "info": "Yes. The image analysis unit is delighted. The snack-adjacent answer has been accepted.",
    },
    {
        "image": "assets/quiz/q4-closeup.png",
        "reveal_image": "assets/reveals/q4-reveal.png",
        "question": "Machi close-up scan 04: final zoom challenge. What are we looking at?"
                    "hint: no hint",
        "options": [
            "DK",
            "PL",
            "YC",
            "MY",
        ],
        "answer": "YC",
        "info": "Correct. Machi logs the result as: deeply loved, visually identified, emotionally verified.",
    },
]


PRIZE_IMAGE_DIR = Path("assets/prize")
FIRST_PRIZE_IMAGE = str(PRIZE_IMAGE_DIR / "prize.png")
BONUS_PRIZE_IMAGE = str(PRIZE_IMAGE_DIR / "bonus_prize.png")


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
        "difficulty": "Hard",
        "prize_stage": "first",
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

          .reveal-stage {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 250px;
            margin: 1rem 0 0.75rem;
            overflow: visible;
          }

          .reveal-image {
            width: min(100%, 420px);
            max-height: 56vh;
            object-fit: contain;
            border-radius: 14px;
            box-shadow: 0 18px 45px rgba(32, 38, 48, 0.24);
            animation: machiRevealFly 720ms cubic-bezier(.16, .84, .3, 1.2) both;
            transform-origin: 50% 85%;
          }

          @keyframes machiRevealFly {
            0% {
              opacity: 0;
              transform: translateY(90px) scale(0.24) rotate(-7deg);
            }
            60% {
              opacity: 1;
              transform: translateY(-12px) scale(1.08) rotate(2deg);
            }
            100% {
              opacity: 1;
              transform: translateY(0) scale(1) rotate(0);
            }
          }

          div[data-testid="column"] div[data-testid="stButton"] > button {
            font-size: 2.6rem;
            line-height: 1;
            height: 110px;
            width: 100%;
            border-radius: 16px;
            background: linear-gradient(160deg, #ff8a8a 0%, #ffb347 100%);
            border: 3px solid #d9534f;
            color: white;
            box-shadow: 0 10px 22px rgba(217, 83, 79, 0.35);
            transition: transform 150ms ease, box-shadow 150ms ease;
          }

          div[data-testid="column"] div[data-testid="stButton"] > button:hover {
            transform: translateY(-4px) scale(1.03);
            box-shadow: 0 14px 28px rgba(217, 83, 79, 0.45);
            border-color: #c9302c;
            color: white;
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


def crop_center(image_path: Path, crop_ratio: float = 0.5) -> Image.Image:
    image = Image.open(image_path)
    width, height = image.size
    crop_width = max(1, int(width * crop_ratio))
    crop_height = max(1, int(height * crop_ratio))
    left = (width - crop_width) // 2
    top = (height - crop_height) // 2
    return image.crop((left, top, left + crop_width, top + crop_height))


def render_quiz_image(image_path: Optional[str]) -> None:
    if not image_path:
        return

    path = Path(image_path)
    if path.exists():
        if st.session_state.difficulty == "Hard":
            st.caption("Hard mode: Machi has zoomed this clue to the center 50%.")
            st.image(crop_center(path), use_container_width=True)
        else:
            st.caption("Easy mode: full close-up image.")
            st.image(str(path), use_container_width=True)
    else:
        st.info(f"Add this question's close-up image at `{image_path}`.")


def render_reveal_image(image_path: Optional[str]) -> None:
    if not image_path:
        return

    path = Path(image_path)
    if not path.exists():
        st.info(f"Add the correct-answer reveal image at `{image_path}`.")
        return

    mime_type = mimetypes.guess_type(path.name)[0] or "image/png"
    image_data = base64.b64encode(path.read_bytes()).decode("utf-8")
    escaped_alt = html.escape(path.stem)

    st.markdown(
        f"""
        <div class="reveal-stage">
          <img class="reveal-image" src="data:{mime_type};base64,{image_data}" alt="{escaped_alt}" />
        </div>
        """,
        unsafe_allow_html=True,
    )


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
def show_correct_dialog(info: str, reveal_image: Optional[str]) -> None:
    machi_speech("answer accepted. celebratory tiny noises deployed.")
    render_reveal_image(reveal_image)
    st.write(info)

    if st.button("Next question"):
        st.session_state.question_index += 1
        set_machi_beep(get_machi().beep_question())
        st.rerun()


@st.dialog("Your Prize!")
def show_prize_dialog(image_path: str, heading: str, next_stage: str) -> None:
    machi_speech("prize protocol engaged. dispensing joy...")
    st.subheader(heading)
    render_reveal_image(image_path)

    button_label = "Continue" if next_stage == "bonus" else "Finish"
    if st.button(button_label):
        st.session_state.prize_stage = next_stage
        if next_stage == "bonus":
            set_machi_beep(get_machi().beep_question())
        else:
            set_machi_beep(get_machi().beep_happy())
        st.rerun()


def render_sidebar() -> None:
    st.sidebar.title("Kiri")

    if st.sidebar.button("Enable sound" if not st.session_state.sound_enabled else "Sound enabled"):
        st.session_state.sound_enabled = True
        set_machi_beep(get_machi().machi_talk_wav(syllables=10))
        st.rerun()

    st.sidebar.caption("Browsers need one click before Machi can beep.")

    st.sidebar.radio(
        "Difficulty",
        ["Hard", "Easy"],
        index=["Hard", "Easy"].index(st.session_state.difficulty),
        key="difficulty",
        help="Hard zooms into the center 50% of each close-up. Easy shows the full image.",
    )

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
    st.title("Happy adoption day 2026 Kiri!")

    if not st.session_state.balloons_launched:
        st.balloons()
        st.session_state.balloons_launched = True

    st.write("A little celebration app, made especially for my pookie.")
    machi_speech("beep boop. adoption day celebration systems online...")

    if st.button("Start the adoption day quiz", type="primary"):
        st.session_state.page = "Adoption day quiz"
        set_machi_beep(get_machi().beep_question())
        st.rerun()


def render_present_row(stage_key: str, image_path: str, heading: str, next_stage: str) -> None:
    cols = st.columns(3)
    for present_index, col in enumerate(cols):
        with col:
            if st.button("🎁", key=f"prize_{stage_key}_{present_index}", use_container_width=True):
                set_machi_beep(get_machi().beep_happy())
                show_prize_dialog(image_path, heading, next_stage)


def render_prize_section() -> None:
    stage = st.session_state.prize_stage

    if stage == "first":
        st.subheader("Select a prize")
        st.caption("Tap a present to see what you've won.")
        render_present_row("first", FIRST_PRIZE_IMAGE, "Prize unlocked!", "bonus")

    elif stage == "bonus":
        st.subheader("Bonus prize")
        st.caption("One more! Tap a present for your bonus prize.")
        render_present_row("bonus", BONUS_PRIZE_IMAGE, "Bonus prize unlocked!", "done")

    else:
        st.success("All prizes collected. Happy adoption day, Kiri!")
        if st.button("Play again"):
            st.session_state.question_index = 0
            st.session_state.prize_stage = "first"
            set_machi_beep(get_machi().beep_happy())
            st.rerun()


def render_quiz() -> None:
    st.title("Adoption day quiz")

    question_index = st.session_state.question_index
    total_questions = len(QUIZ_QUESTIONS)

    if question_index >= total_questions:
        st.success("Quiz complete. Happy adoption day, Kiri!")
        machi_speech("quiz complete. maximum Kiri appreciation achieved.")
        st.balloons()

        render_prize_section()
        return

    question = QUIZ_QUESTIONS[question_index]
    machi_speech("close-up scan loaded. zoom levels: ridiculous. confidence: pending human genius.")
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
            show_correct_dialog(question["info"], question.get("reveal_image"))
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