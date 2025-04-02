"""
(c) Andriy Babak 2021

date: 28/05/2021
modified: 02/04/2025 13:03:56

Author: Andriy Babak
e-mail: ababak@gmail.com
------------------------------
description: CG C++ Support module
------------------------------
"""

import os
import re
import shutil
import subprocess
import sys

import setuptools
import toml
from setuptools.command.bdist_egg import bdist_egg as BuildEggCommand
from setuptools.command.build_ext import build_ext


def get_version() -> str:
    """Read package version from the pyproject.toml file."""
    with open("pyproject.toml", encoding="utf-8") as fd:
        pyproject = toml.load(fd)
    return pyproject["project"]["version"]


VERSION = get_version()


class CMakeExtension(setuptools.Extension):
    def __init__(self, name, sourcedir=""):
        setuptools.Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    """
    Build CMake using docker image
    """

    DOCKER_APP = "docker"
    DOCKER_IMAGE = "ababak/cgcpp:" + ".".join(VERSION.split(".")[:2])

    def run(self):
        try:
            out = subprocess.check_output([self.DOCKER_APP, "--version"])
        except OSError:
            raise RuntimeError(
                "Docker must be installed to build the following extensions: {extensions}".format(
                    extensions=", ".join(e.name for e in self.extensions)
                )
            )
        out = subprocess.check_output(
            [self.DOCKER_APP, "images", "-q", self.DOCKER_IMAGE]
        )
        if not out:
            print('Building docker image "{}"...'.format(self.DOCKER_IMAGE))
            docker_args = [
                self.DOCKER_APP,
                "build",
                # "--rm",
                "-t",
                self.DOCKER_IMAGE,
                ".",
            ]
            subprocess.check_call(docker_args)
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        if not os.path.exists(extdir):
            os.makedirs(extdir)
        sourcedir = ext.sourcedir
        print(
            'Building extension "{}" using "{}"...'.format(ext.name, self.DOCKER_IMAGE)
        )
        docker_args = [
            self.DOCKER_APP,
            "run",
            "--rm",
            "-v",
            "{}:c:/source:ro".format(sourcedir),
            "-v",
            "{}:c:/out".format(os.path.abspath(extdir)),
            self.DOCKER_IMAGE,
        ]
        subprocess.check_call(docker_args)


# Configuration.
setuptools.setup(
    ext_modules=[CMakeExtension("cgcpp/lib_loader", "source_lib_loader")],
    cmdclass={
        "build_ext": CMakeBuild,
    },
    zip_safe=False,
)
