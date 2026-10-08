def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{secs:02d},"
        f"{milliseconds:03d}"
    )


def create_srt(segments, output_path: str):
    with open(output_path, "w", encoding="utf-8") as file:

        for index, segment in enumerate(segments, start=1):

            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"]

            file.write(f"{index}\n")
            file.write(f"{start} --> {end}\n")
            file.write(f"{text}\n\n")