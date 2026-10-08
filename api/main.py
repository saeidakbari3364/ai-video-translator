from pathlib import Path
import shutil
import uuid

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

from src.ai_video_translator.pipeline import VideoTranslator


app = FastAPI(
    title="AI Video Translator",
    description="AI-powered video transcription and Persian subtitle translation API",
    version="1.0.0",
)


translator = VideoTranslator()


UPLOAD_DIR = Path("data/uploads")
OUTPUT_DIR = Path("data/output")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


@app.get("/")
def root():

    return {
        "message": "AI Video Translator API",
        "status": "running",
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
    }


@app.post("/translate")
async def translate_video(
    file: UploadFile = File(...)
):

    job_id = str(uuid.uuid4())

    input_path = (
        UPLOAD_DIR /
        f"{job_id}_{file.filename}"
    )

    job_output_dir = (
        OUTPUT_DIR / job_id
    )

    with open(input_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer,
        )

    result = translator.process(
        str(input_path),
        str(job_output_dir),
    )

    return {
        "job_id": job_id,
        "status": "completed",
        "files": {
            "english_srt": result["english_srt"],
            "persian_srt": result["persian_srt"],
        },
        "segments": result["segments"],
    }


@app.get("/download/{job_id}/{filename}")
def download_file(
    job_id: str,
    filename: str,
):

    file_path = (
        OUTPUT_DIR /
        job_id /
        filename
    )

    return FileResponse(
        file_path,
        filename=filename,
    )