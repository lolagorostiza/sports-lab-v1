from dataclasses import dataclass
from enum import Enum

PITCH_LENGTH_M = 105.0
PITCH_WIDTH_M = 68.0

@dataclass(frozen=True, slots=True)
class Position:
    x: float
    y: float
    
    def distance_to(self, other: "Position") -> float: ...

@dataclass(frozen=True, slots=True)
class Frame:
    t: float
    players: tuple[Position, ...]
    ball: Position
    
    @property
    def centroid(self) -> Position: ...
    
    def spread(self) -> float: ...

class BlockState(Enum):
    COMPACT = "compact"
    STRETCHED = "stretched"
    BROKEN = "broken"