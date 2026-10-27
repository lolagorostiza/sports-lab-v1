
import argparse
import sys
from collections.abc import Iterator
from sports_lab_v1.parsing import parse_row
from sports_lab_v1.domain.analysis import BlockCompactness
from sports_lab_v1.domain.errors import DomainError


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    classifier = BlockCompactness(22,28)
    if args.command == "analyze":
        try:
            print(f"{'t':>5} {'spread':>10} {'state':>10}")
            for line in read_lines(args.path):
                frame = parse_row(line)
                print(f"{frame.t:5.1f} {frame.spread():10.2f} {classifier.classify(frame).name}")
        except DomainError as error:
            print(f"error: {error}", file=sys.stderr)
            return 2
    return 0

def read_lines(path:str) -> Iterator[str]:
    try:
        with open(path, encoding= "utf-8") as file:
            next(file, None)  # Saltar la cabecera
            for line in file:
                if line.strip():
                    yield line
    except OSError as error:
        raise DomainError(
            f"No se puede leer el fichero '{path}': {error}"
        ) from error

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sports_lab_v1")
    subparsers = parser.add_subparsers(
        dest= "command",
        required= True
    )
    
    analyze_parser =  subparsers.add_parser("analyze")
    analyze_parser.add_argument("path")
    
    return parser

if __name__ == "__main__":
    raise SystemExit(main())
    
    