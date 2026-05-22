from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="pending")
    source = Column(String(50), default="telegram")
    created_at = Column(DateTime, default=datetime.utcnow)