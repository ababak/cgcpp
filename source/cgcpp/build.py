"""
(c) Andriy Babak 2021

date: 03/06/2021
modified: 04/08/2022 16:58:02

Author: Andriy Babak
e-mail: ababak@gmail.com
------------------------------
description: CG C++ Support module
------------------------------
"""

from __future__ import print_function
import os
import subprocess

from . import __version__

DOCKER_APP = "docker"
DOCKER_IMAGE = "ababak/cgcpp:" + ".".join(__version__.split(".")[:2])


def build(
    source_dir, destination_dir=None, build_dir=None, maya_dir=None, sidefx_dir=None,
):
    """Run docker image to build source directory."""
    source_dir = os.path.abspath(source_dir).replace("\\", "/")
    destination_dir = os.path.abspath(destination_dir or source_dir).replace("\\", "/")
    try:
        out = subprocess.check_output([DOCKER_APP, "images", "-q", DOCKER_IMAGE])
    except OSError:
        print("[ERROR] Docker not installed")
        return 2
    if not out:
        print("[ERROR] Docker image is not available: {}".format(DOCKER_IMAGE))
        print("Please reinstall cgcpp to rebuild it")
        return 3
    print('Source: "{}"'.format(source_dir))
    print('Build: "{}"'.format(build_dir))
    print('Output: "{}"'.format(destination_dir))
    docker_args = [
        DOCKER_APP,
        "run",
        "--rm",
        "-v",
        "{}:c:/source:ro".format(os.path.abspath(source_dir)),
        "-v",
        "{}:c:/out".format(os.path.abspath(destination_dir)),
    ]
    if build_dir:
        docker_args += ["-v", "{}:c:/build".format(os.path.abspath(build_dir))]
    if maya_dir:
        maya_dir = os.path.abspath(maya_dir).replace("\\", "/")
        if not os.path.isdir(maya_dir):
            print(
                '[ERROR] Autodesk Maya directory does not exist: "{}"'.format(maya_dir)
            )
            return 1
        docker_args += ["-v", maya_dir + ":c:/autodesk:ro"]
        print('Autodesk Maya search directory: "{}"'.format(maya_dir))
    if sidefx_dir:
        sidefx_dir = os.path.abspath(sidefx_dir).replace("\\", "/")
        if not os.path.isdir(sidefx_dir):
            print('[ERROR] SideFX directory does not exist: "{}"'.format(sidefx_dir))
            return 1
        docker_args += ["-v", sidefx_dir + ":c:/sidefx:ro"]
        print('SideFX search directory: "{}"'.format(sidefx_dir))
    docker_args.append(DOCKER_IMAGE)
    subprocess.check_call(docker_args)
    return 0
