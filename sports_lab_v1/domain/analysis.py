from typing import Protocol
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

class ClassificationPolicy(Protocol):
    def classify(self, frame:Frame) -> BlockState: ...

class FurthestPolicy():
    stretched_above: float
    broken_above: float
    
    def __init__(self, stretched_above: float = 22.0, broken_above: float = 28.0) -> None:
        if stretched_above >= broken_above:
            raise ValueError("stretched_above must be below broken_above")
        self._stretched_above = stretched_above
        self._broken_above = broken_above
        
    def classify(self, frame:Frame) -> BlockState:
        furthest = frame.furthest
        if furthest > self._broken_above:
                    return BlockState.BROKEN
        if furthest > self._stretched_above:
            return BlockState.STRETCHED
        return BlockState.COMPACT

class CompositePolicy():
    def __init__(self, policies:list[ClassificationPolicy]) -> None:
        self.policies = policies
    
    def classify(self, frame:Frame) -> BlockState:
        blockStates = [policy.classify(frame) for policy in self.policies]
        
        SEVERITY = {
            BlockState.COMPACT: 0,
            BlockState.STRETCHED: 1,
            BlockState.BROKEN: 2,
        }
        return max(blockStates, key=SEVERITY.__getitem__)
        
    
def classify_match(frames:tuple[Frame,...], 
                   policy:ClassificationPolicy) -> list[BlockState]:
    return [policy.classify(frame) for frame in frames]

