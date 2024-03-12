from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class Kills(TypedDict):
    name: str
    kills: int


class GamePlayerRanking:
    total_kills: int = 0
    players: list = Field(default_factory=list)
    kills: Kills = Field(default_factory=dict)
