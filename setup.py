"""
(c) Andriy Babak 2021

date: 28/05/2021
modified: 04/08/2022 17:50:02

Author: Andriy Babak
e-mail: ababak@gmail.com
------------------------------
description: CG C++ Support module
------------------------------
"""

from __future__ import print_function
import os
import re
import sys
import shutil
import subprocess

from setuptools.command.build_ext import build_ext
from setuptools.command.bdist_egg import bdist_egg as BuildEggCommand
import setuptools

# Define paths

PLUGIN_NAME = "cgcpp-{0}"

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
SOURCE_PATH = os.path.join(ROOT_PATH, "source")
README_PATH = os.path.join(ROOT_PATH, "README.md")
BUILD_PATH = os.path.join(ROOT_PATH, "build")
STAGING_PATH = os.path.join(BUILD_PATH, PLUGIN_NAME)

with open(os.path.join(SOURCE_PATH, "cgcpp", "_version.py")) as _version_file:
    VERSION = re.match(
        r".*__version__ = [\'\"](.*?)[\'\"]", _version_file.read(), re.DOTALL
    ).group(1)


STAGING_PATH = STAGING_PATH.format(VERSION)


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
                "--rm",
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


# Custom commands.
class BuildPlugin(setuptools.Command):
    """Build plugin."""

    description = "Build plugin and create an archive"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run the build step."""
        # Clean staging path
        shutil.rmtree(STAGING_PATH, ignore_errors=True)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", ".", "--target", STAGING_PATH]
        )
        # Generate plugin zip
        shutil.make_archive(
            os.path.join(BUILD_PATH, PLUGIN_NAME.format(VERSION)), "zip", STAGING_PATH
        )


class BuildEgg(BuildEggCommand):
    '''Custom egg build to ensure resources built.

    .. note::

        Required because when this project is a dependency for another project,
        only bdist_egg will be called and *not* build.

    '''

    def run(self):
        '''Run egg build ensuring build_resources called first.'''
        self.run_command('build_ext')
        BuildEggCommand.run(self)


# Configuration.
setuptools.setup(
    name="cgcpp",
    version=VERSION,
    description="CG C++ Support module.",
    long_description=open(README_PATH).read(),
    keywords="",
    url="https://github.com/ababak/cgcpp",
    author="Andriy Babak",
    author_email="ababak@gmail.com",
    license="Apache License (2.0)",
    packages=setuptools.find_packages(SOURCE_PATH),
    package_dir={"": "source"},
    ext_modules=[CMakeExtension("cgcpp/lib_loader", "source_lib_loader")],
    cmdclass={
        "build_ext": CMakeBuild,
        "bdist_egg": BuildEgg,
        "build_plugin": BuildPlugin,
    },
    zip_safe=False,
)
