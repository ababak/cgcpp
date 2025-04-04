"""
(c) Andriy Babak 2021

date: 28/05/2021
modified: 04/04/2025 15:32:12

Author: Andriy Babak
e-mail: ababak@gmail.com
------------------------------
description: CG C++ Support module
------------------------------
"""

import os
import shutil
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
ROOT_PATH = Path(__file__).parent.absolute()
SOURCE_PATH = ROOT_PATH / "source"
BUILD_PATH = ROOT_PATH / "build"


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


class CMakeBuild(build_ext):
    """
    Build CMake using docker image
    """

    DOCKER_APP = "docker"
    DOCKER_IMAGE = f"ababak/cgcpp:{'.'.join(VERSION.split('.')[:2])}"

    def run(self):
        """Prepare the Docker image and run the build."""
        # Check if Docker is installed
        try:
            out = subprocess.check_output([self.DOCKER_APP, "--version"])
        except OSError:
            extensions = ", ".join(e.name for e in self.extensions)
            raise RuntimeError(
                f"Docker must be installed to build the following extensions: {extensions}"
            )
        # Check if the image is available
        out = subprocess.check_output(
            [self.DOCKER_APP, "images", "-q", self.DOCKER_IMAGE]
        )
        if not out:
            # Try to pull the image from Docker Hub
            try:
                print(f'Trying to pull the docker image "{self.DOCKER_IMAGE}"...')
                out = subprocess.check_output(
                    [self.DOCKER_APP, "pull", self.DOCKER_IMAGE]
                )
                print(f'Pulled the docker image "{self.DOCKER_IMAGE}"...')
            except subprocess.CalledProcessError:
                # If the image is not available, build it from the Dockerfile
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
        super().run()

    def build_extension(self, ext):
        staging_path = Path(self.get_ext_fullpath(ext.name)).parent.absolute()
        if not staging_path.exists():
            os.makedirs(staging_path)
        # relative_file_path = Path(dirpath).relative_to(SOURCE_PATH)
        # source_path = dirpath
        # destination_path = (staging_path / relative_file_path).parent
        # for i, j in ext.__dict__.items():
        #     print(f"{i} = {j}")
        print("staging_path", staging_path)
        sdir = Path(__file__).parent
        sources_path = os.path.commonpath(ext.sources)
        source_dir = sdir / sources_path
        print("sdir", sdir)
        print("source_dir", source_dir)
        print(f'Building extension "{ext.name}" using "{self.DOCKER_IMAGE}"...')
        docker_args = [
            self.DOCKER_APP,
            "run",
            "--rm",
            "-v",
            f"{source_dir}:c:/source:ro",
            "-v",
            f"{staging_path}:c:/out",
            self.DOCKER_IMAGE,
        ]
        subprocess.check_call(docker_args)


# Configuration.
setuptools.setup(
    ext_modules=[
        setuptools.Extension(
            "cgcpp.lib_loader",
            sources=[
                "source_lib_loader/lib_loader.cpp",
                "source_lib_loader/CMakeLists.txt",
            ],
        )
    ],
    cmdclass={
        "build_ext": CMakeBuild,
        "bdist_wheel": BdistWheelCommand,
    },
    zip_safe=False,
)
