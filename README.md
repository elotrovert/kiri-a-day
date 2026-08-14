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
assets/quiz/q1-closeup.png
assets/quiz/q2-closeup.png
assets/quiz/q3-closeup.png
assets/quiz/q4-closeup.png
```

Pre-cropped close-ups are best. Use `.png` for the placeholder filenames above, and keep the images roughly the same shape so the quiz layout feels consistent.

## Correct-answer reveal images

Put the full reveal images that appear after a correct guess in:

```text
assets/reveals/
```

The current placeholder filenames are:

```text
assets/reveals/q1-reveal.png
assets/reveals/q2-reveal.png
assets/reveals/q3-reveal.png
assets/reveals/q4-reveal.png
```

These can be wider or larger than the close-ups. When a player guesses correctly, the reveal image pops up in the dialog with a fly-out grow animation.
