# ContentFactory — Automated AI Video Production Pipeline

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-red)
![Google AI](https://img.shields.io/badge/Google%20AI-Gemini%20%7C%20Veo-4285F4?logo=google)
![ElevenLabs](https://img.shields.io/badge/Voice-ElevenLabs-black)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker)

An end-to-end **multimodal AI pipeline** that autonomously produces vertical short-form videos (9:16, 1080p) for the medical aesthetics industry. One JSON task definition → production-ready MP4 in minutes.

---

## Pipeline Architecture

```
tasks.json
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  main.py  (asyncio.gather → parallel task execution) │
└─────────────────────────────────────────────────────┘
    │
    ├── [Step 1] image_engine.py
    │       Google Gemini Imagen 3
    │       Generates a photorealistic base image (9:16)
    │
    ├── [Step 2] video_ai_engine.py
    │       Google Veo 3
    │       Animates the image using a motion prompt
    │       Long-running operation → polling loop
    │
    ├── [Step 3] voice_engine.py
    │       ElevenLabs Turbo v2.5
    │       Synthesizes voiceover narration
    │
    └── [Step 4] video_engine.py
            MoviePy
            Assembles: AI video + audio + text overlay + vignette
            Output: output/{task_id}.mp4
```

---

## Tech Stack

| Layer | Technology | Role |
|---|---|---|
| Image Generation | Google Gemini Imagen 3 | Photorealistic base frame |
| Video Generation | Google Veo 3 | Image-to-video animation |
| Voice Synthesis | ElevenLabs Turbo v2.5 | Natural TTS narration |
| Video Assembly | MoviePy / FFmpeg | Final render & compositing |
| Data Validation | Pydantic v2 | Task schema & type safety |
| Config | python-dotenv | Secrets management |
| Containerization | Docker | Reproducible environment |

---

## Project Structure

```
ContentFactory_Medical/
├── main.py              # Async pipeline orchestrator
├── schemas.py           # Pydantic models (VideoTask, PipelineResult)
├── config.py            # Config & versioned file paths
├── tasks.json           # Task definitions (separated from code)
│
├── image_engine.py      # Gemini Imagen integration
├── video_ai_engine.py   # Veo 3 integration (long-running operations)
├── voice_engine.py      # ElevenLabs TTS integration
├── video_engine.py      # MoviePy video assembly
│
├── logger.py            # Structured logging
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## Key Design Decisions

**Async Pipeline** — tasks run concurrently via `asyncio.gather()`. Blocking I/O (API calls, file writes) is offloaded with `asyncio.to_thread()`, so multiple tasks don't wait for each other.

**Pydantic Schemas** — `VideoTask` validates all task fields on load. A malformed `tasks.json` fails fast with a clear error rather than crashing mid-pipeline.

**Modular Engines** — each AI provider is isolated in its own module. Swapping Veo for Runway or ElevenLabs for OpenAI TTS requires changing one file.

**Versioned Outputs** — `config.versioned_path()` prevents overwriting: re-running a task produces `task_v2.mp4`, `task_v3.mp4`, etc.

---

## Quickstart

### 1. Configure environment

```bash
cp .env.example .env
# Fill in: GOOGLE_CLOUD_API_KEY, ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID
```

### 2. Define tasks

Edit `tasks.json`:
```json
[
  {
    "id": "my_campaign",
    "subject": "Close-up of doctor hands performing treatment...",
    "action_prompt": "Gentle movement, slow cinematic motion...",
    "hook": "Real Results.\nReal Science.",
    "body": "Voiceover narration text here."
  }
]
```

### 3. Run

**Local:**
```bash
pip install -r requirements.txt
python main.py
```

**Docker:**
```bash
docker-compose up --build
```

Output files appear in `output/`.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GOOGLE_CLOUD_API_KEY` | Yes | Google AI Studio API key |
| `ELEVENLABS_API_KEY` | Yes | ElevenLabs API key |
| `ELEVENLABS_VOICE_ID` | Yes | ElevenLabs voice ID |
| `MEDICAL_STYLE` | No | Default image style suffix |
| `OUTPUT_DIR` | No | Output directory (default: `output`) |
| `TEMP_DIR` | No | Temp files directory (default: `temp`) |
