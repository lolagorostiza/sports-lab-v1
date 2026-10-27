from asyncio.windows_events import NULL

from sports_lab_v1.domain.models import Frame, BlockState

class BlockCompactness:
    stretched_above: float
    broken_above: float
    
    def __init__(self, stretched_above: float = 22.0, broken_above: float = 28.0) -> None:
        if stretched_above >= broken_above:
            raise ValueError("stretched_above must be below broken_above")
        self._stretched_above = stretched_above
        self._broken_above = broken_above

    def classify(self, frame: Frame) -> BlockState:
        spread = frame.spread()
        if spread > self._broken_above:
            return BlockState.BROKEN
        if spread > self._stretched_above:
            return BlockState.STRETCHED
        return BlockState.COMPACT