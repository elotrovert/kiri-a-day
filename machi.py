import io
import random
import wave

import numpy as np


class MachiWeb:
    """Machi beep sound generator."""

    def __init__(self, sample_rate: int = 44100, amplitude: float = 0.35):
        self.sample_rate = sample_rate
        self.amplitude = float(amplitude)

    def robot_beep(self, frequency: int = 800, duration: float = 0.2) -> np.ndarray:
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        tone = self.amplitude * np.sin(2 * np.pi * frequency * t)

        fade = int(self.sample_rate * 0.01)
        if fade > 1 and len(tone) > 2 * fade:
            ramp = np.linspace(0, 1, fade)
            tone[:fade] *= ramp
            tone[-fade:] *= ramp[::-1]

        return tone.astype(np.float32)

    def _to_wav_bytes(self, audio: np.ndarray) -> bytes:
        audio_i16 = np.int16(np.clip(audio, -1.0, 1.0) * 32767)
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_i16.tobytes())
        return buf.getvalue()

    def _sequence(self, tones: list[tuple[int, float]], gap: float = 0.03) -> bytes:
        parts = []
        for index, (freq, duration) in enumerate(tones):
            parts.append(self.robot_beep(freq, duration))
            if index < len(tones) - 1 and gap > 0:
                parts.append(np.zeros(int(self.sample_rate * gap), dtype=np.float32))
        return self._to_wav_bytes(np.concatenate(parts))

    def beep_classic(self) -> bytes:
        return self._sequence([(600, 0.2), (900, 0.2), (750, 0.3)])

    def beep_happy(self) -> bytes:
        return self._sequence([(700, 0.12), (900, 0.12), (1100, 0.16)], gap=0.02)

    def beep_question(self) -> bytes:
        return self._sequence([(850, 0.15), (700, 0.10), (950, 0.18)], gap=0.03)

    def beep_short(self) -> bytes:
        return self._sequence([(900, 0.12), (600, 0.12)], gap=0.02)

    def beep_shuffle(self) -> bytes:
        freqs = [600, 750, 900, 1050]
        random.shuffle(freqs)
        return self._sequence([(freqs[0], 0.14), (freqs[1], 0.14), (freqs[2], 0.18)], gap=0.02)

    def beep_error(self) -> bytes:
        return self._sequence([(500, 0.10), (300, 0.10)], gap=0.02)

    def random_beep_wav(self) -> bytes:
        choices = [
            self.beep_classic,
            self.beep_happy,
            self.beep_question,
            self.beep_short,
            self.beep_shuffle,
        ]

        if random.random() < 0.7:
            return self.machi_talk_wav(syllables=random.randint(10, 20))

        return random.choice(choices)()

    def machi_talk_wav(self, syllables: int = 8) -> bytes:
        parts = []

        for _ in range(syllables):
            freq = random.choice([600, 700, 800, 900, 1000])
            duration = random.uniform(0.08, 0.18)
            gap = random.uniform(0.03, 0.08)

            parts.append(self.robot_beep(freq, duration))
            parts.append(np.zeros(int(self.sample_rate * gap), dtype=np.float32))

        return self._to_wav_bytes(np.concatenate(parts))
