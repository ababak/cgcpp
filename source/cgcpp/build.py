"""
(c) Andriy Babak 2021

date: 03/06/2021
modified: 03/06/2021 16:46:06

Author: Andriy Babak
e-mail: ababak@gmail.com
------------------------------
description: CG C++ Support module
------------------------------
"""

from __future__ import print_function
import os
import subprocess

DOCKER_APP = "docker"
DOCKER_IMAGE = "cgcpp"


def build(source_dir, destionation_dir=None, maya_dir=None):
    """Run docker image to build source directory."""
    source_dir = os.path.abspath(source_dir).replace("\\", "/")
    destionation_dir = os.path.abspath(destionation_dir or source_dir).replace(
        "\\", "/"
    )
    try:
        out = subprocess.check_output([DOCKER_APP, "images", "-q", DOCKER_IMAGE])
    except OSError:
        print("[ERROR] Docker not installed")
        return 2
    if not out:
        print("[ERROR] Docker image is not available: {}".format(DOCKER_IMAGE))
        print("Please reinstall cgcpp to rebuild it")
        return 3
    print('Building: "{}"'.format(source_dir))
    print('Output: "{}"'.format(out_dir))
    docker_args = [
        DOCKER_APP,
        "run",
        "--rm",
        "-v",
        "{}:c:/source:ro".format(os.path.abspath(source_dir)),
        "-v",
        "{}:c:/out".format(os.path.abspath(out_dir)),
    ]
    if maya_dir:
        maya_dir = os.path.abspath(maya_dir).replace("\\", "/")
        if not os.path.isdir(maya_dir):
            print(
                '[ERROR] Autodesk Maya directory does not exist: "{}"'.format(maya_dir)
            )
            return 1
        docker_args += ["-v", maya_dir + ":c:/autodesk:ro"]
        print('Autodesk Maya search directory: "{}"'.format(maya_dir))
    docker_args += [DOCKER_IMAGE]
    subprocess.check_call(docker_args)
    return 0
