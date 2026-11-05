
import argparse
import sys
from collections.abc import Iterator
from sports_lab_v1.parsing import parse_row
from sports_lab_v1.domain.analysis import BlockCompactness, FurthestPolicy, CompositePolicy
from sports_lab_v1.domain.errors import DomainError
from sports_lab_v1.utils import read_lines


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
    elif args.command == "compare":
        compactness = BlockCompactness(22, 28)
        furthest = FurthestPolicy(22, 28)
        try:
            print(f"{'t':>5} {'spread':>10} {'state':>10}")
            for line in read_lines(args.path):
                frame = parse_row(line)
                print(
                    f"{frame.t:5.1f} "
                    f"{compactness.classify(frame).name:>12}"
                    f"{furthest.classify(frame).name:>10}"
                )                
        
        except DomainError as error:
            print(f"error: {error}", file=sys.stderr)
                
    return 0

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sports_lab_v1")
    subparsers = parser.add_subparsers(
        dest= "command",
        required= True
    )
    
    analyze_parser =  subparsers.add_parser("analyze")
    analyze_parser.add_argument("path")
    
    analyze_parser =  subparsers.add_parser("compare")
    analyze_parser.add_argument("path")
    
    return parser

if __name__ == "__main__":
    raise SystemExit(main())
    
    