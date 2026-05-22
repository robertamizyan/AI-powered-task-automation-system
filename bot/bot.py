import os
import json
import asyncio
from pathlib import Path

import redis
import requests
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
AUDIO_DIR = BASE_DIR / "bot" / "audio"

AUDIO_DIR.mkdir(exist_ok=True)

load_dotenv(dotenv_path=ENV_PATH)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BACKEND_URL = "http://127.0.0.1:8000"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

redis_client = redis.Redis(
    host="localhost",
    port=6380,
    decode_responses=True,
)


def save_task_to_backend(title: str, source: str):
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


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Hello! Send me a text task or voice message, and I will save it."
    )


@dp.message(lambda message: message.voice is not None)
async def voice_handler(message: Message):
    await message.answer("Voice received. Added to processing queue.")

    try:
        file = await bot.get_file(message.voice.file_id)

        audio_path = AUDIO_DIR / f"voice_{message.message_id}.ogg"

        await bot.download_file(
            file.file_path,
            destination=audio_path,
        )

        job_data = {
            "audio_path": str(audio_path),
        }

        redis_client.rpush(
            "voice_tasks",
            json.dumps(job_data),
        )

    except Exception as e:
        await message.answer(f"Queue error: {str(e)}")


@dp.message()
async def text_handler(message: Message):
    if not message.text:
        return

    success = save_task_to_backend(
        title=message.text,
        source="telegram",
    )

    if success:
        await message.answer("Task saved successfully.")
    else:
        await message.answer("Failed to save task.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())