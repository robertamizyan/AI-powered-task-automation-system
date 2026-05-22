import json
import time
from pathlib import Path

import redis
import requests
from dotenv import load_dotenv
from faster_whisper import WhisperModel


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

BACKEND_URL = "http://127.0.0.1:8000"

redis_client = redis.Redis(
    host="localhost",
    port=6380,
    decode_responses=True,
)

print("Loading Whisper model...")
whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
print("Whisper model loaded.")


def save_task(title: str, source: str):
    task_data = {
        "title": title,
        "description": None,
        "source": source,
    }

    response = requests.post(
        f"{BACKEND_URL}/tasks",
        json=task_data,
    )

    return response.status_code == 200


def transcribe_audio(audio_path: str) -> str:
    segments, info = whisper_model.transcribe(
        audio_path,
        language="en",
    )

    text_parts = []

    for segment in segments:
        text_parts.append(segment.text)

    return " ".join(text_parts).strip()


print("Worker started. Waiting for voice jobs...")


while True:
    job = redis_client.lpop("voice_tasks")

    if not job:
        time.sleep(1)
        continue

    try:
        job_data = json.loads(job)
        audio_path = job_data["audio_path"]

        print(f"Processing audio: {audio_path}")

        text = transcribe_audio(audio_path)

        if not text:
            print("No transcription generated.")
            continue

        success = save_task(
            title=text,
            source="telegram_voice_worker",
        )

        if success:
            print(f"Task saved: {text}")
        else:
            print("Failed to save task to backend.")

    except Exception as e:
        print("Worker error:", e)