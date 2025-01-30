"""
(c) Andriy Babak 2021-2024

date: 01/06/2021
modified: 30/01/2025 14:12:22

Author: Andriy Babak
e-mail: ababak@gmail.com
------------------------------
description: CG C++ Support module
------------------------------
"""

import argparse
import os
import sys

from . import __copyright__, __version__, build


def main():
    parser = argparse.ArgumentParser(
        description="C++ module builder v{}".format(__version__),
        epilog=__copyright__,
        prog="python -m cgcpp",
    )
    parser.add_argument(
        "source", type=str, help="directory containing CMakeLists.txt to build"
    )
    parser.add_argument("--out", help="output directory")
    parser.add_argument("--build", help="build directory")
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
        "--houdini",
        help='SideFX directory with Houdini installations. Default: "{}".'.format(
            sidefx_default_directory
        ),
        nargs="?",
        const=sidefx_default_directory,
    )
    args, unknownargs = parser.parse_known_args()
    source_dir = os.path.abspath(args.source).replace("\\", "/")
    build_dir = args.build and os.path.abspath(args.build).replace("\\", "/")
    out_dir = os.path.abspath(args.out or source_dir).replace("\\", "/")
    if not os.path.isdir(args.source):
        print('[ERROR] Directory does not exist: "{}"'.format(source_dir))
        sys.exit(1)
    result = build.build(
        source_dir=source_dir,
        destination_dir=out_dir,
        build_dir=build_dir,
        maya_dir=args.maya,
        houdini_dir=args.houdini,
    )
    if not result:
        sys.exit(result)


if __name__ == "__main__":
    main()
