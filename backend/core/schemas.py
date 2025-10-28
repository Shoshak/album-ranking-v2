from pydantic import BaseModel, Field
from datetime import time


class Album(BaseModel):
    source: str = Field(examples=["spotify"])
    url: str = Field(
        examples=[
            "https://open.spotify.com/album/4T7JGfRryhw5POaXalkApE",
        ]
    )
    username: str = Field(examples=["Joosenitsa"])


class Session(BaseModel):
    id: int
    first_name: str
    username: str
    photo_url: str
    auth_date: int
    hash: str

class SessionPatch(BaseModel):
    id: str
    auth_date: int

class User(BaseModel):
    id: int
    username: str
    admin_rights: bool = Field(default=False)


class Ranking(BaseModel):
    username: str = Field(examples=["Joosenitsa"])
    placements: list[int] = Field(
        examples=[
            [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23,
            ]
        ]
    )


class Config(BaseModel):
    current_round: int = Field(default=None, examples=[1])
    current_order_number: int = Field(default=None, examples=[1])
    max_submissions: int = Field(default=None, examples=[2])
    submissions_open: bool = Field(default=None, examples=[False])
    max_duration: time = Field(default=None, examples=[time(hour=2)])
    max_tracks: int = Field(default=None, examples=[30])
    min_tracks: int = Field(default=None, examples=[7])
