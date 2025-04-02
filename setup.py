"""
(c) Andriy Babak 2021

date: 28/05/2021
modified: 02/04/2025 13:31:23

Author: Andriy Babak
e-mail: ababak@gmail.com
------------------------------
description: CG C++ Support module
------------------------------
"""

import os
import subprocess
from pathlib import Path

import setuptools
import toml
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
        self.sourcedir = Path(sourcedir).absolute()


class CMakeBuild(build_ext):
    """
    Build CMake using docker image
    """

    DOCKER_APP = "docker"
    DOCKER_IMAGE = f"ababak/cgcpp:{'.'.join(VERSION.split('.')[:2])}"

    def run(self):
        try:
            out = subprocess.check_output([self.DOCKER_APP, "--version"])
        except OSError:
            extensions = ", ".join(e.name for e in self.extensions)
            raise RuntimeError(
                f"Docker must be installed to build the following extensions: {extensions}"
            )
        out = subprocess.check_output(
            [self.DOCKER_APP, "images", "-q", self.DOCKER_IMAGE]
        )
        if not out:
            print(f'Building docker image "{self.DOCKER_IMAGE}"...')
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
        extdir = Path(self.get_ext_fullpath(ext.name)).parent.absolute()
        if not extdir.exists():
            os.makedirs(extdir)
        sourcedir = ext.sourcedir
        print(f'Building extension "{ext.name}" using "{self.DOCKER_IMAGE}"...')
        docker_args = [
            self.DOCKER_APP,
            "run",
            "--rm",
            "-v",
            f"{sourcedir}:c:/source:ro",
            "-v",
            f"{extdir}:c:/out",
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
