import base64
import uuid

import streamlit.components.v1 as components


def play_wav_bytes_autoplay(wav_bytes: bytes, volume: float = 0.45) -> None:
    b64 = base64.b64encode(wav_bytes).decode("utf-8")
    audio_id = f"machi-audio-{uuid.uuid4().hex}"

    components.html(
        f"""
        <audio id="{audio_id}" style="display:none">
          <source src="data:audio/wav;base64,{b64}" type="audio/wav">
        </audio>
        <script>
          (async () => {{
            const audio = document.getElementById("{audio_id}");
            if (!audio) return;
            audio.volume = {max(0.0, min(volume, 1.0))};
            try {{
              audio.load();
              await audio.play();
            }} catch (error) {{
              console.log("Audio blocked:", error);
            }}
          }})();
        </script>
        """,
        height=0,
        width=0,
    )
