from pathlib import Path

from src.ai_video_translator.transcription import Transcriber
from src.ai_video_translator.translation import Translator
from src.ai_video_translator.subtitle import create_srt


def main():

    video_path = "data/input/test.mp4"

    english_srt_path = "data/output/english.srt"
    persian_srt_path = "data/output/persian.srt"

    Path("data/output").mkdir(
        parents=True,
        exist_ok=True,
    )

    # -----------------------------
    # 1. Speech To Text
    # -----------------------------

    print("Loading Whisper model...")

    transcriber = Transcriber(
        model_size="small",
        device="cpu",
        compute_type="int8",
    )

    print("Transcribing video...")

    segments = transcriber.transcribe(
        video_path
    )

    print(
        f"Detected {len(segments)} segments."
    )

    # -----------------------------
    # 2. English Subtitle
    # -----------------------------

    create_srt(
        segments,
        english_srt_path,
    )

    print(
        f"English subtitle saved to: "
        f"{english_srt_path}"
    )

    # -----------------------------
    # 3. Translation
    # -----------------------------

    translator = Translator()

    print("Translating segments...")

    translated_segments = (
        translator.translate_segments(
            segments
        )
    )

    # -----------------------------
    # 4. Persian Subtitle
    # -----------------------------

    create_srt(
        translated_segments,
        persian_srt_path,
    )

    print(
        f"Persian subtitle saved to: "
        f"{persian_srt_path}"
    )


if __name__ == "__main__":
    main()