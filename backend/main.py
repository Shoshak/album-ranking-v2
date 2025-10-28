from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import true, and_, or_, update, func
from .core.database import (
    get_session,
    create_db_and_tables,
    TelegramSession,
    Config,
    UserAlbumSubmission,
    Album,
    Track,
    Ranking,
    User,
)
from .core import schemas
from .core.api import processUrl
from dotenv import load_dotenv
import datetime
import time
import os
import hmac
import hashlib
import uuid


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://0.0.0.0:5173",
        "http://26.217.61.253:5173",
        "http://192.168.0.248:5173/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


@app.get("/users/")
async def get_users(telegram_id: int = None, session: Session = Depends(get_session)):
    db_users = (
        session.query(User)
        .where((User.id == id) if telegram_id is not None else true())
        .all()
    )
    if len(db_users) == 0:
        raise HTTPException(status_code=404, detail="Пользователи не найдены.")
    return db_users


@app.post("/users/")
async def create_user(user: schemas.User, session: Session = Depends(get_session)):
    db_user = User(
        id=user.id,
        username=user.username,
        admin_rights=user.admin_rights,
    )
    if session.query(User).where(User.id == user.id).first() is not None:
        raise HTTPException(status_code=500, detail="Пользователь уже существует.")
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/sessions/")
async def get_sessions(telegram_id: str, session: Session = Depends(get_session)):
    db_session = (
        session.query(Session).where(Session.telegram_id == telegram_id).first()
    )
    if db_session is None:
        raise HTTPException(status_code=404, detail="Сессия не найдена.")
    return db_session


@app.post("/sessions/")
async def create_session(
    data: schemas.Session, session: Session = Depends(get_session)
):
    check_hash = data.hash
    data_check_arr = []
    for key, value in data:
        if key != "hash":
            data_check_arr.append(f"{key}={value}")
    data_check_arr.sort()
    data_check_string = "\n".join(data_check_arr)
    secret_key = hashlib.sha256(TELEGRAM_TOKEN.encode()).digest()
    hash_value = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    if hash_value != check_hash:
        raise HTTPException(status_code=403, detail="Данные не из Telegram.")

    if (time.time() - data.auth_date) > 86400:
        raise HTTPException(status_code=408, detail="Данные устарели.")

    if session.query(Session).where(Session.telegram_id == data.id).first() is not None:
        raise HTTPException(status_code=500, detail="Сессия уже существует.")
    db_session = Session(
        telegram_id=data.id,
        expires_at=(
            datetime.datetime.fromtimestamp(data.auth_date)
            + datetime.timedelta(days=14)
        ),
    )
    session.add(db_session)
    session.commit()
    session.refresh(db_session)
    return db_session


@app.patch("/sessions/")
async def change_session(
    data: schemas.SessionPatch, session: Session = Depends(get_session)
):
    db_session = (
        session.query(Session)
        .where(
            Session.id == data.id,
        )
        .first()
    )
    session_update = (
        update(Session)
        .where(
            Session.id == data.id,
        )
        .values(
            expires_at=datetime.datetime.fromtimestamp(data.auth_date)
            + datetime.timedelta(days=14)
        )
    )
    session.execute(session_update)
    session.commit()
    session.refresh(db_session)
    return db_session


@app.get("/albums/")
async def get_albums(
    session: Annotated[Session, Depends(get_session)],
    artist: str | None = None,
    name: str | None = None,
    release_year: int | None = None,
    no_spoilers: bool = False,
):
<<<<<<< HEAD
    config = session.query(Config).first()
    if not config:
        raise HTTPException(status_code=404, detail="Конфиг не найден.")
=======
    db_config = session.query(Config).first()
>>>>>>> ca9f3ffdc88753ec1a27e30fd7c1cbb7aa39c7f4
    db_albums = session.query(Album).where(
        (Album.artist == artist) if artist is not None else true(),
        (Album.name == name) if name is not None else true(),
        ((Album.release_year == release_year) if release_year is not None else true()),
    )
    if no_spoilers:
        db_albums = (
            db_albums.where(
                (Album.round_number < db_config.current_round),
            ).all()
            + db_albums.where(
                and_(
                    (Album.order_number < db_config.current_order_number),
                    (Album.round_number == db_config.current_round),
                )
            ).all()
        )
    else:
        db_albums = db_albums.all()
    if len(db_albums) == 0:
        raise HTTPException(status_code=404, detail="Альбомы не найдены.")
    return db_albums


@app.post("/albums/")
async def create_album(
    album: schemas.Album,
    session: Annotated[Session, Depends(get_session)],
):
    config = session.query(Config).first()
    if not config:
        raise HTTPException(status_code=404, detail="Конфиг не найден.")
    if not config.submissions_open:
        raise HTTPException(status_code=500, detail="Отправка альбомов закрыта")
    requested_album = processUrl(album.source, album.url)
    artist = requested_album["artist"]
    name = requested_album["name"]
    release_year = requested_album["release_year"]
    duration = requested_album["duration"]
    total_tracks = requested_album["total_tracks"]
    cover = requested_album["cover"]
    for key in ("artist", "name", "release_year", "total_tracks", "duration", "cover"):
        requested_album.pop(key, None)
    tracks = list(requested_album.values())
    q = session.query(Album)
    if q.where(and_(Album.artist == artist, Album.name == name)).first() is not None:
        raise HTTPException(status_code=500, detail="Альбом уже был на круге")
    if (
        q.where(
            or_(
                and_(
                    Album.round_number == config.current_round - 1,
                    Album.artist == artist,
                ),
                and_(
                    Album.round_number == config.current_round,
                    Album.artist == artist,
                ),
            )
        ).first()
        is not None
    ):
        raise HTTPException(
            status_code=500,
            detail="Этот исполнитель уже был на этом или прошлом круге",
        )
    if not (config.min_tracks <= total_tracks <= config.max_tracks):
        raise HTTPException(
            status_code=500, detail="У альбома неподходящее количество треков"
        )
    if not (duration <= config.max_duration):
        raise HTTPException(
            status_code=500, detail="Длина альбома превышает разрешённую"
        )
    if (
        len(
            session.query(UserAlbumSubmission)
            .join(
                Album,
                and_(
                    UserAlbumSubmission.album_id == Album.id,
                    Album.round_number == config.current_round,
                ),
            )
            .where(UserAlbumSubmission.username == album.username)
            .all()
        )
        == config.max_submissions
    ):
        raise HTTPException(
            status_code=500,
            detail="Этот пользователь уже отправил максимальное количество альбомов",
        )
    round_albums = q.where(Album.round_number == config.current_round).all()
    db_album = Album(
        artist=artist,
        name=name,
        duration=duration,
        total_tracks=total_tracks,
        release_year=release_year,
        round_number=config.current_round,
        cover=cover,
        order_number=(
            (round_albums[-1].order_number + 1) if len(round_albums) != 0 else 1
        ),
    )
    session.add(db_album)
    session.commit()
    album_id = (
        session.query(Album)
        .where(Album.artist == artist, Album.name == name)
        .first()
        .id
    )
    db_tracks = []
    for track_name in requested_album.values():
        db_tracks.append(Track(track_name=track_name, album_id=album_id))
    session.add_all(db_tracks)
    session.commit()
    userSubmission = UserAlbumSubmission(
        username=album.username,
        album_id=(
            session.query(Album)
            .where(Album.artist == artist, Album.name == name)
            .first()
            .id
        ),
    )
    session.add(userSubmission)
    session.commit()
    session.refresh(db_album)
    return db_album


@app.get("/albums/{album_id}")
async def get_album(album_id: int, session: Annotated[Session, Depends(get_session)]):
    db_album = session.query(Album).where(Album.id == album_id).first()
    if not db_album:
        raise HTTPException(status_code=404, detail="Альбом не найден.")
    return db_album


@app.post("/albums/{album_id}")
async def create_ranking(
    album_id: int,
    ranking: schemas.Ranking,
    session: Annotated[Session, Depends(get_session)],
):
    db_album = session.query(Album).where(Album.id == album_id).first()
    tracks = session.query(Track).where(Track.album_id == album_id).all()
    db_rankings = []
    if len(tracks) == 0:
        raise HTTPException(status_code=404, detail="Альбом не найден.")
    if len(tracks) != len(ranking.placements):
        raise HTTPException(
            status_code=400,
            detail="Количество позиций не равно количеству треков в альбоме.",
        )
    if (
        session.query(Ranking)
        .where(
            and_(
                Ranking.username == ranking.username,
                Ranking.track_id == tracks[0].id,
            )
        )
        .first()
        is not None
    ):
        raise HTTPException(
            status_code=400,
            detail="У этого пользователя уже есть оценки.",
        )
    for i in range(len(ranking.placements)):
        db_ranking = Ranking(
            username=ranking.username,
            track_id=tracks[i].id,
            placement=ranking.placements[i],
        )
        db_rankings.append(db_ranking)
    session.add_all(db_rankings)
    session.commit()
    session.refresh(db_album)
    return db_album


@app.patch("/albums/{album_id}")
async def change_ranking(
    album_id: int,
    ranking: schemas.Ranking,
    session: Annotated[Session, Depends(get_session)],
):
    db_album = session.query(Album).where(Album.id == album_id).first()
    tracks = session.query(Track).where(Track.album_id == album_id).all()
    for i in range(len(ranking.placements)):
        db_ranking = (
            session.query(Ranking)
            .where(
                and_(
                    Ranking.track_id == tracks[i].id,
                    Ranking.username == ranking.username,
                )
            )
            .first()
        )
        ranking_update = (
            update(Ranking)
            .where(
                and_(
                    Ranking.username == ranking.username,
                    Ranking.track_id == tracks[i].id,
                )
            )
            .values(placement=ranking.placements[i])
        )
        session.execute(ranking_update)
    session.commit()
    session.refresh(db_album)
    return db_album


@app.get("/tracks/")
async def get_tracks(
    session: Annotated[Session, Depends(get_session)],
    track_name: str | None = None,
):
    config = session.query(Config).first()
    if not config:
        raise HTTPException(status_code=404, detail="Конфиг не найден.")
    db_album = (
        session.query(Album)
        .where(
            and_(
                Album.round_number == config.current_round,
                Album.order_number == config.current_order_number,
            )
        )
        .first()
    )
    if not db_album:
        raise HTTPException(status_code=404, detail="Оценивание недоступно.")
    m = Track
    db_tracks = (
        session.query(m)
        .where(
            (m.track_name == track_name) if track_name is not None else true(),
            (m.album_id == db_album.id),
        )
        .all()
    )
    if len(db_tracks) == 0:
        raise HTTPException(status_code=404, detail="Треки не найдены.")
    return db_tracks


@app.get("/tracks/{track_id}")
async def get_track_rankings(
    session: Annotated[Session, Depends(get_session)],
    track_id: int,
    username: str | None = None,
):
    db_rankings = (
        session.query(Ranking)
        .where(
            Ranking.track_id == track_id,
            (Ranking.username == username) if username is not None else true(),
        )
        .all()
    )
    if len(db_rankings) == 0:
        raise HTTPException(status_code=404, detail="Оценки не найдены.")
    return db_rankings


@app.get("/rankings/{album_id}")
async def get_album_rankings(
    album_id: int, session: Annotated[Session, Depends(get_session)]
):
    db_tracks = session.query(Track).where(Track.album_id == album_id).all()
    if not session.query(Ranking).where(Ranking.track_id == db_tracks[0].id).first():
        raise HTTPException(status_code=404, detail="У альбома нет ранкингов.")
    db_rankings = []
    for track in db_tracks:
        rankings = []
        i = 0
        for ranking in session.query(Ranking).where(Ranking.track_id == track.id).all():
            rankings.append(
                {"username": ranking.username, "placement": ranking.placement}
            )
            i += 1
        placements = [dict["placement"] for dict in rankings]
        db_rankings.append(
            {
                "track_name": track.track_name,
                "rankings": rankings,
                "placement": round(sum(placements) / len(placements) * 100) / 100,
            }
        )
    return sorted(db_rankings, key=lambda d: d["placement"])


@app.get("/config/")
async def get_config(session: Annotated[Session, Depends(get_session)]):
    return session.query(Config).first()


@app.patch("/config/")
async def change_config(
    config: schemas.Config,
    session: Annotated[Session, Depends(get_session)],
):
    db_config = session.query(Config).first()
    session.execute(
        update(Config),
        [
            {
                "id": db_config.id,
                "current_round": (
                    config.current_round
                    if config.current_round is not None
                    else db_config.current_round
                ),
                "current_order_number": (
                    config.current_order_number
                    if config.current_order_number is not None
                    else db_config.current_order_number
                ),
                "max_submissions": (
                    config.max_submissions
                    if config.max_submissions is not None
                    else db_config.max_submissions
                ),
                "submissions_open": (
                    config.submissions_open
                    if config.submissions_open is not None
                    else db_config.submissions_open
                ),
                "max_duration": (
                    config.max_duration
                    if config.max_duration is not None
                    else db_config.max_duration
                ),
                "max_tracks": (
                    config.max_tracks
                    if config.max_tracks is not None
                    else db_config.max_tracks
                ),
                "min_tracks": (
                    config.min_tracks
                    if config.min_tracks is not None
                    else db_config.min_tracks
                ),
            }
        ],
    )
    session.commit()
    session.refresh(db_config)
    return db_config
