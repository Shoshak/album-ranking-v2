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
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session, relationship
from datetime import time
import os
import uuid

Base = declarative_base()


class TelegramSession(Base):
    __tablename__ = "sessions"

    id = Column(
        String(32), primary_key=True, default=uuid.uuid4
    )  # UUID stored as string
    telegram_id = Column(Integer, nullable=False, index=True)
    username = Column(String, nullable=True, index=True)
    expires_at = Column(DateTime, nullable=False, index=True)


class Config(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True)
    current_round = Column(Integer, default=1)
    current_order_number = Column(Integer, default=1)
    max_submissions = Column(Integer, default=2)
    submissions_open = Column(Boolean, default=False)
    max_duration = Column(Time, default=time(hour=2))
    max_tracks = Column(Integer, default=30)
    min_tracks = Column(Integer, default=7)


class UserAlbumSubmission(Base):
    __tablename__ = "user_album_submissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, autoincrement=True)
    artist = Column(String, nullable=False)
    name = Column(String, nullable=False)
    release_year = Column(Integer)
    duration = Column(Time, nullable=False)
    total_tracks = Column(Integer, nullable=False)
    round_number = Column(Integer, nullable=False)
    cover = Column(String, nullable=False)
    order_number = Column(Integer)

    __table_args__ = (
        UniqueConstraint("round_number", "order_number", name="uix_round_order"),
    )

    tracks = relationship("Track", back_populates="album", cascade="all, delete-orphan")


class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    track_name = Column(String, nullable=False)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)

    album = relationship("Album", back_populates="tracks")
    rankings = relationship(
        "Ranking", back_populates="track", cascade="all, delete-orphan"
    )


class Ranking(Base):
    __tablename__ = "rankings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    track_id = Column(Integer, ForeignKey("tracks.id"), nullable=False)
    placement = Column(Integer, nullable=False)
    track = relationship("Track", back_populates="rankings")

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
