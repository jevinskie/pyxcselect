#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

from packaging.version import Version
from rich import print

from .. import _version, xcselect


def real_main(args: argparse.Namespace) -> int:
    verbose: bool = args.verbose
    if args.version:
        print(Version(_version.version))
    elif args.xcselect_version:
        print(xcselect.version())
    elif args.developer_dir:
        path = xcselect.developer_dir()
        print(path())
        if verbose:
            print(f"from_env_var: {path.from_env_var}")
            print(f"from_command_line_tools: {path.from_command_line_tools}")
            print(f"from_default: {path.from_default}")
    return 0


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=Path(__file__).stem,
        description="pyxcselect, Python bindings to libxcselect.dylib, frontend. Utility for getting Xcode related paths.",
    )
    parser.add_argument(
        "-d", "--developer-dir", action="store_true", help="display the Developer directory path"
    )
    parser.add_argument(
        "--xcselect-version", action="store_true", help="display the version of libxcselect"
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
