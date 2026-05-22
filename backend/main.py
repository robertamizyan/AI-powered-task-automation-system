from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Task Bot Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


active_connections: list[WebSocket] = []


async def notify_clients(message: str):
    disconnected_connections = []

    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception:
            disconnected_connections.append(connection)

    for connection in disconnected_connections:
        active_connections.remove(connection)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "AI Task Bot Backend is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/tasks", response_model=TaskResponse)
async def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    task = Task(
        title=task_data.title,
        description=task_data.description,
        source=task_data.source,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    await notify_clients("task_created")

    return task


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).order_by(Task.id.desc()).all()


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = task_data.status

    db.commit()
    db.refresh(task)

    await notify_clients("task_updated")

    return task


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    await notify_clients("task_deleted")

    return {"message": "Task deleted successfully"}