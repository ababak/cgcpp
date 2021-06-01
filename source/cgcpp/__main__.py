"""
(c) Andriy Babak 2021

date: 01/06/2021
modified: 01/06/2021 14:35:04

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

DOCKER_APP = "docker"
DOCKER_IMAGE = "cgcpp"


def execute_task(command, shell=False, prefix="", env=None):
    """
    Execute task and print out the output
    """
    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=shell, env=env)
    except OSError:
        out_text = 'Command not found: "{}"'.format(command)
        if prefix:
            out_text = "[" + prefix + "] " + out_text
        print(out_text)
        raise
    except Exception as e:
        print('Error executing the command "%s": %r', command, e)
        raise
    for stdout_line in iter(proc.stdout.readline, b""):
        out_text = stdout_line.strip()
        if prefix:
            out_text = "[" + prefix + "] " + out_text
        print(out_text)
    proc.stdout.close()
    return_code = proc.wait()
    return return_code


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
    args, unknownargs = parser.parse_known_args()
    source_dir = os.path.abspath(args.source).replace("\\", "/")
    out_dir = os.path.abspath(args.out or source_dir).replace("\\", "/")
    if not os.path.isdir(args.source):
        print('[ERROR] Directory does not exist: "{}"'.format(source_dir))
        sys.exit(1)
    try:
        out = subprocess.check_output([DOCKER_APP, "--version"])
    except OSError:
        print("[ERROR] Docker not installed")
        sys.exit(2)
    out = subprocess.check_output([DOCKER_APP, "images", "-q", DOCKER_IMAGE])
    if not out:
        print("[ERROR] Docker image is missing: {}".format(DOCKER_IMAGE))
        print("Please reinstall cgcpp to rebuild it")
        sys.exit(3)
    print('Building: "{}"'.format(source_dir))
    print('Output: "{}"'.format(out_dir))
    docker_args = [
        DOCKER_APP,
        "run",
        "--rm",
        # "-it",
        "-v",
        "{}:c:/source:ro".format(os.path.abspath(source_dir)),
        "-v",
        "{}:c:/out".format(os.path.abspath(out_dir)),
    ]
    if args.maya:
        if not os.path.isdir(args.maya):
            print(
                '[ERROR] Autodesk Maya directory does not exist: "{}"'.format(args.maya)
            )
            sys.exit(1)
        docker_args += ["-v", args.maya + ":c:/autodesk:ro"]
        print('Autodesk Maya search directory: "{}"'.format(args.maya))
    docker_args += [DOCKER_IMAGE]
    subprocess.check_call(docker_args)


if __name__ == "__main__":
    main()
