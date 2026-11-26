import uuid 
import enum
from datetime import datetime, timezone 

from sqlalchemy import String, Text, DateTime, ForeignKey, Enum, UniqueConstraint, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class PostState(enum.Enum):
    unsorted = "unsorted"
    kept = "kept"
    discarded = "discarded"

class Platform(enum.Enum):
    instagram = "instagram"
    tiktok ="tiktok"

class NoteTag(enum.Enum):
    inspiration ="inspiration"
    want_to_try = "want_to_try"
    to_visit = "to_visit"


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

class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (UniqueConstraint("user_id", "url"),)

    id:         Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id:    Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    platform:   Mapped[Platform] = mapped_column(Enum(Platform, name="platform"))
    url:        Mapped[str] = mapped_column(String(500))
    caption:    Mapped[str | None] = mapped_column(Text)
    author:     Mapped[str | None] = mapped_column(String(100))
    hashtags:   Mapped[list[str] | None] = mapped_column(JSON)
    saved_at:   Mapped[datetime] = mapped_column(DateTime(timezone=True))
    state:      Mapped[PostState] = mapped_column(Enum(PostState, name="post_state"), default=PostState.unsorted)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class PostFolder(Base):
    __tablename__ = "post_folders"

    post_id:   Mapped[uuid.UUID] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    folder_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("folders.id", ondelete="CASCADE"), primary_key=True)


class Note(Base):
    __tablename__ = "notes"

    id:         Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    post_id:    Mapped[uuid.UUID] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    text:       Mapped[str | None] = mapped_column(Text)
    tag:        Mapped[NoteTag | None] = mapped_column(Enum(NoteTag, name="note_tag"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
