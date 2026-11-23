import uuid 
from datetime import datetime, timezone 

from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def now_utc():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"

    id:             Mapped[uuid.UUID] = mapped_column(primary_key=True , default= uuid.uuid4)
    email:          Mapped[str] = mapped_column(String(255), unique = True)
    password_hash:  Mapped[str] = mapped_column(String(255))
    name:           Mapped[str] = mapped_column(String(100))
    description:    Mapped[str |None] = mapped_column(Text)
    created_at:     Mapped[datetime] = mapped_column (DateTime(timezone=True), default=now_utc)

class Folder(Base):
    __tablename__ = "folder"
    