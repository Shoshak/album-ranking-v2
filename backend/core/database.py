from datetime import datetime, time
from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    UniqueConstraint,
    ForeignKey,
    Time,
    DateTime,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
    declarative_base,
    scoped_session,
    relationship,
)
import os
import uuid


class Base(DeclarativeBase):
    pass


class TelegramSession(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(
        String(32), primary_key=True, default=uuid.uuid4
    )  # UUID stored as string
    telegram_id: Mapped[int] = mapped_column(index=True)
    username: Mapped[str] = mapped_column(index=True)
    expires_at: Mapped[datetime] = mapped_column(index=True)


class Config(Base):
    __tablename__ = "config"

    id: Mapped[int] = mapped_column(primary_key=True)
    current_round: Mapped[int] = mapped_column(default=1)
    current_order_number: Mapped[int] = mapped_column(default=1)
    max_submissions: Mapped[int] = mapped_column(default=2)
    submissions_open: Mapped[bool] = mapped_column(default=False)
    max_duration: Mapped[time] = mapped_column(default=time(hour=2))
    max_tracks: Mapped[int] = mapped_column(default=30)
    min_tracks: Mapped[int] = mapped_column(default=7)


class UserAlbumSubmission(Base):
    __tablename__ = "user_album_submissions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column()
    album_id: Mapped[int] = mapped_column(ForeignKey("albums.id"))


class Album(Base):
    __tablename__ = "albums"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    artist: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    release_year: Mapped[int] = mapped_column()
    duration: Mapped[time] = mapped_column()
    total_tracks: Mapped[int] = mapped_column()
    round_number: Mapped[int] = mapped_column()
    cover: Mapped[str] = mapped_column()
    order_number: Mapped[int | None] = mapped_column()

    __table_args__ = (
        UniqueConstraint("round_number", "order_number", name="uix_round_order"),
    )

    tracks: Mapped["Track"] = relationship(
        back_populates="album", cascade="all, delete-orphan"
    )


class Track(Base):
    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    track_name: Mapped[str] = mapped_column()
    album_id: Mapped[int] = mapped_column(ForeignKey("albums.id"))

    album: Mapped["Album"] = relationship(back_populates="tracks")
    rankings: Mapped["Ranking"] = relationship(
        back_populates="track", cascade="all, delete-orphan"
    )


class Ranking(Base):
    __tablename__ = "rankings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column()
    track_id: Mapped[int] = mapped_column(ForeignKey("tracks.id"))
    placement: Mapped[int] = mapped_column()
    track: Mapped["Track"] = relationship(back_populates="rankings")

    __table_args__ = (UniqueConstraint("username", "track_id", name="uix_user_track"),)


db_filename = "app.db"
db_path = os.path.join(os.getcwd(), db_filename)

engine = create_engine(
    f"sqlite:///{db_path}",
    echo=False,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        if session.query(Config).first() is None:
            db_config = Config(id=1)
            session.add(db_config)
            session.commit()
            session.refresh(db_config)
            session.close()
        session.close()
