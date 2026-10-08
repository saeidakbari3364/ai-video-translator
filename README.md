# 🎬 AI Video Translator

An end-to-end **AI-powered video translation system** that automatically extracts speech from videos, generates time-aligned subtitles, translates them into Persian, and exposes the pipeline through a REST API.

The project demonstrates a practical **AI Engineering workflow** combining Speech-to-Text, Machine Translation, subtitle generation, FastAPI, Docker, and modern Python project management.

---

## 🚀 Features

* 🎙️ **Automatic Speech Recognition (ASR)**

  * Uses [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper)
  * Converts video speech into text
  * Generates accurate timestamps for each segment

* 📝 **Automatic Subtitle Generation**

  * Generates standard `.srt` subtitle files
  * Preserves original timestamps

* 🌍 **English → Persian Translation**

  * Uses Meta's NLLB-200 translation model
  * Translates each subtitle segment independently
  * Keeps the original subtitle timing

* ⚡ **REST API**

  * Built with FastAPI
  * Interactive Swagger documentation
  * Video upload endpoint
  * Subtitle download endpoint

* 🐳 **Docker Support**

  * Containerized application
  * Includes FFmpeg
  * Ready for deployment

---

## 🧠 System Architecture

```text
                    ┌──────────────────┐
                    │    Video File    │
                    │     (.mp4)       │
                    └────────┬─────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Faster-Whisper    │
                  │    Speech-to-Text   │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Timestamped Text   │
                  │ start / end / text  │
                  └──────────┬──────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
       ┌────────────────┐       ┌─────────────────┐
       │  English SRT   │       │   NLLB-200      │
       │   Generation   │       │   Translation   │
       └────────────────┘       └────────┬────────┘
                                         │
                                         ▼
                                ┌─────────────────┐
                                │   Persian SRT   │
                                │   Generation    │
                                └─────────────────┘
```

---

## 🔄 Processing Pipeline

The complete pipeline is:

```text
Video
  │
  ▼
Speech Recognition
  │
  ▼
Timestamped Transcript
  │
  ├──────────────► English Subtitles
  │
  ▼
Machine Translation
  │
  ▼
Persian Subtitles
```

The important point is that **translation changes only the text**.

The original `start` and `end` timestamps are preserved:

```python
{
    "start": 12.50,
    "end": 16.80,
    "text": "متن ترجمه شده"
}
```

This allows the translated subtitle to remain synchronized with the original video.

---

## 🛠️ Tech Stack

| Technology                | Purpose                      |
| ------------------------- | ---------------------------- |
| Python 3.11               | Main programming language    |
| Faster-Whisper            | Speech-to-Text               |
| NLLB-200                  | Machine Translation          |
| PyTorch                   | Deep Learning backend        |
| Hugging Face Transformers | Translation model            |
| FFmpeg                    | Video/audio processing       |
| FastAPI                   | REST API                     |
| Uvicorn                   | ASGI server                  |
| uv                        | Python dependency management |
| Docker                    | Containerization             |
| SRT                       | Subtitle format              |

---

## 📁 Project Structure

```text
ai-video-translator/
│
├── api/
│   └── main.py
│
├── data/
│   ├── input/
│   │   └── test.mp4
│   │
│   ├── output/
│   │
│   └── uploads/
│
├── src/
│   └── ai_video_translator/
│       ├── __init__.py
│       ├── transcription.py
│       ├── translation.py
│       ├── subtitle.py
│       └── pipeline.py
│
├── main.py
├── Dockerfile
├── .dockerignore
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-video-translator.git

cd ai-video-translator
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## 2. Install FFmpeg

FFmpeg is required for video/audio processing.

Check the installation:

```bash
ffmpeg -version
```

If the command works, FFmpeg is ready.

---

## 3. Install dependencies

This project uses `uv`.

If `uv` is not installed:

```bash
pip install uv
```

Then:

```bash
uv sync
```

---

# ▶️ Run the Local Pipeline

Place a test video inside:

```text
data/input/test.mp4
```

Then run:

```bash
uv run python main.py
```

The system will:

1. Load Faster-Whisper
2. Transcribe the video
3. Generate English subtitles
4. Load NLLB-200
5. Translate the subtitles into Persian
6. Generate the Persian `.srt` file

Output:

```text
data/output/
├── english.srt
└── persian.srt
```

---

# 🌐 Run the API

Start FastAPI:

```bash
uv run uvicorn api.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 📡 API Endpoints

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

---

### Translate Video

```http
POST /translate
```

Upload a video file and the system will:

```text
Video
 ↓
Whisper
 ↓
English SRT
 ↓
NLLB
 ↓
Persian SRT
```

Example response:

```json
{
  "job_id": "example-job-id",
  "status": "completed",
  "files": {
    "english_srt": "data/output/example-job-id/english.srt",
    "persian_srt": "data/output/example-job-id/persian.srt"
  },
  "segments": 23
}
```

---

### Download Subtitle

```http
GET /download/{job_id}/{filename}
```

Example:

```text
/download/example-job-id/persian.srt
```

---

# 🧪 Example

Suppose the video contains:

```text
Hello, and welcome to our tutorial on data science.
```

Faster-Whisper produces:

```text
Start: 0.00
End:   7.44

Hello, and welcome to our tutorial on data science.
```

The English SRT becomes:

```text
1
00:00:00,000 --> 00:00:07,440
Hello, and welcome to our tutorial on data science.
```

NLLB then translates the text:

```text
سلام، به آموزش ما درباره علم داده خوش آمدید.
```

The Persian SRT keeps the same timing:

```text
1
00:00:00,000 --> 00:00:07,440
سلام، به آموزش ما درباره علم داده خوش آمدید.
```

---

# 🧩 Core Components

## 1. Transcription

`transcription.py`

Responsible for converting speech into timestamped text.

```python
Transcriber
```

Uses:

```text
Faster-Whisper
```

Output:

```python
{
    "start": 0.0,
    "end": 7.44,
    "text": "Hello, and welcome..."
}
```

---

## 2. Translation

`translation.py`

Responsible for translating subtitle text.

Model:

```text
facebook/nllb-200-distilled-600M
```

Language configuration:

```text
English → Persian

eng_Latn → pes_Arab
```

---

## 3. Subtitle Generation

`subtitle.py`

Converts timestamped segments into the standard SRT format.

```text
Index
Timestamp
Text
```

Example:

```text
1
00:00:00,000 --> 00:00:07,440
Hello, and welcome...
```

---

## 4. Pipeline

`pipeline.py`

Coordinates the complete workflow:

```python
VideoTranslator
```

The pipeline combines:

```text
Transcriber
      ↓
Subtitle Generator
      ↓
Translator
      ↓
Persian Subtitle Generator
```

---

# 🐳 Docker

Build the image:

```bash
docker build -t ai-video-translator .
```

Run the container:

```bash
docker run -p 8000:8000 ai-video-translator
```

Open:

```text
http://localhost:8000/docs
```

---

# 📦 Docker Architecture

```text
┌───────────────────────────────────┐
│       Docker Container            │
│                                   │
│  ┌─────────────┐                  │
│  │   FastAPI   │                  │
│  └──────┬──────┘                  │
│         │                         │
│         ▼                         │
│  ┌─────────────┐                  │
│  │   Pipeline  │                  │
│  └──────┬──────┘                  │
│         │                         │
│    ┌────┴─────┐                   │
│    ▼          ▼                   │
│ Whisper      NLLB                 │
│    │          │                   │
│    └────┬─────┘                   │
│         ▼                         │
│      SRT Files                    │
│                                   │
└───────────────────────────────────┘
```

---

# ⚠️ Performance Notes

This project is currently designed primarily for **learning, prototyping, and AI Engineering portfolio development**.

Both models run locally:

```text
Faster-Whisper
NLLB-200
```

On CPU, processing can be relatively slow, especially for long videos.

For production workloads, GPU acceleration is recommended.

---

# 🔮 Future Improvements

The project can be extended into a production-grade video translation platform.

### Planned features

* [ ] Background job processing
* [ ] Celery + Redis
* [ ] PostgreSQL job database
* [ ] Job status API
* [ ] Progress tracking
* [ ] Automatic language detection
* [ ] Support for multiple source languages
* [ ] Support for multiple target languages
* [ ] Video/audio extraction with FFmpeg
* [ ] Persian TTS
* [ ] AI voice dubbing
* [ ] Speaker diarization
* [ ] Subtitle burning
* [ ] Web-based frontend
* [ ] Authentication
* [ ] File size/type validation
* [ ] Cloud storage
* [ ] Production deployment
* [ ] GPU inference
* [ ] Monitoring and logging

---

# 🏗️ Future Production Architecture

The planned production architecture is:

```text
                   Client
                     │
                     ▼
               ┌──────────┐
               │ FastAPI  │
               └────┬─────┘
                    │
                    ▼
              ┌────────────┐
              │ PostgreSQL │
              │    Jobs    │
              └────────────┘
                    │
                    ▼
               ┌─────────┐
               │  Redis  │
               └────┬────┘
                    │
                    ▼
             ┌──────────────┐
             │Celery Worker │
             └──────┬───────┘
                    │
             ┌──────┴──────┐
             ▼             ▼
        Faster-Whisper    NLLB
             │             │
             └──────┬──────┘
                    ▼
               Subtitle
                Storage
```

This architecture allows the API to accept videos without keeping the HTTP request blocked while AI models process the video.

---

# 🎯 Learning Objectives

This project demonstrates several important concepts in modern AI Engineering:

* Speech-to-Text
* Natural Language Processing
* Machine Translation
* Generative AI pipelines
* Timestamp alignment
* Python project structure
* Dependency management with `uv`
* REST API development
* FastAPI
* Docker
* Model serving
* AI pipeline orchestration
* Production architecture

---

# 👨‍💻 Author

**Saeid Akbari**

AI Engineer & Educator

Focused on:

```text
Artificial Intelligence
Machine Learning
Deep Learning
NLP
Agentic AI
MLOps
AI Engineering
```

---

# 📄 License

This project is intended for educational and portfolio purposes.

Add an appropriate open-source license before public distribution, such as MIT, if desired.
