# AI Task Bot

AI Task Bot is a full-stack AI-powered task management system that allows users to create tasks through Telegram text messages and Telegram voice messages.

Voice messages are automatically transcribed using Whisper AI and processed asynchronously through a Redis worker architecture.

The project includes:

- Telegram Bot
- FastAPI Backend
- PostgreSQL Database
- Redis Queue
- Async Worker
- Whisper AI Transcription
- React Dashboard
- Real-time updates

---

# Features

## Text Task Creation
Users can send text messages to the Telegram bot.

Example:

```txt
Buy groceries tomorrow
```

The task is automatically saved into PostgreSQL and displayed on the dashboard.

---

## Voice Task Creation
Users can send Telegram voice messages.

Example:

```txt
Finish frontend dashboard tomorrow morning
```

The system:

1. Downloads the audio
2. Adds the job into Redis queue
3. Worker processes audio asynchronously
4. Whisper AI transcribes speech into text
5. Task is saved into PostgreSQL
6. Dashboard updates automatically

---

## Real-Time Dashboard
The React frontend displays:

- Task list
- Task statuses
- Task source
- Real-time updates
- Task counters
- Filtering
- Task deletion

---

# Architecture

```txt
Telegram
    ↓
Bot Service (Aiogram)
    ↓
Redis Queue
    ↓
Worker Service
    ↓
Whisper AI Transcription
    ↓
FastAPI Backend
    ↓
PostgreSQL Database
    ↓
React Frontend Dashboard
```

---

# Tech Stack

## Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- WebSockets

## Frontend
- React
- Axios
- CSS

## AI
- Faster-Whisper

## Async Processing
- Redis
- Worker Service

## Messaging
- Telegram Bot API
- Aiogram

---

# Project Structure

```txt
ai-task-bot/
│
├── backend/
├── bot/
├── worker/
├── frontend/
├── shared/
│
├── .env
├── start.ps1
└── README.md
```

---

# Requirements

## Software

- Python 3.11+
- Node.js
- PostgreSQL
- Redis
- FFmpeg

---

# Environment Variables

Create `.env` in the project root:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tasks_db
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

---

# Installation

## 1. Clone Repository

```powershell
git clone <repository_url>
cd ai-task-bot
```

---

## 2. Backend Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Run backend:

```powershell
uvicorn main:app --reload
```

---

## 3. Bot Setup

```powershell
cd bot
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Run bot:

```powershell
python bot.py
```

---

## 4. Worker Setup

```powershell
cd worker
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Run worker:

```powershell
python worker.py
```

---

## 5. Frontend Setup

```powershell
cd frontend
npm install
npm run dev
```

Frontend URL:

```txt
http://localhost:5173
```

---

# Redis Setup

## Start Redis

```powershell
cd "C:\Program Files\Redis"
.\redis-server.exe --port 6380
```

Expected output:

```txt
Ready to accept connections
```

---

# One-Command Startup

The project includes:

```txt
start.ps1
```

Run:

```powershell
.\start.ps1
```

This automatically starts:

- Redis
- Backend
- Worker
- Telegram Bot
- Frontend

---

# API Endpoints

## Get Tasks

```http
GET /tasks
```

---

## Create Task

```http
POST /tasks
```

---

## Update Task Status

```http
PATCH /tasks/{id}
```

---

## Delete Task

```http
DELETE /tasks/{id}
```

---

# Example Flow

## Text Flow

```txt
Telegram Text
→ Bot
→ Backend
→ PostgreSQL
→ Frontend Dashboard
```

---

## Voice Flow

```txt
Telegram Voice
→ Bot
→ Redis Queue
→ Worker
→ Whisper AI
→ Backend
→ PostgreSQL
→ Frontend Dashboard
```

---


