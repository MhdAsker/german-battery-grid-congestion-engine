from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from gridflex.features.targets import target_diagnostics
from gridflex.validation import validate_timeseries


def main() -> None:
    parser = argparse.ArgumentParser(prog="gridflex")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate", help="validate a canonical parquet dataset")
    validate.add_argument("path", type=Path)
    validate.add_argument("--frequency", default="15min")
    diagnose = sub.add_parser("diagnose-target", help="report target distribution without modeling")
    diagnose.add_argument("path", type=Path)
    diagnose.add_argument("--column", default="curtailment_mwh")
    diagnose.add_argument("--threshold", type=float, default=0.1)
    args = parser.parse_args()
    frame = pd.read_parquet(args.path)
    if args.command == "validate":
        result = validate_timeseries(frame, frequency=args.frequency)
    else:
        result = target_diagnostics(frame[args.column], args.threshold)
    print(json.dumps(result, default=str, indent=2))


if __name__ == "__main__":
    main()
