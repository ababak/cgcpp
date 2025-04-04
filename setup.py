"""
(c) Andriy Babak 2021

date: 28/05/2021
modified: 04/04/2025 12:16:21

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
from wheel.bdist_wheel import bdist_wheel


def get_version() -> str:
    """Read package version from the pyproject.toml file."""
    with open("pyproject.toml", encoding="utf-8") as fd:
        pyproject = toml.load(fd)
    return pyproject["project"]["version"]


VERSION = get_version()


class BdistWheelCommand(bdist_wheel):
    def finalize_options(self):
        super().finalize_options()
        # Mark the wheel as compatible with any Python 3
        self.root_is_pure = False
        self.py_limited_api = False

    def get_tag(self):
        # Override the wheel tag to be platform-specific but Python-version agnostic
        impl = "py3"
        abi = "none"
        plat = self.plat_name.replace("-", "_").replace(".", "_")
        return impl, abi, plat


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
            try:
                print(f'Trying to pull the docker image "{self.DOCKER_IMAGE}"...')
                out = subprocess.check_output(
                    [self.DOCKER_APP, "pull", self.DOCKER_IMAGE]
                )
                print(f'Pulled the docker image "{self.DOCKER_IMAGE}"...')
            except subprocess.CalledProcessError:
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
        "bdist_wheel": BdistWheelCommand,
    },
    include_package_data=True,
    zip_safe=False,
)
