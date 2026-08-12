# Kiri Adoption Day Streamlit App

A simple password-protected Streamlit app with a celebration homepage and multiple-choice adoption day quiz.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The local default password is:

```text
kiri
```

To use a different local password, set:

```bash
export KIRI_APP_PASSWORD="your-password"
streamlit run app.py
```

## Streamlit Cloud password

In Streamlit Cloud, add this under **App settings → Secrets**:

```toml
APP_PASSWORD = "your-password"
```

The app will use that password automatically.

## Quiz images

Put close-up quiz images in:

```text
assets/quiz/
```

The current placeholder filenames are:

```text
assets/quiz/q1-closeup.jpg
assets/quiz/q2-closeup.jpg
assets/quiz/q3-closeup.jpg
assets/quiz/q4-closeup.jpg
```

Pre-cropped close-ups are best. Use `.jpg` or `.png`, and keep the images roughly the same shape so the quiz layout feels consistent.
