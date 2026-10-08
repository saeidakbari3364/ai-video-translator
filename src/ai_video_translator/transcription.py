from faster_whisper import WhisperModel


class Transcriber:
    def __init__(
        self,
        model_size: str = "small",
        device: str = "cpu",
        compute_type: str = "int8",
    ):
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type,
        )

    def transcribe(self, video_path: str):
        segments, info = self.model.transcribe(
            video_path,
            beam_size=5,
        )

        results = []

        for segment in segments:
            results.append(
                {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip(),
                }
            )

        return results