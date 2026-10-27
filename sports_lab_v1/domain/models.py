from dataclasses import dataclass
from math import sqrt
from statistics import fmean
from turtle import distance
from enum import Enum

from sports_lab_v1.domain.errors import InvalidFrame, InvalidPosition

PITCH_LENGTH_M = 105.0
PITCH_WIDTH_M = 68.0

@dataclass(frozen=True, slots=True)
class Position:
    x: float
    y: float

    def __post_init__(self) -> None:
        if not (0.0 <= self.x <= PITCH_LENGTH_M and 0.0 <= self.y <= PITCH_WIDTH_M):
            raise InvalidPosition()
    
    def distance_to(self, other:"Position") -> float:
        return sqrt(pow(other.x-self.x, 2) + pow(other.y-self.y, 2))

@dataclass(frozen=True, slots=True)
class Frame:
    t: float
    players: tuple[Position, ...]
    ball: Position
    
    def __post_init__(self) -> None:
        if self.t < 0:
            raise InvalidFrame()
        
        if len(self.players) < 2:
            raise InvalidFrame()
        
    @property
    def centroid(self) -> Position:
        mean_x = fmean(p.x for p in self.players)
        mean_y = fmean(p.y for p in self.players)
        
        return Position(mean_x, mean_y)
    
    def spread(self) -> float:
      return fmean(p.distance_to(self.centroid) for p in self.players)

class BlockState(Enum):
    COMPACT = "compact"
    STRETCHED = "stretched"
    BROKEN = "broken"