"""
(c) Andriy Babak 2021

date: 01/06/2021
modified: 17/03/2022 17:10:03

Author: Andriy Babak
e-mail: ababak@gmail.com
------------------------------
description: CG C++ Support module
------------------------------
"""

from __future__ import print_function, absolute_import
import os
import sys
import argparse
import subprocess

from . import __version__, __copyright__
from . import build


def main():
    parser = argparse.ArgumentParser(
        description="C++ module builder",
        version=__version__,
        epilog=__copyright__,
        prog="python -m cgcpp",
    )
    parser.add_argument(
        "source", type=str, help="directory containing CMakeLists.txt to build"
    )
    parser.add_argument("--out", help="output directory")
    maya_default_directory = "C:/Program Files/Autodesk"
    parser.add_argument(
        "--maya",
        help='Autodesk directory with Maya installations. Default: "{}".'.format(
            maya_default_directory
        ),
        nargs="?",
        const=maya_default_directory,
    )
    sidefx_default_directory = "C:/Program Files/Side Effects Software"
    parser.add_argument(
        "--sidefx",
        help='SideFX directory with Houdini installations. Default: "{}".'.format(
            sidefx_default_directory
        ),
        nargs="?",
        const=sidefx_default_directory,
    )
    args, unknownargs = parser.parse_known_args()
    source_dir = os.path.abspath(args.source).replace("\\", "/")
    out_dir = os.path.abspath(args.out or source_dir).replace("\\", "/")
    if not os.path.isdir(args.source):
        print('[ERROR] Directory does not exist: "{}"'.format(source_dir))
        sys.exit(1)
    result = build.build(
        source_dir=source_dir,
        destination_dir=out_dir,
        maya_dir=args.maya,
        sidefx_dir=args.sidefx,
    )
    if not result:
        sys.exit(result)


if __name__ == "__main__":
    main()
