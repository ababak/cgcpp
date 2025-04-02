"""
(c) Andriy Babak 2021

date: 28/05/2021
modified: 02/04/2025 12:25:46

Author: Andriy Babak
e-mail: ababak@gmail.com
------------------------------
description: CG C++ Support module
------------------------------
"""

from __future__ import print_function

import os
import re
import shutil
import subprocess
import sys

import setuptools
from setuptools.command.bdist_egg import bdist_egg as BuildEggCommand
from setuptools.command.build_ext import build_ext

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

    DOCKER_APP = "docker"
    DOCKER_IMAGE = "ababak/cgcpp:" + ".".join(VERSION.split(".")[:2])

    def __init__(self, name, sourcedir=""):
        setuptools.Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

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
)
