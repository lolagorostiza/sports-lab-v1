
from ast import List
import enum
from sports_lab_v1.domain.models import Frame
from sports_lab_v1.domain.models import Position


def parse_row(line: str) -> Frame:
    items = line.strip().split(',')
    frameTime = float(items[0])
    itemsSize = len(items)
    ballPosition = Position(float(items[-2]), float(items[-1]))
    
    players = tuple(
        Position(float(items[i]), float(items[i + 1]))
        for i in range(1, len(items) - 2, 2)
    )
        
    return Frame(t= frameTime, players= players, ball= ballPosition)