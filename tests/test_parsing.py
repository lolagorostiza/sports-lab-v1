import pytest
import subprocess
import sys
from sports_lab_v1.parsing import parse_row
from sports_lab_v1.domain.errors import InvalidFrame, InvalidPosition


def test_line_parsed_ok():
    line = "0.0,64.443,32.944,62.394,40.111,62.945,28.683,52.500,34.000"
    
    parsedFrame = parse_row(line)
    
    assert parsedFrame.t == 0.0

def test_line__with_incorrect_position():
    line = "0.0,64.443,3222.944,62.394,40.111,62.945,28.683,52.500,34.000"
    
    with pytest.raises(InvalidPosition):    
        parse_row(line)

def test_analyze_valid_fixture_cli():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sports_lab_v1",
            "analyze",
            "data/a1_match_sample.csv",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, (
        f"El comando falló.\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
    
def test_analyze_missing_file_cli():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sports_lab_v1",
            "analyze",
            "data/no_existe.csv",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert result.stderr.strip()
    assert "Traceback" not in result.stderr

def test_analyze_prints_table_and_summary():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sports_lab_v1",
            "analyze",
            "data/a1_match_sample.csv",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0

    assert "t" in result.stdout
    assert "spread" in result.stdout
    assert "state" in result.stdout

    assert "COMPACT" in result.stdout
    assert "STRETCHED" in result.stdout
    assert "BROKEN" in result.stdout