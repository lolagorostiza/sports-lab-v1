import pytest
from pathlib import Path
from sports_lab_v1.domain.analysis import ClassificationPolicy, FurthestPolicy, classify_match
from sports_lab_v1.domain.models import BlockState, Frame, Position
from tests.test_domain import frame
from sports_lab_v1.utils import read_lines
from sports_lab_v1.parsing import parse_row
from sports_lab_v1.domain.analysis import BlockCompactness, FurthestPolicy


@pytest.fixture
def anyFrame1():
    return Frame(
        t=1.0,
        players=(
            Position(1, 0),       
            Position(95, 55),
            Position(100, 55),
            Position(95, 60),
            Position(100, 60),
            Position(90, 65),
            Position(95, 65),
            Position(100, 65),
            Position(105, 60),
            Position(105, 65),
            Position(90, 55),
        ),
        ball=Position(52.1, 35.12))

@pytest.fixture
def anyFrame2():
    return Frame(
        t=1.0,
        players=(
            Position(2, 0),       
            Position(95, 55),
            Position(100, 55),
            Position(95, 60),
            Position(100, 60),
            Position(90, 65),
            Position(95, 65),
            Position(100, 65),
            Position(105, 60),
            Position(105, 65),
            Position(90, 55),
        ),
        ball=Position(52.1, 35.12))

@pytest.fixture
def anyFrame3():
    return Frame(
        t=1.0,
        players=(
            Position(3, 0),       
            Position(95, 55),
            Position(100, 55),
            Position(95, 60),
            Position(100, 60),
            Position(90, 65),
            Position(95, 65),
            Position(100, 65),
            Position(105, 60),
            Position(105, 65),
            Position(90, 55),
        ),
        ball=Position(52.1, 35.12))

def test_classification_policy_can_be_imported():
    assert ClassificationPolicy is not None

def test_classification_policy_declares_classify():
    assert hasattr(ClassificationPolicy, "classify")

def test_classification_policy_cannot_be_instantiated():
    with pytest.raises(TypeError):
        ClassificationPolicy()

def test_with_distant_player():
    frame = Frame(
        t=1.0,
        players=(
            Position(0, 0),       # Jugador muy alejado
            Position(95, 55),
            Position(100, 55),
            Position(95, 60),
            Position(100, 60),
            Position(90, 65),
            Position(95, 65),
            Position(100, 65),
            Position(105, 60),
            Position(105, 65),
            Position(90, 55),
        ),
        ball=Position(52.1, 35.12))
    
    policy = FurthestPolicy()
    assert BlockState.COMPACT != policy.classify(frame)

def test_with_players_together():
    frame = Frame(
        t=2.0,
        players=(
            Position(50, 30),
            Position(51, 30),
            Position(52, 31),
            Position(50, 32),
            Position(51, 32),
            Position(52, 32),
            Position(50, 33),
            Position(51, 33),
            Position(52, 33),
            Position(49, 31),
            Position(53, 31),
        ),
        ball=Position(51, 32),
    )
    
    policy = FurthestPolicy()
    assert BlockState.COMPACT == policy.classify(frame)

def test_classify_match_with_policy_always_broken(anyFrame1):
    class AlwaysBrokenPolicy:
        def classify(self, frame):
            return BlockState.BROKEN
        
    frames = (anyFrame1, anyFrame1, anyFrame1)
    policy = AlwaysBrokenPolicy()
    
    states = classify_match(frames, policy)
    
    assert states == [BlockState.BROKEN, BlockState.BROKEN, BlockState.BROKEN]

def test_classify_match_with_policy_per_frame_verdict_keeps_order(anyFrame1, anyFrame2, anyFrame3):
    class PolicyByFrame:
        def __init__(self, verdicts:dict[Frame,BlockState]):
            self.verdicts = verdicts
            
        def classify(self, frame):
            return self.verdicts[frame]
    
    frames =  (anyFrame1, anyFrame2, anyFrame3)
    
    verdicts = {
        anyFrame1 : BlockState.COMPACT,
        anyFrame2 : BlockState.BROKEN,
        anyFrame3 : BlockState.STRETCHED,
    }
    
    policy = PolicyByFrame(verdicts)
    
    result = classify_match(frames, policy)
    assert result == [BlockState.COMPACT, BlockState.BROKEN, BlockState.STRETCHED]
    
def test_results_disagree_where_they_should():
    blockStates1 = [BlockCompactness().classify(parse_row(line)) 
                    for line in read_lines("data/a2_isolated_sample.csv")]
    
    blockStates2 = [FurthestPolicy().classify(parse_row(line)) 
                        for line in read_lines("data/a2_isolated_sample.csv")]
    
    assert blockStates1 != blockStates2

def test_results_agree_where_they_should():
    line = "0.0," + ",".join([
        "40.0,34.0", "41.0,34.0", "42.0,34.0", "43.0,34.0",
        "40.0,35.0", "41.0,35.0", "42.0,35.0", "43.0,35.0",
        "40.0,36.0", "41.0,36.0", "42.0,36.0", "43.0,36.0",
    ])
    blockStates1 = [BlockCompactness().classify(parse_row(line))]
    
    blockStates2 = [FurthestPolicy().classify(parse_row(line))]
    
    assert blockStates1 == blockStates2