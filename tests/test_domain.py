
from tarfile import BLOCKSIZE

import pytest
from dataclasses import FrozenInstanceError
from sports_lab_v1.domain.analysis import BlockCompactness
from sports_lab_v1.domain.errors import InvalidFrame, InvalidPosition
from sports_lab_v1.domain.models import BlockState, Position
from sports_lab_v1.domain.models import Frame

def test_position_equality():
    pos1 = Position(10.0, 20.0)
    pos2 = Position(10.0, 20.0)
    pos3 = Position(15.0, 25.0)

    assert pos1 == pos2
    assert pos1 != pos3

def test_position_is_frozen():
    pos = Position(10.0, 20.0)
    
    with pytest.raises(FrozenInstanceError):
        pos.x = 1.0

def test_position_limits_valid():
    with pytest.raises(InvalidPosition): # 1
        Position(-20, 30)

    with pytest.raises(InvalidPosition): # 2
        Position(500, 20)

    with pytest.raises(InvalidPosition): # 3
        Position(10, -40)

    with pytest.raises(InvalidPosition): # 4
        Position(10, -60)
    
    Position(0, 0)
    Position(105, 68)
    
def test_distance_correct():
    pos1 = Position(0.0, 0.0)
    pos2 = Position(3.0, 4.0)
    currentDistance = pos1.distance_to(pos2)
    expectedDistance = 5.0
    
    assert currentDistance == pytest.approx(expectedDistance)

# Frame

def test_not_negative_time():
    with pytest.raises(InvalidFrame):
        frame = Frame(
            t=-1.5,
            players=(
                Position(10.0, 20.0),
                Position(30.0, 40.0),
                Position(50.0, 60.0),
            ),
            ball=Position(25.0, 35.0)
        )

def test_calculate_centroid():
    frame = Frame(
        t=0.0,
        players=(
            Position(0.0, 0.0),
            Position(4.0, 0.0),
            Position(4.0, 4.0),
            Position(0.0, 4.0),
        ),
        ball=Position(2.0, 2.0),
    )
    
    assert Position(2.0, 2.0) == frame.centroid

def test_maximum_not_media():
    frame = Frame(
        t=0.0,
        players=(
            Position(0.0, 10.0),
            Position(0.0, 20.0),
            Position(0.0, 30.0),
            Position(0.0, 40.0),
            Position(0.0, 50.0)
        ),
        ball=Position(2.0, 2.0),
    )

    assert 12.0 == frame.spread()

def test_blockstate_correct():
    assert BlockState("compact") is BlockState.COMPACT

def test_frame_less_two_players_error():
    with pytest.raises(InvalidFrame):
        Frame(
                t=0.0,
                players=(
                    Position(0.0, 10.0),
                ),
                ball=Position(2.0, 2.0),
            )
        
    
# Analysis
@pytest.fixture
def frame():
    return Frame(
        t=1.5,
        players=(
            Position(10.0, 20.0),
            Position(30.0, 40.0),
            Position(50.0, 60.0),
        ),
        ball=Position(25.0, 35.0),
    )
    
def test_threshold_compact():
    frame = Frame(
                t= 1.5,
                players=(
                    Position(10.0, 20.0),
                    Position(30.0, 40.0),
                    Position(50.0, 60.0),
                ),
                ball=Position(25.0, 35.0)
            )
    
    classifier = BlockCompactness(22,28)
    
    assert classifier.classify(frame) == BlockState.COMPACT
    
def test_threshold_stretched():
    frame = Frame(
                t= 1.5,
                players=(
                    Position(10.0, 20.0),
                    Position(30.0, 40.0),
                    Position(50.0, 60.0),
                ),
                ball=Position(25.0, 35.0)
            )
    
    classifier = BlockCompactness(12,28)
    
    assert classifier.classify(frame) == BlockState.STRETCHED
    
def test_threshold_broken():
    frame = Frame(
                t= 1.5,
                players=(
                    Position(10.0, 20.0),
                    Position(30.0, 40.0),
                    Position(50.0, 60.0),
                ),
                ball=Position(25.0, 35.0)
            )
    
    classifier = BlockCompactness(10,15)
    
    assert classifier.classify(frame) == BlockState.BROKEN