#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

from packaging.version import Version
from rich import print

from .. import _version, xcrun


def real_main(args: argparse.Namespace) -> int:
    verbose: bool = args.verbose
    if args.version:
        print(Version(_version.version))
    return 0


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=Path(__file__).stem,
        description="pyxcrun, Python bindings to xcrun/libxcrun.dylib, frontend. Utility for getting Xcode related paths and running Xcode commands.",
    )
    parser.add_argument(
        "--xcrun-version", action="store_true", help="display the version of xcrun/libxcrun.dylib"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="be verbose")
    parser.add_argument(
        "-V", "--version", action="store_true", help="display the version of this program"
    )
    return parser


def main() -> int:
    parser = get_arg_parser()
    args = parser.parse_args()
    if not any(dict(args._get_kwargs()).values()):
        parser.print_help()
        return 1
    return real_main(args)


if __name__ == "__main__":
    sys.exit(main())
