import uuid 
import enum
from datetime import datetime, timezone 

from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class PostState(enum.Enum):
    unsorted = "unsorted"
    kept = "kept"
    discarded = "discarded"


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
    __tablename__ = "folders"

    id:             Mapped[uuid.UUID] = mapped_column(primary_key=True, default = uuid.uuid4)
    user_id:        Mapped[uuid.UUID] = mapped_column( ForeignKey("users.id", ondelete = "CASCADE"))
    parent_id:      Mapped[uuid.UUID| None] = mapped_column(ForeignKey("folders.id", ondelete="CASCADE"))
    name:           Mapped[str] = mapped_column(String(100))
    cover:          Mapped[str |None] = mapped_column(String(255))
    color:          Mapped[str |None] = mapped_column(String(20))
    created_at:     Mapped[datetime] = mapped_column(DateTime(timezone=True), default= now_utc)

class Folder(Base):
    __tablename__ = "posts"
    __table_args__ = (UniqueConstraint("user_id", "url"),)

